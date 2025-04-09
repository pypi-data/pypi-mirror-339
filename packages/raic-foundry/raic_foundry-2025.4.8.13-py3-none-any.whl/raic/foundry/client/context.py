from pathlib import Path
from typing import Optional
from .environment import EnvironmentEnum
from .raic_configuration import RaicConfiguration
from .raic_authenticator import RaicAuthenticator


_root_workspace: Path | None = None
_raic_configuration: RaicConfiguration | None = None
_raic_auth: RaicAuthenticator | None = None
_datasource = None


def login_if_not_already(workspace: Path | str = '.', environment: EnvironmentEnum = EnvironmentEnum.Prod):
    global _root_workspace, _raic_configuration, _raic_auth
    if isinstance(workspace, str):
        workspace = Path(workspace)

    _root_workspace = workspace
    _raic_configuration = RaicConfiguration(environment)
    _raic_auth = RaicAuthenticator(_raic_configuration.get_configuration())
    _raic_auth.login_if_not_already()


def get_workspace() -> Path:
    global _root_workspace, _raic_configuration, _raic_auth
    if _root_workspace is None:
        raise Exception("No workspace specified.  Please set workspace before proceeding")
    
    return _root_workspace


def set_environment(environment: EnvironmentEnum):
    global _raic_configuration, _raic_auth
    if _raic_configuration is not None:
        if _raic_configuration.get_environment() != environment and _raic_auth is not None:
            _raic_auth.clear_login()

        _raic_configuration.set_environment(environment)
    else:
        _raic_configuration = RaicConfiguration(environment)

    _raic_auth = RaicAuthenticator(_raic_configuration.get_configuration())


def set_datasource(datasource):
    global _datasource
    _datasource = datasource


def get_datasource():
    global _datasource
    return _datasource


def get_environment() -> EnvironmentEnum:
    global _raic_configuration, _raic_auth
    if _raic_configuration is None:
        return EnvironmentEnum.Unspecified
    
    return _raic_configuration.get_environment()


def get_organization_id() -> str:
    global _raic_configuration, _raic_auth
    if _raic_configuration is None:
        raise Exception("Not environment specified")
    
    assert _raic_auth is not None, \
        "RaicAuthenticator not initialized"
    
    return _raic_auth.get_org_id()


def get_username() -> str | None:
    global _raic_configuration, _raic_auth
    if _raic_configuration is None:
        raise Exception("Not environment specified")
    
    assert _raic_auth is not None, \
        "RaicAuthenticator not initialized"
    
    user = _raic_auth.get_user()
    return user['name'] if user is not None else None


def get_raic_auth() -> RaicAuthenticator:
    global _raic_configuration, _raic_auth
    if _raic_configuration is None:
        raise Exception("Not environment specified")
    
    assert _raic_auth is not None, \
        "RaicAuthenticator not initialized"
     
    return _raic_auth


def get_raic_configuration(key: str) -> str:
    global _raic_configuration
    if _raic_configuration is None:
        raise Exception("Not environment specified")
     
    return _raic_configuration.get_configuration()[key]

