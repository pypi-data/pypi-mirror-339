import os
import shutil
import pytest
import random
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from azure.identity import AzureCliCredential
from azure.keyvault.secrets import SecretClient

import raic.foundry.shared.azure
from raic.foundry.client.context import login_if_not_already
from raic.foundry.datasources import Datasource

# Get the directory of the current script
root_dir = Path(os.path.abspath(__file__)).parent.parent.absolute()

def test_new_from_local_folder_prepare_upload(setUp):
    test_name, _, datasources_directory, _ = setUp
    input_path = _load_test_imagery_from_scus(datasources_directory, 'foundry-test-zip', 'test_zip')
    _remove_files_except(input_path, "upload.zip")

    try:
        # Act
        result = Datasource.new_from_local_folder(f'Integration Test {test_name}', input_path)

        # Assert
        _assert_blob_exists(result, 'trimble_3/pano_000002_001193.jpg')
        _assert_blob_exists(result, 'trimble_3/pano_000002_001194.jpg')
        _assert_blob_exists(result, 'trimble_3/pano_000002_001195.jpg')
        _assert_blob_exists(result, 'data_source_manifest.json')
    finally:
        if 'result' in locals() and result is not None:
            # Cleanup Data Source
            result.delete()

def test_new_from_local_folder_no_prepare_upload(setUp):
    test_name, _, datasources_directory, _ = setUp
    input_path = _load_test_imagery_from_scus(datasources_directory, 'foundry-test-zip', 'test_zip')
    _remove_files_except(input_path, "upload.zip")

    try:
        # Act
        result = Datasource.new_from_local_folder(f'Integration Test {test_name}', input_path, prepare_imagery=False)

        # Assert
        _assert_blob_exists(result, 'upload.zip')
    finally:
        if 'result' in locals() and result is not None:
            # Cleanup Data Source
            result.delete()

def test_from_existing_by_id(setUp):
    test_name, _, datasources_directory, _ = setUp
    input_path = _load_test_imagery_from_scus(datasources_directory, 'foundry-test-geotiff', 'test_geotiff')

    try:
        # Arrange
        data_source_name = f'Integration Test {test_name}_datasource_{random.randint(1, 100)}'
        data_source = Datasource.new_from_local_folder(data_source_name, input_path)
        existing_data_source_id = data_source.datasource_id

        # Act
        result = Datasource.from_existing(existing_data_source_id)

        # Assert
        assert result.datasource_id == data_source.datasource_id
        assert result._record['name'] == data_source_name
    finally:
        if 'result' in locals() and result is not None:
            # Cleanup Data Source
            result.delete()

def test_from_existing_by_name(setUp):
    test_name, _, datasources_directory, _ = setUp
    input_path = _load_test_imagery_from_scus(datasources_directory, 'foundry-test-geotiff', 'test_geotiff')

    try:
        # Arrange
        data_source_name = f'Integration Test {test_name}_datasource_{random.randint(1, 100)}'
        data_source = Datasource.new_from_local_folder(data_source_name, input_path)

        # Act
        result = Datasource.from_existing(data_source_name)

        # Assert
        assert result.datasource_id == data_source.datasource_id
        assert result._record['name'] == data_source_name
    finally:
        if 'result' in locals() and result is not None:
            # Cleanup Data Source
            result.delete()

@pytest.fixture
def setUp(request: pytest.FixtureRequest):
    test_name = request.node.name
    workspace_directory = os.path.join(str(root_dir), ".ignore")
    datasources_directory = os.path.join(str(root_dir), ".ignore/datasources")
    output_directory = Path(workspace_directory, 'test', test_name)

    # Clear previous run output
    if output_directory.is_dir():
        print(f'Cleaning up any previous runs of {test_name} before starting...')
        shutil.rmtree(str(output_directory))

    # Ensure logged in
    login_if_not_already()

    print(f'Setup for {test_name} complete')
    yield test_name, workspace_directory, datasources_directory, output_directory


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


def _assert_blob_exists(data_source, blob_name):
    container_url = data_source.get_blob_storage_container_url()
    assert raic.foundry.shared.azure.blob_exists(container_url, blob_name) == True, f'Blob {blob_name} not found in data source {data_source._record['name']} ({data_source.datasource_id})'


def _remove_files_except(directory, keep_files):
    if os.path.isfile(directory):
        directory = os.path.dirname(directory)

    for file_or_folder_name in os.listdir(directory):
        filepath = os.path.join(directory, file_or_folder_name)

        if os.path.isfile(filepath) and file_or_folder_name not in keep_files:
            os.remove(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath)

