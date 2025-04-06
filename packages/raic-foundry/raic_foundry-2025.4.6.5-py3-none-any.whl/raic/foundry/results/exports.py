import time
import pandas as pd
from raic.foundry.client.overwatch import get_overwatch_detections, raic_get, raic_post

def export_overwatch_dataframe(inference_run_id: str, context_id: str, class_label: str = "whole") -> pd.DataFrame:
    """
    Fetches all inference results from Overwatch and returns them as a pandas DataFrame.

    :param inference_run_id: The inference run ID.
    :type inference_run_id: str
    :param context_id: The context ID.
    :type context_id: str
    :param class_label: The label class to filter detections by (default is "whole").
    :type class_label: str, optional
    :return: A pandas DataFrame containing all inference results.
    :rtype: pd.DataFrame
    """
    all_results = []
    seen_ids = set()
    while True:
        batch_results = get_overwatch_detections(context_id, inference_run_id, class_label)
        new_results = [r for r in batch_results if r.get("id") not in seen_ids]
        if not new_results:
            break
        all_results.extend(new_results)
        seen_ids.update(r.get("id") for r in new_results)
    return pd.DataFrame(all_results)

def export_overwatch_pickle(inference_run_id: str, context_id: str, class_label: str = "whole") -> str:
    """
    Fetches all inference results from Overwatch, saves them as a Pickle file, and returns the file path.

    :param inference_run_id: The inference run ID.
    :type inference_run_id: str
    :param context_id: The context ID.
    :type context_id: str
    :param class_label: The label class to filter detections by (default is "whole").
    :type class_label: str, optional
    :return: The file path of the saved Pickle file.
    :rtype: str
    """
    df = export_overwatch_dataframe(inference_run_id, context_id, class_label)
    file_path = f"overwatch_results_{inference_run_id}.pkl"
    df.to_pickle(file_path)
    return file_path

def export_overwatch_csv(inference_run_id: str, context_id: str, class_label: str = "whole") -> str | None:
    """
    Initiates an Overwatch export request and retrieves the CSV download link.

    :param inference_run_id: The ID of the inference run.
    :type inference_run_id: str
    :param context_id: The ID of the context.
    :type context_id: str
    :param class_label: The label class to filter detections by (default is "whole").
    :type class_label: str, optional
    :return: A URL to the CSV file if successful, otherwise None.
    :rtype: str | None
    """
    request_path = "/exports"
    payload = {
        "label_class": class_label,
        "format": "Csv",
        "inference_run_id": inference_run_id,
        "context_id": context_id,
        "filters": {}
    }
    response = raic_post(request_path, payload)
    if not response or "export_id" not in response:
        return None
    export_id = response["export_id"]
    max_retries = 10
    retry_count = 0
    download_link = None
    while retry_count < max_retries:
        status_resp = raic_get(f"/exports/{export_id}")
        if status_resp.get("status") == "Completed":
            download_link = status_resp.get("download_link")
            break
        elif status_resp.get("status") == "Failed":
            return None
        time.sleep(5)
        retry_count += 1
    return download_link