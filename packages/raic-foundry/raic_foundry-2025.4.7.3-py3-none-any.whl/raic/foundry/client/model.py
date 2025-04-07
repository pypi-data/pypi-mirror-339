from pathlib import Path
from .request import raic_get
from ..shared import azure as az
from .raic_client_base import RaicClient

class ModelClient(RaicClient):
    def __init__(self):
        return super().__init__()

    def get_recent_models(self, top: int = 10, skip: int = 0):
        request = f"search/registeredmodels"
        query_params = { 
            '$filter': f"ModelType eq 'ObjectDetection'",
            '$orderBy': 'CreatedOn desc', 
            '$top': top,
            '$skip': skip
        }
        response = raic_get(request, query_params=query_params)
        return response['value']

    def get_recent_embedders(self, top: int = 10, skip: int = 0):
        request = f"search/registeredmodels"
        query_params = { 
            '$filter': f"ModelType eq 'Embedder'",
            '$orderBy': 'CreatedOn desc', 
            '$top': top,
            '$skip': skip
        }
        response = raic_get(request, query_params=query_params)
        return response['value']

    def find_models_by_type_and_name(self, type: str, name: str):
        request = f"search/registeredmodels"
        query_params = { 
            '$filter': f"ModelType eq '{type}' and Name eq '{name}'",
            '$orderBy': 'CreatedOn desc'
        }
        return raic_get(request, query_params=query_params)

    def get_model(self, model_id: str):
        request = f"registeredmodels/{model_id}"
        return raic_get(request)
