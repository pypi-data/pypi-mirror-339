from .request import raic_get, raic_post, raic_patch
from .raic_client_base import RaicClient

def create_context(context_name: str):
    request = f"/overwatch/contexts"
    payload = {
        "context_name": context_name
    }
    return raic_post(request, payload)


def get_overwatch_detections(context_id: str, inference_run_id: str, class_label: str):
    request = f"/overwatch/inference_run/{inference_run_id}/detections/context/{context_id}/detectionsWithOverwatch?top=100&label_class={class_label}"
    response = raic_get(request)
    return response['pageItems']


def get_overwatch_container_sas_url():
    request = "/overwatch/sas_url"
    response = raic_get(request)
    return response['sas_url']

