import base64
import pickle
from typing import Optional, Iterator
from .request import raic_get, raic_stream_get, raic_post, raic_patch, raic_delete
from .raic_client_base import RaicClient

class InferenceClient(RaicClient):
    def __init__(self):
        return super().__init__()
    
    def get_inference_runs(self, top: int = 10, skip: int = 0):
        request = f"search/monitoringjobs"
        return raic_get(request, query_params={ '$orderBy': 'CreatedOn desc', '$top': top, '$skip': skip })

    def find_inference_runs_by_name(self, name: str):
        request = f"search/monitoringjobs"
        return raic_get(request, query_params={ '$orderBy': 'CreatedOn desc', '$filter': f"Name eq '{name}'" })

    def get_inference_run(self, inference_run_id: str):
        request = f"monitoring/jobs/{inference_run_id}"
        return raic_get(request)

    def create_inference_run(
        self, 
        name: str, 
        data_source_id: str,
        model_id: Optional[str] = None, 
        model_version: Optional[int] = None, 
        vectorizer_id: Optional[str] = None, 
        vectorizer_version: Optional[int] = None, 
        prediction_model_id: Optional[str] = None, 
        prediction_model_version: Optional[int] = None,
        raic_vision_model_id: Optional[str] = None, 
        raic_vision_model_version: Optional[int] = None, 
        iou: Optional[float] = 0.5, 
        confidence: Optional[float] = 0.1, 
        max_detects: Optional[int] = 10, 
        small_objects: Optional[bool] = False, 
        no_object_detection: bool = False, 
        no_batching: bool = False, 
        track_objects: bool = False, 
        metadata: Optional[dict] = None
    ):
        path = "monitoring/jobs"
        data = {
            "displayName": name,
            "domain": "Image",
            "dataSourceId": data_source_id,
            "raicVisionModelId": raic_vision_model_id,
            "raicVisionModelVersion": raic_vision_model_version,
            "predictionModelId": prediction_model_id,
            "predictionModelVersion": prediction_model_version,
            "miniBatchSize": 32,
            "noBatch": no_batching,
            "trackObjects": track_objects,
            "metadata": metadata
        }
        
        if model_id is not None and not no_object_detection:
            data["model"] = {
                "id": model_id,
                "version": model_version,
                "hyperParameters": {
                    "iou": iou,
                    "confidence": confidence,
                    "maxDetectionsPerImage": max_detects,
                    "smallObjects": small_objects
                }
            }
        
        if vectorizer_id is not None:
            data["vectorizer"] = {
                "id": vectorizer_id,
                "version": vectorizer_version
            }
                           
        return raic_post(path, data)

    def restart_inference_run(self, inference_run_id: str):
        request = f"monitoring/jobs/{inference_run_id}/restart"
        return raic_post(request)
    
    def update_inference_run(self, inference_run_id: str, name: Optional[str] = None, is_shared: Optional[bool] = None):
        request = f"monitoring/jobs/{inference_run_id}"
        payload = {}

        if name is not None:
            payload["name"] = name

        if is_shared is not None and bool(is_shared):
            payload["isShared"] = True
            payload["organizationPermission"] = "Full"

        return raic_patch(request, payload)

    def iter_detections(self, inference_run_id: str, include_embeddings: bool = False) -> Iterator[dict]:
        request = f"cascade-vision/inference-runs/{inference_run_id}/detections/stream?include_embeddings={include_embeddings}"
        iterator = raic_stream_get(request)
        for encoded_string in iterator:
            decoded_bytes = base64.b64decode(encoded_string)
            detection_record = pickle.loads(decoded_bytes)
            yield detection_record
    
    def delete_inference_run(self, inference_run_id: str):
        request = f"monitoring/jobs/{inference_run_id}"
        payload = { "isDeleted": True }
        return raic_patch(request, payload)



