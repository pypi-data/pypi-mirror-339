from .request import raic_get
from .raic_client_base import RaicClient

def get_current_user():
    request = f"users"
    response = raic_get(request)
    return response

