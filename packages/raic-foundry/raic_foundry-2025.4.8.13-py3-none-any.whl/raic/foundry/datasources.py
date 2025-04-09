"""
Data source to use as an input to an inference run

Here are some quickstart examples. Make sure to first login to Raic Foundry

.. code-block:: python

    from raic.foundry.client.context import login_if_not_already

    # Login to Raic Foundry (prompted on the command line)
    login_if_not_already()


Example: Create new data source from local imagery

.. code-block:: python

    from raic.foundry.datasources import Datasource

    # Create data source record and upload imagery
    name = 'My New Data Source'
    local_path = '[Local Imagery]'
    data_source = Datasource.new_from_local_folder(name, local_path)
    print(data_source)

Example: Look up existing data source by name

.. code-block:: python

    from raic.foundry.datasources import Datasource

    # Look up existing data source record
    name = 'My Existing Data Source'
    data_source = Datasource.from_existing(name)
    print(data_source)
 
Example: Look up existing data source by UUID

.. code-block:: python

    from raic.foundry.datasources import Datasource

    # Look up existing data source record
    id = '72350d6d-65b6-4742-a8e0-4753ae92d0e2'
    data_source = Datasource.from_existing(id)
    print(data_source)   

"""
import json
import uuid
from pathlib import Path
from typing import Optional, Any
from raic.foundry.client.datasource import DataSourceClient
import raic.foundry.inputs
import raic.foundry.shared.azure
import raic.foundry.inputs.datasource
from raic.foundry.entities.manifests import DataSourceManifest
from raic.foundry.cli.console import clear_console

class Datasource():
    def __init__(self, datasource_id: str, record: dict, local_path: Optional[Path] = None, needs_upload: Optional[bool] = False):
        """Create a representation of a data source to use as an input to an inference run

        Args:
            datasource_id (str): UUID of the datasource
            record (dict): Datasource record from API
        """
        self.datasource_id = datasource_id
        self._record = record
        self._local_path = local_path
        self._needs_upload = needs_upload

    def get_blob_storage_container_url(self) -> str:
        account_name = self._record['storageAccountName']
        container_name = self._record['storageAccountContainer']
        sas_key = self._record['storageAccountSasToken']
        return raic.foundry.shared.azure.build_storage_uri(account_name, container_name, sas_key)

    def prepare(self):
        """Search the local folder for usable imagery files.  
        
        PLEASE NOTE: this may require more than twice the original disk space as the original imagery
        
        For each found the following transformations will be made:
        1) Archive files (.zip, .tar, .bz2, .gz, .xz) will be unpacked
        2) Geospatial raster files (all single-file formats supported by gdal, multifile not yet supported) will be transformed to EPSG:4326 geotiff (.tif)
        3) Geotiff (.tif) files larger than 9792px in width or height will be separated into smaller tiles of 9792px
        4) Imagery formats (.jpg, .png, .bmp, .gif) are read and left unchanged

        Raises:
            Exception: If local folder does not exist
            Exception: If local folder contains not files
        """
        if self._local_path is None:
            print('Data source does not have a local path')
            return
        
        manifest = DataSourceManifest.load(self._local_path)
        if manifest is not None:
            return manifest
        
        return raic.foundry.inputs.datasource.prepare(self._local_path)

    def upload(self):
        """If this datasource is newly created from local imagery, upload to the data source blob storage

        Raises:
            Exception: If local folder does not exist
            Exception: If local folder contains not files
        """
        if self._local_path is None:
            raise Exception(f"Cannot upload datasource image, no local source path specified")
        elif not self._local_path.exists():
            raise Exception(f"Cannot upload datasource image, local source path doesn't exist")
        elif not self._has_files(self._local_path):
            raise Exception(f"Cannot upload datasource image, local source path is empty")
        
        if not self._needs_upload:
            print('Data source already uploaded')
            return
                       
        datasource_uri = raic.foundry.shared.azure.build_storage_uri(self._record['storageAccountName'], self._record['storageAccountContainer'], self._record['storageAccountSasToken'])

        manifest = DataSourceManifest.load(self._local_path)
        if manifest is not None:
            raic.foundry.shared.azure.upload_to_storage_from_manifest(manifest, datasource_uri)
        else:
            raic.foundry.shared.azure.upload_to_storage(self._local_path, datasource_uri)

        self._needs_upload = False

    def delete(self):
        DataSourceClient().delete_datasource(self.datasource_id)
    
    @classmethod
    def from_existing(cls, identifier: str) -> 'Datasource':
        """Look up an existing data source by its UUID or its name
        Note: If there are multiple datasources with the same name looking up by name will fail with an Exception

        Args:
            identifier (str): Either the UUID of the datasource or its name

        Raises:
            Exception: If multiple datasources are returned with the same name

        Returns:
            Datasource
        """
        if cls._is_uuid(identifier):
            datasource_record = DataSourceClient().get_datasource(identifier)
        else:
            response = DataSourceClient().find_datasources_by_name(identifier)
            if len(response['value']) == 0 or len(response['value']) > 1:
                raise Exception(f"{len(response['value'])} datasources are named '{identifier}'")
            
            datasource_record = response['value'][0]

        return Datasource(datasource_id=datasource_record['id'], record=datasource_record, needs_upload=False)

    @classmethod
    def new_from_local_folder(cls, name: str, local_path: Path | str, prepare_imagery: bool = True, upload_imagery: bool = True) -> 'Datasource':
        """Create new data source from local imagery
        If prepare_imagery is set to True (default) then the local folder will be searched for usable imagery files.  
        
        PLEASE NOTE: this may require more than twice the original disk space as the original imagery
        
        For each found the following transformations will be made:
        1) Archive files (.zip, .tar, .bz2, .gz, .xz) will be unpacked
        2) Geospatial raster files (all single-file formats supported by gdal, multifile not yet supported) will be transformed to EPSG:4326 geotiff (.tif)
        3) Geotiff (.tif) files larger than 9792px in width or height will be separated into smaller tiles of 9792px
        4) Imagery formats (.jpg, .png, .bmp, .gif) are read and left unchanged

        Args:
            name (str): Desired name of the new data source
            local_path (Path | str): Local path contains imagery to upload to data source (aka blob storage container)
            prepare_imagery (bool, optional): Whether to transform imagery in the local folder. Defaults to True.

        Raises:
            Exception: If local folder does not exist
            Exception: If local folder contains not files

        Returns:
            Datasource
        """
        local_path = Path(local_path)
        if not local_path.exists():
            raise Exception(f"Cannot create datasource from a local source folder that doesn't exist")
        elif not cls._has_files(local_path):
            raise Exception(f"Cannot create datasource from a local source folder without imagery")
        
        datasource_record = DataSourceClient().create_datasource(name)
        data_source = Datasource(datasource_id=datasource_record['id'], record=datasource_record, local_path=local_path, needs_upload=True)
        if prepare_imagery:
            data_source.prepare()

        if upload_imagery:
            data_source.upload()

        return data_source

    @classmethod
    def from_prompt(cls, prepare_imagery: bool = True, upload_imagery: bool = True) -> 'Datasource':
        datasource_selected = False
        while not datasource_selected:
            clear_console()
            print(f"\nWhere do you want to source imagery from?")
            print(f" 1. Look up an existing datasource")
            print(f" 2. Create a new one from local workspace")
            selection = input("[1]: ")
            print()
            if not bool(selection) or selection == '1':
                count = 10
                skip = 0
                existing_datasources = []
                selection = None

                while not bool(selection) or not selection.isnumeric():
                    datasources_page = DataSourceClient().get_recent_datasources(top=count, skip=skip)
                    existing_datasources.extend(datasources_page)
                    for index, datasource in enumerate(datasources_page):
                        print(f'{skip + index + 1}. {datasource['name']}')

                    if len(datasources_page) > 0:
                        selection = input("Select datasource [more]: ")
                    else:
                        selection = input("Select datasource (that's all): ")

                    print()
                    skip += count
                
                datasource_selected = True
                return cls.from_existing(existing_datasources[int(selection) - 1]['id'])

            elif selection == '2':
                subfolders = []
                datasources_folder = Path('datasources')
                datasources_folder.mkdir(exist_ok=True)

                for entry in datasources_folder.iterdir():
                    if entry.is_dir():
                        subfolders.append(entry)

                for index, path in enumerate(subfolders):
                    print(f'{index + 1}. {path.name}')

                selection = None
                while not bool(selection) or not selection.isnumeric():
                    selection = input("Select datasource folder: ")
                    print()

                datasource_selected = True
                data_source_name = input("Datasource name? ")
                local_datasource_folder = subfolders[int(selection) - 1]
                return cls.new_from_local_folder(name=data_source_name, local_path=local_datasource_folder, prepare_imagery=prepare_imagery, upload_imagery=upload_imagery)
            
        raise ValueError(f"Invalid selection: {selection}. Please select either 1 or 2.")

    @classmethod
    def _has_files(cls, folder_path: Path):
        if not folder_path.is_dir():
            return False  # Not a directory

        # Check if there's at least one file within the folder
        return any(folder_path.iterdir())

    @classmethod
    def _is_uuid(cls, uuid_to_test: str, version=4) -> bool:
        try:
            uuid.UUID(uuid_to_test, version=version)
            return True
        except ValueError:
            return False
