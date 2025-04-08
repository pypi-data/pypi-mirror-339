from pathlib import Path
from .request import raic_download_bytes
from .raic_client_base import RaicClient

def get_inference_crop(inference_run_id: str, detection_id: str):
    request = f"imagery/monitoring/{inference_run_id}/crops/{detection_id}.jpg"
    return raic_download_bytes(request)


def get_inference_low_res_image(inference_run_id: str, image_name: str):
    rename = Path(image_name).with_suffix(".jpg")
    request = f"imagery/monitoring/{inference_run_id}/low/{rename}"
    return raic_download_bytes(request)

