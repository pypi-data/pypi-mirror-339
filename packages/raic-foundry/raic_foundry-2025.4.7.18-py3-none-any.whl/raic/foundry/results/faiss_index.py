import os
import faiss
import numpy as np
from pathlib import Path

from ..shared import azure as blob_storage


def get_faiss_index(
    container_url: str,
    inference_run_id: str,
    label_class: str = "whole"
) -> tuple[faiss.IndexFlatL2, np.ndarray]:
    """
    Retreives the faiss index and detection id mappings. 
    Looks for the faiss index files locally, then checks
    blob storage and raises an exception if none exists.

    Args:
        - container_url (str): 
            The URL of the blob storage container with sas token.
        - inference_run_id (str): 
            The inference run id.
        - label_class (str): 
            Each class in the inference run has its own index as well as an index with all the classes. 
            Specify which class index to download; defaults to "whole".

    Returns:
        tuple[faiss.IndexFlatL2, np.ndarray]:
            - the faiss index
            - an np-array of the detection id mappings
    """
    root_faiss_path = Path("/mnt/faiss")
    if not root_faiss_path.exists():
        root_faiss_path = Path(".cache")

    faiss_index_blobname = _get_faiss_index_blobname(inference_run_id, label_class)
    faiss_id_map_blobname = _get_faiss_id_map_blobname(inference_run_id, label_class)

    faiss_id_map_filename_temp = _get_faiss_id_map_filename_temp(root_faiss_path, inference_run_id, label_class)
    faiss_index_filename_temp = _get_faiss_index_filename_temp(root_faiss_path, inference_run_id, label_class)
    faiss_index_filename = _get_faiss_index_filename(root_faiss_path, inference_run_id, label_class)
    faiss_id_map_filename = _get_faiss_id_map_filename(root_faiss_path, inference_run_id, label_class)

    if faiss_index_filename.is_file():
        print(f"Index {faiss_index_filename.name} is local")

        faiss_index = faiss.read_index(str(faiss_index_filename))
        detection_ids = np.load(str(faiss_id_map_filename), allow_pickle=True)
    else:
        if faiss_id_map_filename_temp.exists() or faiss_index_filename_temp.exists():
            print(f"Failing out a request for index {faiss_index_filename.name} that's being built.")
            raise Exception("Building index, please come back later")

        try:
            faiss_index_filename.parent.mkdir(parents=True, exist_ok=True)

            # Check blob storage
            if blob_storage.blob_exists(container_url=container_url, blob_name=faiss_index_blobname):
                print(f"Index {faiss_index_filename.name} is in blob storage, pulling it down...")

                blob_storage.download_blob_to_file(
                    container_url=container_url,
                    blob_name=faiss_index_blobname,
                    destination_file=str(faiss_index_filename_temp)
                )

                blob_storage.download_blob_to_file(
                    container_url=container_url,
                    blob_name=faiss_id_map_blobname,
                    destination_file=str(faiss_id_map_filename_temp)
                )
                
                # Rename to indicate they are fully downloaded and ready for use
                faiss_index_filename_temp.rename(faiss_index_filename)
                faiss_id_map_filename_temp.rename(faiss_id_map_filename)
            
                faiss_index = faiss.read_index(str(faiss_index_filename))
                detection_ids = np.load(str(faiss_id_map_filename), allow_pickle=True)

                print(f"Index {faiss_index_filename.name} download from blob storage complete")
            else:
                raise Exception("Index cannot be found, please reach out to the platform team to have it created")
        finally:
            if faiss_id_map_filename_temp.exists():
                os.remove(str(faiss_id_map_filename_temp))

            if faiss_index_filename_temp.exists():
                os.remove(str(faiss_index_filename_temp))

    return faiss_index, detection_ids


def _get_faiss_index_filename(root_path: Path, inference_run_id: str, label_class: str) -> Path:
    return Path(root_path, f"{inference_run_id}_{label_class}.faiss")

def _get_faiss_id_map_filename(root_path: Path, inference_run_id: str, label_class: str) -> Path:
    return Path(root_path, f"{inference_run_id}_{label_class}.npy")

def _get_faiss_index_blobname(inference_run_id: str, label_class: str):
    return f"{inference_run_id}/index/{label_class}.faiss"

def _get_faiss_id_map_blobname(inference_run_id: str, label_class: str):
    return f"{inference_run_id}/index/{label_class}.npy"

def _get_faiss_index_filename_temp(root_path: Path, inference_run_id: str, label_class: str) -> Path:
    return Path(root_path, f"{inference_run_id}_{label_class}_temp.faiss")

def _get_faiss_id_map_filename_temp(root_path: Path, inference_run_id: str, label_class: str) -> Path:
    return Path(root_path, f"{inference_run_id}_{label_class}_temp.npy")

