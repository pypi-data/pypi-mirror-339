import os
import shutil
import pytest
from pathlib import Path
import raic.foundry.inputs.geospatial
import raic.foundry.inputs.image
import raic.foundry.inputs.datasource
from azure.storage.blob import BlobServiceClient
from azure.identity import AzureCliCredential
from azure.keyvault.secrets import SecretClient

# Get the directory of the current script
root_dir = Path(os.path.abspath(__file__)).parent.parent.absolute()


def test_nir_geotiff(setUp):
    workspace_directory, datasources_directory, inference_run_directory = setUp
    input_path = _load_test_imagery_from_scus(datasources_directory, 'monitoring-test-nir-geotiff', 'nir_geotiff')
    image_artifact_generator = raic.foundry.inputs.datasource.load_from_local_folder(input_path, input_path, keep_image_open=False)
    for image in image_artifact_generator:
        print(image)

    assert None is None


def test_cjymtk_jpg(setUp):
    workspace_directory, datasources_directory, inference_run_directory = setUp
    input_path = _load_test_imagery_from_scus(datasources_directory, 'monitoring-test-cymk', 'cmyk_jpg')
    image_artifact_generator = raic.foundry.inputs.datasource.load_from_local_folder(input_path, input_path, keep_image_open=False)
    for image in image_artifact_generator:
        print(image)

    assert None is None


def test_prepare(setUp):
    workspace_directory, datasources_directory, inference_run_directory = setUp
    input_path = _load_test_imagery_from_scus(datasources_directory, 'monitoring-test-cymk', 'cmyk_jpg')
    image_artifact_generator = raic.foundry.inputs.geospatial.tile_raster(input_path, input_path)
    for image in image_artifact_generator:
        print(image)

    assert None is None


@pytest.fixture
def setUp(request: pytest.FixtureRequest):
    workspace_directory = os.path.join(str(root_dir), ".ignore")
    datasources_directory = os.path.join(str(root_dir), ".ignore/datasources")
    inference_run_directory = Path(workspace_directory, 'runs', request.node.name)

    # Clear previous run output
    if inference_run_directory.is_dir():
        print(f'Cleaning up any previous runs of {request.node.name} before starting...')
        shutil.rmtree(str(inference_run_directory))

    print(f'Setup for {request.node.name} complete')
    yield workspace_directory, datasources_directory, inference_run_directory


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

