from setuptools import setup, find_packages

setup(
    name='datapipelabcustomprocessor',
    version='0.1.4',
    description='A data pipeline custom processor node.',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'json5',
        'loguru',
        'azure-storage-blob',
        'google-cloud-storage',
        'pandas'
    ],
)