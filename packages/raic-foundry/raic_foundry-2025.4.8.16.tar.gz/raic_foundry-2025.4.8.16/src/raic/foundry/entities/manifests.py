from typing import Optional
from pathlib import Path
from pydantic import BaseModel, ConfigDict


class DataSourceManifest(BaseModel):
    model_config = ConfigDict(frozen=True)

    root_path: Path
    relative_paths: list[Path]

    def save(self, destination_folder: Optional[Path] = None):
        if destination_folder is None:
            destination_folder = self.root_path
            
        manifest_file = Path(destination_folder, self.get_manifest_filename()) 
        manifest_file.write_text(self.model_dump_json(indent=2))

    @classmethod
    def load(cls, source_path: Path):
        if source_path is None:
            return None
            
        if source_path.is_dir():
            source_path = Path(source_path, cls.get_manifest_filename())

        if not source_path.exists():
            return None

        return DataSourceManifest.model_validate_json(source_path.read_text())

    @classmethod
    def get_manifest_filename(cls):
        return f'data_source_manifest.json'
