import os
import shutil
import pytest
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from azure.identity import AzureCliCredential
from azure.keyvault.secrets import SecretClient
import raic.foundry.inputs.archive as archive

# Get the directory of the current script
root_dir = Path(os.path.abspath(__file__)).parent.parent.absolute()

def test_double_unpack_via_file(setUp):
    datasources_directory = setUp
    input_path = os.path.join(datasources_directory, "trimble_3_zip/trimble_3.zip")
    _remove_files_except(input_path, "trimble_3.zip")

    source_zip_file_path = Path(input_path)
    manifest = archive.unpack(source_zip_file_path)
    assert 3 == len(manifest.relative_paths)

    manifest = archive.unpack(source_zip_file_path)
    assert 3 == len(manifest.relative_paths)

    
def test_double_unpack_via_folder(setUp):
    datasources_directory = setUp
    input_path = os.path.join(datasources_directory, "trimble_3_zip/trimble_3.zip")
    _remove_files_except(input_path, "trimble_3.zip")

    source_zip_folder_path = Path(input_path).parent
    manifest = archive.unpack(source_zip_folder_path)
    assert 3 == len(manifest.relative_paths)

    manifest = archive.unpack(source_zip_folder_path)
    assert 3 == len(manifest.relative_paths)


def test_complex_unpack(setUp):
    #
    # Test complex unpack scenarios all in one datasource
    #
    datasources_directory = setUp
    input_path = _load_test_imagery_from_scus(datasources_directory, 'monitoring-test-unpack-validation', 'unpack-validation')
    _remove_files_except(input_path, ["imageswithdoubleparens.zip", "macosx_test.tar", "multicompression.tar.gz"])

    manifest = archive.unpack(Path(input_path))
    assert 70 == len(manifest.relative_paths)


@pytest.fixture
def setUp(request: pytest.FixtureRequest):
    datasources_directory = os.path.join(str(root_dir), ".ignore/datasources")
    yield datasources_directory

    print(f'Setup for {request.node.name} complete')


def _load_test_imagery_from_scus(datasources_directory, data_source_container, destination_folder):
    imagery_datasource_folder = os.path.join(datasources_directory, destination_folder)
    account_url = "https://devstraicscussynth.blob.core.windows.net"

    if os.path.exists(imagery_datasource_folder):
        print(f'Imagery folder {imagery_datasource_folder} already exists')
    else:
        print(f'Creating service client for {account_url}...')
        secretClient = SecretClient("https://dev-kv-raic-scus-synth.vault.azure.net", AzureCliCredential())
        connection_string = secretClient.get_secret('BlobStorage--DefaultBlobStorage--ProviderOptions--ConnectionString').value
        assert connection_string is not None

        service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = service_client.get_container_client(data_source_container)

        print(f'Retrieving list of files in datasource container {data_source_container}...')
        blob_list = container_client.list_blobs()
        blob_list = [blob.name for blob in blob_list]

        print(f'There are {len(blob_list)} files in this datasource.  Let\'s download them')
        for blob_name in blob_list:
            _download_blob(container_client, blob_name, imagery_datasource_folder)

    return imagery_datasource_folder


def _download_blob(container_client, blob_name, imagery_datasource_folder):
    blob_client = container_client.get_blob_client(blob_name)
    local_file_path = os.path.join(imagery_datasource_folder, blob_name)

    if not os.path.exists(os.path.dirname(local_file_path)):
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

    print(f'Downloading {local_file_path}...')
    with open(local_file_path, "wb") as local_file:
        download_stream = blob_client.download_blob(max_concurrency=4)
        download_stream.readinto(local_file)


def _remove_files_except(directory, keep_files):
    if os.path.isfile(directory):
        directory = os.path.dirname(directory)

    for file_or_folder_name in os.listdir(directory):
        filepath = os.path.join(directory, file_or_folder_name)

        if os.path.isfile(filepath) and file_or_folder_name not in keep_files:
            os.remove(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath)

