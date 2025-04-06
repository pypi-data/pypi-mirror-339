import os
import time
from typing import Optional
from datetime import datetime, timedelta

from auth0.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier
import jwt
import requests
import json
from pathlib import Path


class RaicAuthenticator:
    LOCAL_APP_FOLDER = '.raic-foundry'

    def __init__(self, configuration: dict[str, str], local_auth_storage_override: Optional[Path] = None):
        self._local_auth_storage_override = local_auth_storage_override
        self.current_user = None
        self.access_token = None
        self._expiration_datetime = None
        self.org_id = None
        self.configuration = configuration

        authFile = self._get_local_auth_file()

        if authFile.exists() and authFile.is_file():
            token_data = json.loads(authFile.read_text())

            # validate environment configuration
            if 'name' not in self.configuration:
                raise Exception(f'No environment configuration is specified please set up your environment before initializing raic authentication')
            elif 'AuthZeroAlgorithms' not in self.configuration:
                raise Exception(f'It looks like the environment {self.configuration['name']} configuration is not complete.  Could this be because you have isolated_mode set to True?')

            exp = jwt.decode(token_data['access_token'], algorithms=self.configuration['AuthZeroAlgorithms'], options={"verify_signature": False})['exp']
            if exp > time.time():
                self.access_token = token_data['access_token']
                self._expiration_datetime = datetime.now() + timedelta(seconds=exp-time.time())
                self.current_user = jwt.decode(token_data['id_token'], algorithms=self.configuration['AuthZeroAlgorithms'], options={"verify_signature": False})
                self.org_id = self.current_user['https://api.raic.ai/organization'] 

    def clear_login(self):
        authFile = self._get_local_auth_file()
        if authFile.exists():
            os.remove(str(authFile))

    def login(self):
        device_code_payload = {
            'client_id': self.configuration['AuthZeroV2ClientId'],
            'scope': 'openid profile',
            'audience': self.configuration['AuthZeroAudience']
        }
        device_code_response = requests.post('https://{}/oauth/device/code'.format(self.configuration['AuthZeroTenantName']), data=device_code_payload)

        if device_code_response.status_code != 200:
            print(f'Error generating the device code. Status Code: {device_code_response.status_code}, Reason: {device_code_response.reason}')
            print(f'Text: {device_code_response.text}')
            raise Exception(f'Error generating the device code. Status Code: {device_code_response.status_code}, Reason: {device_code_response.reason}')

        print()
        print(f'Authenticating to the RAIC {self.configuration['name'].upper()} environment...')
        device_code_data = device_code_response.json()
        print('On your computer or mobile device navigate to: ', device_code_data['verification_uri_complete'])
        print('  Enter the following code: ', device_code_data['user_code'])
        print()

        token_payload = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            'device_code': device_code_data['device_code'],
            'client_id': self.configuration['AuthZeroV2ClientId'],
            'audience': self.configuration['AuthZeroAudience']
        }

        authenticated = False
        while not authenticated:

            token_response = requests.post('https://{}/oauth/token'.format(self.configuration['AuthZeroTenantName']), data=token_payload)

            token_data = token_response.json()

            if token_response.status_code == 200:
                self.access_token = token_data['access_token']
                self._validate_token(token_data['id_token'])
                self._expiration_datetime = datetime.now() + timedelta(seconds=token_data['expires_in'])
                self.current_user = jwt.decode(token_data['id_token'], algorithms=self.configuration['AuthZeroAlgorithms'], options={"verify_signature": False})
                self.org_id = self.current_user['https://api.raic.ai/organization']
                authenticated = True

                authFile = self._get_local_auth_file()
                authFile.write_text(json.dumps(token_data))

            elif token_data['error'] not in ('authorization_pending', 'slow_down'):
                print(f'Error generating the device code. Status Code: {token_response.status_code}, Reason: {token_response.reason}')
                print(f'Text: {token_response.text}')
                raise Exception(f'Error generating the device code. Status Code: {token_response.status_code}, Reason: {token_response.reason}')
            else:
                time.sleep(device_code_data['interval'])

    def login_if_not_already(self):
        if not self.is_logged_in():
            self.login()

    def is_logged_in(self) -> bool:
        timeout_margin = timedelta(seconds=60)
        return self.current_user is not None and self._expiration_datetime is not None and self._expiration_datetime - datetime.now() > timeout_margin

    def get_org_id(self) -> str:
        return str(self.org_id) 

    def get_user(self):
        return self.current_user 

    def get_access_token(self):
        return self.access_token 

    def _validate_token(self, id_token):
        jwks_url = 'https://{}/.well-known/jwks.json'.format(self.configuration['AuthZeroTenantName'])
        issuer = 'https://{}/'.format(self.configuration['AuthZeroTenantName'])
        sv = AsymmetricSignatureVerifier(jwks_url)
        tv = TokenVerifier(signature_verifier=sv, issuer=issuer, audience=self.configuration['AuthZeroV2ClientId'])
        tv.verify(id_token)

    def _get_local_auth_file(self) -> Path:
        return Path(self._get_userdata_path(), "raic-user-auth")
    
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
