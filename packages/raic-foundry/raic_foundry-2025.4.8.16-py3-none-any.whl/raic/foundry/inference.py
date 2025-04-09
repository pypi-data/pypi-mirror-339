"""
Inference run execute raic foundry object detection, vectorization and prediction

Inference runs can serve a variety of different purposes.  They can operate on both geospatial and non-geospatial imagery formats, taking into account their temporal tags whenever possible.

Here are some quickstart examples. Make sure to first login to Raic Foundry

.. code-block:: python

    from raic.foundry.client.context import login_if_not_already

    # Login to Raic Foundry (prompted on the command line)
    login_if_not_already()


Example: Object detect and vectorize crops using default models

.. code-block:: python

    from raic.foundry.datasources import Datasource
    from raic.foundry.inference import InferenceRun

    # Look up existing data source record
    data_source = Datasource.from_existing('My Existing Data Source')

    # Start new inference run
    run = InferenceRun.new(name='My New Inference Run', data_source=data_source)

    data_frame = run.wait_and_return_dataframe()
    print(data_frame)

Example: Only vectorize images (aka classification only)

.. code-block:: python

    from raic.foundry.datasources import Datasource
    from raic.foundry.inference import InferenceRun

    # Look up existing data source record
    data_source = Datasource.from_existing('My Existing Data Source')

    # Start new inference run
    run = InferenceRun.new(name='My New Inference Run', data_source=data_source, universal_detector=None)

    data_frame = run.wait_and_return_dataframe()
    print(data_frame)
 
Example: Fully customize universal detector, vectorizer model as well as a prediction model

.. code-block:: python

    from raic.foundry.datasources import Datasource
    from raic.foundry.models import UniversalDetector, VectorizerModel, PredictionModel
    from raic.foundry.inference import InferenceRun

    # Look up existing data source record
    data_source = Datasource.from_existing('My Existing Data Source')

    # Look up models from model registry
    universal_detector = UniversalDetector.from_existing('baseline', version='latest')
    vectorizer_model = VectorizerModel.from_existing('baseline', version='latest')
    prediction_model = PredictionModel.from_existing('My Prediction Model', version='latest')

    # Start new inference run
    run = InferenceRun.new(
        name='CM Inference Run', 
        data_source=data_source, 
        universal_detector=universal_detector,
        vectorizer_model=vectorizer_model,
        prediction_model=prediction_model
    )

    data_frame = run.wait_and_return_dataframe()
    print(data_frame)

    
Example: Iterating results from query as an alternative

.. code-block:: python

    from raic.foundry.inference import InferenceRun

    ...
    for prediction in run.iterate_predictions():
        print(prediction)


"""
import csv
import uuid
import time
import tempfile
import pandas as pd
from pathlib import Path
from typing import Optional, Any, Iterator, List
from concurrent.futures import ThreadPoolExecutor, as_completed
from shapely import Point, from_wkt

from raic.foundry.shared.utils import chunk_iterable
from raic.foundry.datasources import Datasource
from raic.foundry.models import UniversalDetector, VectorizerModel, PredictionModel, RaicVisionModel
from raic.foundry.client.inference_job import InferenceClient
from raic.foundry.client.raic_vision_job import CascadeVisionClient
from raic.foundry.cli.console import clear_console

class InferenceRun():
    def __init__(self, record: dict, is_raic_vision: bool = False):
        """Manage an inference run

        Args:
            record (dict): Inference run record from the API
        """
        self.id = record['id']
        self._record = record
        self._is_raic_vision = is_raic_vision

    def is_complete(self) -> bool:
        """Check whether the run has completed yet

        Returns:
            bool: True if run status is Completed
        """
        if self._is_raic_vision:
            updated_record = CascadeVisionClient().get_run(self.id)
        else:
            updated_record = InferenceClient().get_inference_run(self.id)

        return updated_record['status'] == 'Completed'

    def restart(self):
        """In the event that an inference run gets stuck it can be restarted from the beginning.  Any frames already processed will be skipped.
        """
        if self._is_raic_vision:
            CascadeVisionClient().restart_run(self.id)
        else:
            InferenceClient().restart_inference_run(self.id)

    def iterate_predictions(self, include_embeddings: bool = True) -> Iterator[dict]:
        """Iterate through all inference run prediction results as they are queried from the API

        Args:
            include_embeddings (bool, optional): Include the embedding vector with each prediction. Defaults to True.

        Yields:
            Iterator[dict]: All of the prediction results as an iterator, optionally including the embeddings for each
        """
        if self._is_raic_vision:
            return CascadeVisionClient().iterate_predictions(self.id, include_embeddings)
        else:
            return InferenceClient().iterate_predictions(self.id, include_embeddings)

    def fetch_predictions_as_dataframe(self, include_embeddings: bool = True) -> pd.DataFrame:
        """Collect all of the prediction results from the inference run

        Args:
            include_embeddings (bool, optional): Include the embedding vector with each prediction. Defaults to True.

        Returns:
            DataFrame: All of the prediction results as a pandas DataFrame, optionally including the embeddings for each
        """
        if self._is_raic_vision:
            iterator = CascadeVisionClient().iterate_predictions(self.id, include_embeddings)
        else:
            iterator = InferenceClient().iterate_predictions(self.id, include_embeddings)

        fieldnames=["inference_run_id", "detection_id", "frame_id", 
                    "image_name", "label_class", "confidence", "x0", "y0", "x1", "y1", 
                    "centroid", "extent", "frame_sequence_number", "embedding", "builder_class_id"]

        def get_centroid(centroid: str | None) -> Point | None:
            return None if centroid is None else from_wkt(centroid).centroid

        def get_extent(extent: str | None):
            return None if extent is None else from_wkt(extent)

        with tempfile.NamedTemporaryFile(mode='w+t', delete=True) as tmpfile:
            writer = csv.DictWriter(tmpfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for record in iterator:
                record['centroid'] = get_centroid(record['centroid'])
                record['extent'] = get_extent(record['extent'])
                complete_row = {field: record.get(field, '') for field in fieldnames}
                writer.writerow(complete_row)

            tmpfile.seek(0)
            return pd.read_csv(tmpfile)
        
    def wait_and_return_dataframe(self, poll_interval: int = 10, include_embeddings: bool = True) -> pd.DataFrame:
        """Wait for inference run to complete return predictions as a data frame

        Args:
            poll_interval (int, optional): Polling interval in seconds. Minimum value is 5 seconds. Defaults to 10 seconds.
            include_embeddings (bool, optional): Include the embedding vector with each prediction. Defaults to True.

        Returns:
            DataFrame: All of the prediction results as a pandas DataFrame, optionally including the embeddings for each
        """
        if poll_interval is None or poll_interval < 5:
            poll_interval = 5

        while not self.is_complete():
            time.sleep(poll_interval)

        return self.fetch_predictions_as_dataframe()

    def stream_crop_images(self, destination_path: Path | str, max_workers: Optional[int] = None) -> Iterator[Path]:
        """Download the crops images for inference run predictions

        Each one is named by its prediction identifier

        Args:
            destination_path (Path | str): Local folder where prediction crops will be downloaded.
            max_workers (Optional[int], optional): Max number of worker threads to parallelize download. Defaults to None.

        Yields:
            Iterator[Path]: Iterator of each crop image local path as its downloaded
        """
        prediction_iterator = self.iterate_predictions(include_embeddings=False)

        def download(prediction: dict):
            local_file_path = Path(destination_path, f'{prediction['detection_id']}.jpg')
            InferenceClient().download_crop_image(inference_run_id=self.id, detection_id=prediction['detection_id'], save_to_path=local_file_path)
            return local_file_path

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(download, batch): batch
                for batch in prediction_iterator
            }

            for future in as_completed(futures):
                yield future.result()

    def delete(self):
        """Delete the inference run
        """
        if self._is_raic_vision:
            CascadeVisionClient().update_run(self.id, is_deleted=True)
        else:
            InferenceClient().delete_inference_run(self.id)
    
    @classmethod
    def from_existing(cls, identifier: str):
        """Look up an existing inference run by its UUID or its name
        Note: If there are multiple runs with the same name looking up by name will fail with an Exception

        Args:
            identifier (str): Either the UUID of the inference run or its name

        Raises:
            Exception: If multiple runs are returned with the same name

        Returns:
            InferenceRun
        """

        is_raic_vision = False
        if cls._is_uuid(identifier):
            try:
                run_record = CascadeVisionClient().get_run(identifier)
            except Exception:
                run_record = None

            if run_record is not None:
                is_raic_vision = True
            else:
                run_record = InferenceClient().get_inference_run(identifier)

            if run_record is None:
                raise Exception(f"Inference run {identifier} cannot be found")
        else:
            response = InferenceClient().find_inference_runs_by_name(identifier)
            if len(response['value']) == 0 or len(response['value']) > 1:
                raise Exception(f"{len(response['value'])} inference runs are named '{identifier}'")
            
            run_record = response['value'][0]

        return InferenceRun(run_record, is_raic_vision)

    @classmethod
    def from_prompt(
        cls,
        data_source: Datasource,
        name: Optional[str] = None,
        universal_detector: Optional[UniversalDetector] = None,
        vectorizer_model: Optional[VectorizerModel] = None,
        prediction_model: Optional[PredictionModel] = None,
        raic_vision_model: Optional[RaicVisionModel] = None
    ):
        if bool(name):
            return cls.new(name=name, data_source=data_source, universal_detector=universal_detector, vectorizer_model=vectorizer_model, prediction_model=prediction_model)
        
        clear_console()
        print(f"Datasource: {data_source._record['name']}")

        if raic_vision_model is None:
            universal_detector_name = "baseline" if universal_detector is None else universal_detector._record['name']
            vectorizer_model_name = "baseline" if vectorizer_model is None else vectorizer_model._record['name']

            print(f"Universal Detector: {universal_detector_name}")
            print(f"Vectorizer Model: {vectorizer_model_name}")

            default_name = f"{data_source._record['name']} ({universal_detector_name}) ({vectorizer_model_name})"

            if prediction_model is not None:
                print(f"Prediction Model: {prediction_model._record['name']}")
                default_name += f" ({prediction_model._record['name']})"
        else:
            print(f"Raic Vision Model: {raic_vision_model._record['name']}")
            default_name = f"{data_source._record['name']} ({raic_vision_model._record['name']})"
            
        print()

        selection = input(f"What should this inference run be called? [{default_name}]: ")
        if not bool(selection):
            return cls.new(name=default_name, data_source=data_source, universal_detector=universal_detector, vectorizer_model=vectorizer_model, prediction_model=prediction_model)
       
        return cls.new(name=selection, data_source=data_source, universal_detector=universal_detector, vectorizer_model=vectorizer_model, prediction_model=prediction_model)
        
    @classmethod
    def new(
        cls,
        name: str,
        data_source: Datasource,
        universal_detector: Optional[UniversalDetector|str] = 'baseline',
        vectorizer_model: Optional[VectorizerModel|str] = 'baseline',
        prediction_model: Optional[PredictionModel|str] = None,
        raic_vision_model: Optional[RaicVisionModel|str] = None
    ):
        """Create a new inference run

        Args:
            name (str): Name of new inference run
            data_source (Datasource): Data source object representing imagery already uploaded to a blob storage container
            universal_detector (Optional[UniversalDetector | str], optional): Model for object detection. Defaults to 'baseline'.
            vectorizer_model (Optional[VectorizerModel | str]): Model for vectorizing detection drop images. Defaults to 'baseline'.
            prediction_model (Optional[PredictionModel | str], optional): Model for classifying detections without needing deep training. Defaults to None.
            raic_vision_model (Optional[RaicVisionModel | str], optional): Model combining all three previous models into one. Defaults to None.

        Raises:
            Exception: If no vectorizer model is specified

        Returns:
            InferenceRun
        """
        if vectorizer_model is None:
            vectorizer_model = 'baseline'
        
        if universal_detector is not None and isinstance(universal_detector, str):
            universal_detector = UniversalDetector.from_existing(universal_detector)

        if isinstance(vectorizer_model, str):
            vectorizer_model = VectorizerModel.from_existing(vectorizer_model)

        if isinstance(prediction_model, str):
            prediction_model = PredictionModel.from_existing(prediction_model)

        if isinstance(raic_vision_model, str):
            raic_vision_model = RaicVisionModel.from_existing(raic_vision_model)

        run_record = InferenceClient().create_inference_run(
            name=name, 
            data_source_id=data_source.datasource_id, 
            model_id=universal_detector.id if universal_detector is not None else None,
            model_version=universal_detector.version if universal_detector is not None else None,
            iou=universal_detector.iou if universal_detector is not None else 0,
            confidence=universal_detector.confidence if universal_detector is not None else 0,
            max_detects=universal_detector.max_detects if universal_detector is not None else 0,
            small_objects=universal_detector.small_objects if universal_detector is not None else False,
            no_object_detection=False if universal_detector is not None else True,
            vectorizer_id=vectorizer_model.id,
            vectorizer_version=vectorizer_model.version,
            prediction_model_id=prediction_model.id if prediction_model is not None else None,
            prediction_model_version=prediction_model.version if prediction_model is not None else None,
            raic_vision_model_id=raic_vision_model.id if raic_vision_model is not None else None,
            raic_vision_model_version=raic_vision_model.version if raic_vision_model is not None else None
        )

        return InferenceRun(run_record, is_raic_vision=raic_vision_model is not None)

    @classmethod
    def _is_uuid(cls, uuid_to_test: str, version=4) -> bool:
        try:
            uuid.UUID(uuid_to_test, version=version)
            return True
        except ValueError:
            return False
    
    @classmethod
    def suppress_errors(cls, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                return None
        return wrapper


