import os
import json
from typing import Optional
from pathlib import Path
from .environment import EnvironmentEnum

context_root_dir = Path(os.path.abspath(__file__)).parent.parent.absolute()

class RaicConfiguration:
    LOCAL_APP_FOLDER = '.raic-foundry'

    def __init__(self, environment: EnvironmentEnum, local_auth_storage_override: Optional[Path] = None):
        self._local_auth_storage_override = local_auth_storage_override
       
        configuration_location_override = os.environ.get('RAIC_ENVIRONMENTS', '')
        if configuration_location_override is not None and configuration_location_override != '':
            self._environments_configuration_file_path = Path(configuration_location_override)
        else:
            self._environments_configuration_file_path = Path(Path(os.path.abspath(__file__)).parent.parent.absolute(), 'configuration', 'raic-configuration.json')
        
        self._env = None
        self._envFile = self._get_local_env_file()
        self.set_environment(environment)

    def set_environment(self, environment: EnvironmentEnum):
        all_environments = json.loads(self._environments_configuration_file_path.read_text())

        if environment.name.lower() not in all_environments:
            raise Exception(f"Environment {environment} is not recognized")
        
        if self._envFile.exists() and self._env is not None and 'name' in self._env:
            if self._env['name'] == environment.name.lower():
                return
            
            environment_name = json.loads(self._envFile.read_text())['name'].lower()
            self._env = all_environments[environment_name]
        else:
            self._env = all_environments[environment.name.lower()]
            self._envFile.write_text(json.dumps({ "name": self._env['name']}))

    def get_environment(self):
        environment_string = self._env['name'].lower()
        if environment_string == 'dev':
            environment = EnvironmentEnum.Dev
        elif environment_string == 'qa':
            environment = EnvironmentEnum.QA
        elif environment_string == 'prod' or environment_string == 'prd':
            environment = EnvironmentEnum.Prod
        else:
            raise Exception(f"Environment {environment_string} is not recognized")
        
        return environment
    
    def get_configuration(self):
        return self._env

    def _get_local_env_file(self) -> Path:
        return Path(self._get_userdata_path(), "raic-env")
    
    def _get_userdata_path(self) -> Path:
        if self._local_auth_storage_override is not None:
            config_dir = Path(self._local_auth_storage_override)
        elif os.name == 'nt':
            # Windows
            config_dir = Path(Path(os.environ['LOCALAPPDATA']), self.LOCAL_APP_FOLDER)
        elif os.name == 'posix':
            # macOS and Linux
            config_dir = Path(Path.home(), self.LOCAL_APP_FOLDER)
        else:
            raise OSError(f"Unsupported operating system '{os.name}' found when storing raic-foundry configuration")
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
