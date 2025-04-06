import io
import os
import re
import json
import logging
import tempfile
from typing import Optional
from azure.core.pipeline.policies import HttpLoggingPolicy
from subprocess import call
from pathlib import Path
from azure.storage.blob import ContainerClient
from raic.foundry.entities.manifests import DataSourceManifest

AZCOPY_PATH = os.getenv("AZCOPY_PATH", "azcopy")

blob_logger = logging.getLogger('azure.storage.blob')
blob_logger.setLevel(logging.WARNING)

http_logger = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
http_logger.setLevel(logging.WARNING)

def separate_sas_key(url: str):
    parts = url.split('?')
    return (parts[0], parts[1]) if len(parts) >= 2 else (parts[0], None)

def separate_sas_url_into_parts(url: str):
    match = re.match('(https://[0-9A-Za-z._-]*)/([0-9A-Za-z._-]*)/?([/0-9A-Za-z._-]*)\\\\?(.*)', url)
    if not match:
        return None, None, None, None
    
    return match.groups()[0], match.groups()[1], match.groups()[2], match.groups()[3]

def build_storage_uri_with_sas(blob_storage_url: str, sas_key: str):
    # Ensure there is no sas key on blob storage first
    blob_storage_url, _ = separate_sas_key(blob_storage_url)
    sas_key = sas_key.lstrip('?')
    return f"{blob_storage_url}?{sas_key}"

def build_storage_uri(account_name: str, container_name: str, sas_key: Optional[str] = None) -> str:
    domain = 'blob.core.windows.net'
    if 'azml' in account_name or 'usgv' in account_name:
        domain = 'blob.core.usgovcloudapi.net'

    blob_storage_url = f"https://{account_name}.{domain}/{container_name}"

    if sas_key is not None:
        blob_storage_url = build_storage_uri_with_sas(blob_storage_url, sas_key)

    return blob_storage_url

def download_from_storage(source_url: str, destination_folder: str | Path, recursive: bool = False) -> None:
    if recursive:
        # Ensure that folder contents, not folder itself, will be copied
        account_url, container_name, _, sas_key = separate_sas_url_into_parts(source_url)
        source_url = f'{account_url}/{container_name}/*?{sas_key}'

    status = call([
        AZCOPY_PATH,
        "cp",
        "--recursive",
        "--overwrite=false",
        "--log-level=INFO",
        source_url,
        str(destination_folder),
    ])

    if status == 1:
        raise Exception(f"Failed to perform download from blob storage location {source_url}")

def download_manifest_from_storage(data_source_id: str, container_url: str) -> DataSourceManifest | None:
    manifest_name = DataSourceManifest.get_manifest_filename(data_source_id)
    if not blob_exists(container_url, manifest_name):
        return None
    
    download_stream = download_blob_to_stream(container_url, manifest_name)
    byte_stream = io.BytesIO()
    download_stream.readinto(byte_stream)
    byte_stream.seek(0)  # Ensure we read from the beginning
    parsed_data = json.loads(byte_stream.read().decode("utf-8"))
    return DataSourceManifest(**parsed_data)


def upload_to_storage(source_folder: str | Path, destination_url: str, exclude: list[str] | None = None) -> None:
    # Ensure that folder contents, not folder itself, will be copied
    source_folder = str(source_folder)
    if not source_folder.endswith('/*'):
        source_folder = f'{source_folder}/*'

    execution_arguments = [
        AZCOPY_PATH,
        "cp",
        "--recursive",
        "--overwrite=false",
        "--log-level=INFO",
        source_folder,
        destination_url
    ]

    if exclude != None:
        execution_arguments.append(f'--exclude-path={";".join(exclude)}')

    status = call(execution_arguments)

    if status == 1:
        safe_url, _ = separate_sas_key(destination_url)
        raise Exception(f"Failed to perform upload to blob storage location {safe_url}")

def upload_to_storage_from_manifest(prepared_imagery_manifest: DataSourceManifest, destination_url: str, include_manifest_file: bool = True) -> None:
    with tempfile.NamedTemporaryFile(mode='w+t', delete=True) as tmpfile:
        for relative_path in prepared_imagery_manifest.relative_paths:
            tmpfile.write(f"{str(relative_path)}\n")

        if include_manifest_file:
            prepared_imagery_manifest.save()
            tmpfile.write(f"{prepared_imagery_manifest.get_manifest_filename()}\n")

        tmpfile.seek(0)

        execution_arguments = [
            AZCOPY_PATH,
            "cp",
            "--recursive",
            "--overwrite=false",
            "--log-level=INFO",
            f'{prepared_imagery_manifest.root_path}/*',
            destination_url,
            f"--list-of-files={tmpfile.name}"
        ]

        status = call(execution_arguments)

        if status == 1:
            safe_url, _ = separate_sas_key(destination_url)
            raise Exception(f"Failed to perform upload to blob storage location {safe_url}")

    
def list_blobs_in_container(container_url: str, blob_filter: str | None = None) -> list[str]:
    blob_count = 0
    with ContainerClient.from_container_url(container_url) as container_client:
        blob_names = []
        blob_list = container_client.list_blobs(name_starts_with=blob_filter)
        for blob in blob_list:
            if blob.size > 0:
                blob_names.append(blob.name)
                blob_count+=1
                if blob_count % 1000 == 0:
                    print(f'Blob count is {blob_count}...')
        
        print(f"Found {len(blob_names)} blobs in container: {container_client.container_name}")
        return blob_names

def blob_exists(container_url: str, blob_name: str):
    with ContainerClient.from_container_url(container_url) as container_client:
        return _blob_exists(container_client, blob_name)
 
def download_blob_to_file(container_url: str, blob_name: str, destination_file: str):
    with ContainerClient.from_container_url(container_url) as container_client:
        return _download_blob_to_file(container_client, blob_name, destination_file)
    
def download_blob_to_stream(container_url: str, blob_name: str):
    with ContainerClient.from_container_url(container_url) as container_client:
        return _download_blob_to_stream(container_client, blob_name)
    
def _blob_exists(
    container_client: ContainerClient,
    blob_name: str
) -> bool:
    blob_client = container_client.get_blob_client(blob=blob_name)
    return blob_client.exists()

def _download_blob_to_file(
    container_client: ContainerClient,
    source_blob: str,
    destination_file: str
):
    try:
        with open(destination_file, "wb") as download_file:
            download_stream = _download_blob_to_stream(container_client, source_blob)
            download_stream.readinto(download_file)
    except:
        if os.path.exists(destination_file):
            os.remove(destination_file)
        raise

def _download_blob_to_stream(
    container_client: ContainerClient,
    source_blob: str
):
    blob_client = container_client.get_blob_client(blob=source_blob)
    return blob_client.download_blob()
