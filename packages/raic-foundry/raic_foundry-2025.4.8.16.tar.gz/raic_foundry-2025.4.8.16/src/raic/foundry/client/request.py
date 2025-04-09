import io
import requests
import urllib.parse
from pathlib import Path
from typing import Optional, Any, Iterator
import raic.foundry.client.context
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 503, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def raic_get(request: str, query_params: Optional[dict] = None):
    response = requests_retry_session().get(_build_endpoint(request, query_params), headers=_get_headers())
    response.raise_for_status()
    return response.json()


def raic_stream_get(request: str, query_params: Optional[dict] = None) -> Iterator:
    with requests_retry_session().get(_build_endpoint(request, query_params), headers=_get_headers(), stream=True) as response:
        response.raise_for_status()
        for line in response.iter_lines(decode_unicode=True):
            if line:  # Filter out keep-alive new lines
                yield line


def raic_post(request: str, data: Optional[Any] = None, query_params: Optional[dict] = None):
    response = requests_retry_session().post(_build_endpoint(request, query_params), headers=_get_headers(), json=data)
    response.raise_for_status()
    return response.json()


def raic_patch(request: str, data, query_params: Optional[dict] = None):
    response = requests_retry_session().patch(_build_endpoint(request, query_params), headers=_get_headers(), json=data)
    response.raise_for_status()
    return response.json()


def raic_delete(request: str, query_params: Optional[dict] = None):
    response = requests_retry_session().get(_build_endpoint(request, query_params), headers=_get_headers())
    response.raise_for_status()
    return response.json()


def raic_download_file(request: str, destination_file_path: Path, query_params: Optional[dict] = None):
    response = requests_retry_session().get(_build_endpoint(request, query_params), headers=_get_headers(), stream=True)
    response.raise_for_status()

    with destination_file_path.open('wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

    print(f"File '{str(destination_file_path)}' downloaded successfully.")


def raic_download_bytes(request: str, query_params: Optional[dict] = None):
    response = requests_retry_session().get(_build_endpoint(request, query_params), headers=_get_headers(), stream=True)
    response.raise_for_status()

    return io.BytesIO(response.content)

def _build_endpoint(request, query_params: Optional[dict] = None) -> str:
    safe_request = urllib.parse.quote(request)
    endpoint = f'{raic.foundry.client.context.get_raic_configuration('ApiRoot')}/{safe_request.lstrip('/')}'
    if query_params is not None:
        endpoint += f'?{'&'.join([f'{k}={urllib.parse.quote(str(v))}' for k, v in query_params.items()])}'

    return endpoint

def _get_headers() -> dict:
    headers = {"Authorization": f"Bearer {raic.foundry.client.context.get_raic_auth().get_access_token()}"}
    return headers
