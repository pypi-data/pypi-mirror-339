import base64
import pickle
from typing import Optional, Iterator
from .request import raic_get, raic_stream_get, raic_post, raic_patch
from .raic_client_base import RaicClient
from .inference_job import InferenceClient

class CascadeVisionClient(RaicClient):
    def __init__(self):
        return super().__init__()

    def get_run(self, cascade_vision_run_id: str):
        request = f"cascade-vision/cascade-vision-runs/{cascade_vision_run_id}"
        return raic_get(request)

    def create_run(
        self, 
        name: str, 
        data_source_id: str,
        raic_vision_model_id: Optional[str] = None, 
        raic_vision_model_version: Optional[int] = None, 
        iou: Optional[float] = 0.5, 
        confidence: Optional[float] = 0.1, 
        max_detects: Optional[int] = 10, 
        small_objects: Optional[bool] = False, 
        metadata: Optional[dict] = None
    ):
        return InferenceClient().create_inference_run(
            name=name, 
            data_source_id=data_source_id,
            raic_vision_model_id=raic_vision_model_id, 
            raic_vision_model_version=raic_vision_model_version, 
            iou=iou, 
            confidence=confidence, 
            max_detects=max_detects, 
            small_objects=small_objects,
            metadata=metadata
        )

    def restart_run(self, cascade_vision_run_id: str):
        request = f"cascade-vision/cascade-vision-runs/{cascade_vision_run_id}/restart"
        return raic_post(request)
    
    def update_run(self, cascade_vision_run_id: str, name: Optional[str] = None, is_shared: Optional[bool] = None, is_deleted: Optional[bool] = None):
        request = f"cascade-vision/cascade-vision-runs/{cascade_vision_run_id}"
        payload = {}

        if name is not None:
            payload["name"] = name

        if is_shared is not None and bool(is_shared):
            payload["organizationPermission"] = "Full"

        if is_deleted is not None:
            payload["is_deleted"] = is_deleted

        return raic_patch(request, payload)

    def iter_detections(self, cascade_vision_run_id: str, include_embeddings: bool = False) -> Iterator[dict]:
        request = f"cascade-vision/cascade-vision-runs/{cascade_vision_run_id}/detections/stream?include_embeddings={include_embeddings}"
        iterator = raic_stream_get(request)
        for encoded_string in iterator:
            decoded_bytes = base64.b64decode(encoded_string)
            detection_record = pickle.loads(decoded_bytes)
            yield detection_record



