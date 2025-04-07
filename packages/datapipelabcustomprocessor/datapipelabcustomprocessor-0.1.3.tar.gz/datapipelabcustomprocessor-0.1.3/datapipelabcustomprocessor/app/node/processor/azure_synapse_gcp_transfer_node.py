from datapipelab.app.node.tnode import TNode

import os
import shutil
from google.cloud import storage
import json
from notebookutils import mssparkutils
from datapipelab.logger import logger

class AzureSynapseToGCPBucketNode(TNode):

    def __init__(self, spark, tnode_config):
        super().__init__(spark=spark)
        self.tnode_config = tnode_config
        self.spark = spark

    def write_gcp_key_to_local(self, gcp_key_json_string, gcp_credentials_path='temp_key.json'):
        data = json.loads(gcp_key_json_string)
        # Write the dictionary to a JSON file
        with open(gcp_credentials_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        return gcp_credentials_path

    def gcp_bucket_connetion(self, gcp_credentials_path, gcp_bucket_name):
        gcp_storage_client = storage.Client.from_service_account_json(gcp_credentials_path)
        gcp_bucket = gcp_storage_client.bucket(gcp_bucket_name)
        return gcp_bucket

    def upload_file_to_gcs(self, source_file_path, gcp_blob_name, gcp_bucket):
        gcp_blob = gcp_bucket.blob(gcp_blob_name)
        gcp_blob.upload_from_filename(source_file_path)

    # Recursively list files from a given directory path, with optional file extension filtering
    def directory_file_list(self, directory_path, file_extension=None):
        file_list = []

        def walk(path, base=''):
            for item in mssparkutils.fs.ls(path):
                rel_path = os.path.join(base, item.name)
                if item.isDir:
                    walk(item.path, rel_path)
                else:
                    if file_extension is None or file_extension in item.name:
                        file_list.append((item.path, rel_path))

        walk(directory_path)
        return file_list  # list of tuples (full_path, relative_path)

    # Create a clean temporary local directory
    def create_temp_directory(self, directory_name='temp_adls_storage'):
        directory_path = os.path.join(os.getcwd(), directory_name)
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)
        os.makedirs(directory_path)
        return directory_path

    # Copy a single file to local and upload to GCP
    def copy_and_upload_file(self, adls_path, relative_path, local_base_dir, gcp_bucket, keep_local_file=False):
        local_file_path = os.path.join(local_base_dir, relative_path)
        local_dir = os.path.dirname(local_file_path)
        os.makedirs(local_dir, exist_ok=True)


        mssparkutils.fs.cp(adls_path, f"file:{local_file_path}")

        gcp_blob_name = relative_path.replace('\\', '/')  # Unix-style
        self.upload_file_to_gcs(local_file_path, gcp_blob_name, gcp_bucket)
        logger.info(f'{relative_path} copied to GCP bucket')

        # Delete local file if flag is False
        if not keep_local_file:
            os.remove(local_file_path)

    def _process(self):
        logger.info("Custom node process started")

        logger.info("Step 1: Fetch GCP credentials")
        gcp_key_json_str = os.environ['GCP_KEY_JSON_STR']
        gcp_credentials_path = self.write_gcp_key_to_local(gcp_key_json_str)

        logger.info("Step 2: Establish GCP connection")
        gcp_bucket_name = os.environ['GCP_BUCKET_NAME']
        gcp_bucket = self.gcp_bucket_connetion(gcp_credentials_path, gcp_bucket_name)

        logger.info("Step 3: Set source (ADLS) and destination (local temp)")
        source_directory_path = os.environ['SOURCE_PATH']
        file_extension = os.environ.get('FILE_EXTENSION', None)  # optional
        destination_path = self.create_temp_directory()

        logger.info("Step 4: List files in ADLS (recursively)")
        files = self.directory_file_list(source_directory_path, file_extension)

        logger.info("Step 5: Process each file: copy -> upload -> delete (if desired)")
        for full_path, rel_path in files:
            self.copy_and_upload_file(
                adls_path=full_path,
                relative_path=rel_path,
                local_base_dir=destination_path,
                gcp_bucket=gcp_bucket,
                keep_local_file=False  # Set to True if you want to keep the file
            )

        return None

    def process(self):
        return self._process()


