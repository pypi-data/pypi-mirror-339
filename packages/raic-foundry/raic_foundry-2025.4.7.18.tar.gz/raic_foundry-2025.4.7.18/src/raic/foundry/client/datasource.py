from .request import raic_get, raic_post, raic_delete
from .raic_client_base import RaicClient

class DataSourceClient(RaicClient):
    def __init__(self):
        return super().__init__()

    def get_recent_datasources(self, top: int = 10, skip: int = 0):
        request = f"search/datasources"
        query_params = { 
            '$filter': f"AcquisitionMode eq 'BatchInference'",
            '$orderBy': 'CreatedOn desc', 
            '$top': top,
            '$skip': skip
        }
        response = raic_get(request, query_params=query_params)
        return response['value']

    def find_datasources_by_name(self, name: str):
        request = f"search/datasources"
        return raic_get(request, query_params={ '$orderBy': 'CreatedOn desc', '$filter': f"Name eq '{name}'" })
    
    def get_datasource(self, datasource_id: str):
        request = f"datasources/{datasource_id}"
        return raic_get(request)
    
    def create_datasource(self, name: str, description: str | None = None):
        request = f"datasources"
        payload = {
            "name": name,
            "description": description if description is not None else name,
            "acquisitionMode": "BatchInference",
            "imageryProvider": "RaicBlob"
        }
        return raic_post(request, payload)
    
    def delete_datasource(self, datasource_id: str):
        request = f"datasources/{datasource_id}"
        return raic_delete(request)
