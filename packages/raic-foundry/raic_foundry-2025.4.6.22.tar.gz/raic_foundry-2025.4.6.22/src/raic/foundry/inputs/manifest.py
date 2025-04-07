

from pathlib import Path
from ..entities.manifests import DataSourceManifest
import raic.foundry.client.datasource
from raic.foundry.shared.azure import build_storage_uri, download_from_storage
from raic.foundry.shared.utils import is_guid


DATASOURCE_MANIFEST_FILENAME = "datasource_manifest.json"

def load_datasource_manifest_from_folder(folder_path: Path) -> DataSourceManifest | None:
    """
    Load a datasource manifest from a specified folder.
    Searches for manifest files within the folder. If more than one manifest file is found, an exception is raised.
    If no manifest files are found, the function returns None. Otherwise, it loads the manifest from the found file.
    Args:
        folder_path (Path): The path to the folder containing the datasource manifest.
    Returns:
        DataSourceManifest | None: The loaded datasource manifest if found, otherwise None.
    Raises:
        Exception: If more than one datasource manifest file is found in the folder.
    """
    
    if folder_path.is_file():
        folder_path = folder_path.parent

    manifest_files = list(folder_path.glob(DATASOURCE_MANIFEST_FILENAME))
    if len(manifest_files) > 1:
        raise Exception(f"More than one datasource manifest exists in {folder_path}, cannot continue")
    elif len(manifest_files) == 0:
        return None
    
    manifest_file = manifest_files[0]

    return load_datasource_manifest_from_file(manifest_file)


def load_datasource_manifest_from_file(file_path: Path) -> DataSourceManifest:
    return DataSourceManifest.model_validate_json(file_path.read_text())


def save_datasource_manifest(folder_path: Path, manifest: DataSourceManifest):
    manifest_files = list(folder_path.glob(DATASOURCE_MANIFEST_FILENAME))
    if len(manifest_files) > 1:
        raise Exception(f"More than one datasource manifest exists in {folder_path}, cannot continue")

    manifest_file = Path(folder_path, DATASOURCE_MANIFEST_FILENAME) 
    manifest_file.write_text(manifest.model_dump_json(indent=2))


def get_datasource_manifest(
    destination_folder: Path,
    datasource_id: str | None,
) -> DataSourceManifest | None:
    """
    Retrieves the datasource manifest either from a local folder or by downloading it from a remote storage.
    Args:
        destination_folder (Path): The local folder where the datasource manifest is stored or will be downloaded to.
        datasource_id (str | None): The unique identifier of the datasource. Used to download the datasource manifest if it does not exist locally.
    Returns:
        DataSourceManifest: The datasource manifest object.
    Raises:
        ValueError: If the datasource_id is not a valid GUID.
        Exception: If there is an error during the download or loading process.
    """
    # if manifest file exists locally, load it
    local_datasource_manifest = load_datasource_manifest_from_folder(destination_folder)
    if local_datasource_manifest is not None:
        return local_datasource_manifest
    # if manifest file does not exist locally, download it
    else:
        if datasource_id is not None:
            if isinstance(datasource_id, str) and is_guid(datasource_id):
                datasource_json = raic.foundry.client.datasource.get_datasource(datasource_id)
                if datasource_json is not None:
                    datasource_manifest_url = build_storage_uri(datasource_json['storageAccountUrl'], f"{datasource_json['storageAccountContainer']}/{DATASOURCE_MANIFEST_FILENAME}", datasource_json['storageAccountSasToken'])
                    download_from_storage(
                        source_url=datasource_manifest_url,
                        destination_folder=destination_folder
                    )

                    return load_datasource_manifest_from_folder(destination_folder)

    raise Exception(f"Failed to retrieve datasource manifest for datasource_id: {datasource_id}")