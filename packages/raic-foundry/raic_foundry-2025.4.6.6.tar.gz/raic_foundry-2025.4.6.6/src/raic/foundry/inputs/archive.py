import patoolib
from pathlib import Path
from ..entities.manifests import DataSourceManifest
from .manifest import load_datasource_manifest_from_folder, save_datasource_manifest

def unpack(source_path: Path) -> DataSourceManifest:
    manifest = load_datasource_manifest_from_folder(source_path)
    if manifest is not None:
        return manifest
    else:
        if source_path.is_dir():
            root_path = source_path
            paths = [path for path in source_path.rglob("*.*")]
        elif source_path.is_file():
            root_path = source_path.parent
            paths = [source_path]
        else:
            raise Exception(f"{source_path} is not a valid data source path.")
        
        archive_files = [path for path in paths if _is_supported_archive(path)]
        extracted_files = []

        # keep the extract path simple if there is only a single archive file involved
        if len(paths) == 1 and len(archive_files) == 1:
            extracted_files.extend(extract_archive(archive_files[0], root_path, extract_into_folder=False))
            paths.remove(archive_files[0])
        else:
            for archive_file in archive_files:
                extracted_files.extend(extract_archive(archive_file, Path(archive_file.parent)))
                paths.remove(archive_file)

        paths.extend(extracted_files)

        paths = [p for p in paths if p.suffix != '.Identifier']

        return DataSourceManifest(root_path=root_path, relative_paths=[path.relative_to(root_path) for path in paths])


def extract_archive(archive_path: Path, output_dir: Path, extract_into_folder: bool = True) -> list[Path]:
    destination_folder = Path(output_dir, archive_path.stem) if extract_into_folder else Path(output_dir)
    destination_folder = Path(patoolib.extract_archive(str(archive_path), outdir=str(destination_folder)))
    return [path for path in destination_folder.rglob("*.*") if path.is_file() and path != archive_path]


def _is_supported_archive(path: Path):
    for suffix in path.suffixes:
        if suffix.lstrip('.') in patoolib.supported_formats(['extract']):
            return True
        
    return False