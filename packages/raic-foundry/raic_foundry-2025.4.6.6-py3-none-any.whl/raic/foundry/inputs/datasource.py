from typing import Optional
from pathlib import Path
import raic.foundry.shared.azure
import raic.foundry.inputs.image
import raic.foundry.inputs.archive
import raic.foundry.inputs.exif
import raic.foundry.inputs.geospatial
import raic.foundry.shared.utils
from raic.foundry.entities.artifacts import ImageArtifact, ImageInfo
from raic.foundry.entities.manifests import DataSourceManifest

def list_images_in_datasource(container_url: str, blob_filter: str | None = None):
    print(f'Gathering list of all blobs available in container...')
    return raic.foundry.shared.azure.list_blobs_in_container(container_url, blob_filter)


def load_image_from_datasource(container_url: str, blob_name, local_path: Path | None = None, keep_image_open: bool = True):
    image = None
    try:
        image_url = f'{container_url}{blob_name}'
        if local_path is not None and Path(local_path, blob_name).exists():
            local_file_path = Path(local_path, blob_name)
            image = raic.foundry.inputs.image._lazyload_image(local_file_path)
            if image is None:
                print(f'Skipping {blob_name}, not an image file')
                return None
            print(f'Found {blob_name} locally, no need to re-download')
        else:
            print(f'Downloading datasource image {blob_name}...')
            image, local_file_path = raic.foundry.inputs.image._download_image(container_url, blob_name, local_path)
            if image is None:
                print(f'Skipping {blob_name}, either failed to download or not an image file')
                return None

        geospatial_info = raic.foundry.inputs.geospatial.get_info(local_file_path)
        image_artifact = ImageArtifact(
            info = ImageInfo(
                name=Path(blob_name).name,
                relative_path=Path(blob_name),
                local_path=local_file_path,
                url=image_url,
                width=image.width,
                height=image.height,
                collected_on=geospatial_info.collected_on if geospatial_info is not None and geospatial_info.collected_on is not None else raic.foundry.inputs.exif.get_datetime(image),
                geospatial=geospatial_info,
                sequence_number=None
            ),
            image=image        
        )
    finally:
        if image is not None and not keep_image_open:
            image.close() # in case the image was not yet assigned to the artifact, explicitly close the image object
            image_artifact.close_image()

    return image_artifact


def load_from_datasource(container_url: str, blob_filter: str | None = None, local_path: Path | None = None, assign_sequence_number: bool = False, keep_image_open: bool = True):
    print(f'Gathering list of all blobs available in container...')
    blob_names = raic.foundry.shared.azure.list_blobs_in_container(container_url, blob_filter)

    sequence_number = 1
    for blob_name in blob_names:
        image_artifact = load_image_from_datasource(container_url, blob_name, local_path, keep_image_open)
        if image_artifact is None:
            continue
        
        image_artifact.info.sequence_number = sequence_number
        yield image_artifact


def load_from_local_folder(source_path: Path | list[Path], root_path: Path, assign_sequence_number: bool = False, keep_image_open: bool = True):
    sequence_number = 1
    for file_path in raic.foundry.shared.utils.list_files_in_folder(source_path):
        artifact = load_from_local_file(file_path=file_path, root_path=root_path, sequence_number=sequence_number if assign_sequence_number else None, keep_image_open=keep_image_open)
        if artifact is None:
            continue

        sequence_number = sequence_number + 1
        yield artifact


def load_from_local_file(file_path: Path, root_path: Path, sequence_number: int | None = None, keep_image_open: bool = True):
    image_artifact = raic.foundry.inputs.image.load_from_local_file(file_path, root_path, sequence_number, keep_image_open)
    if image_artifact != None:
        image_artifact.info.geospatial=raic.foundry.inputs.geospatial.get_info(file_path)

    if image_artifact.info.geospatial is not None and image_artifact.info.geospatial.collected_on is not None:
        image_artifact.info.collected_on = image_artifact.info.geospatial.collected_on

    return image_artifact


def prepare(source_path: Path,
    max_size_px: int = 9792
) -> DataSourceManifest:
    archive_manifest = raic.foundry.inputs.archive.unpack(source_path)
    root_path = archive_manifest.root_path
    available_relative_file_paths = archive_manifest.relative_paths

    unpacked_relative_file_paths = []
    for file_path in [Path(root_path, relative_file_path) for relative_file_path in available_relative_file_paths]:
        processed = False
        for geospatial_file_path in raic.foundry.inputs.geospatial.prepare(file_path, root_path, max_size_px):
            unpacked_relative_file_paths.append(geospatial_file_path)
            processed = True

        if processed:
            continue

        # TODO: video.load_from_local_file(data_source_file, data_source_root_path)

        if processed:
            continue

        image_artifact = load_from_local_file(file_path, root_path)
        if image_artifact is not None:
            unpacked_relative_file_paths.append(image_artifact.info.local_path.relative_to(root_path))
        else:
            print(f'Data source file {file_path.name} not recognized as valid image type')

    manifest = DataSourceManifest(root_path=root_path, relative_paths=[relative_file_path for relative_file_path in unpacked_relative_file_paths])
    manifest.save()
    return manifest
