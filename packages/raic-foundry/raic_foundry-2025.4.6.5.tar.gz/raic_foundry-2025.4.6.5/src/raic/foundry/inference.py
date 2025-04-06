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

    while not run.is_complete():
        time.sleep(10)

    data_frame = run.fetch_results_as_dataframe()
    print(data_frame)

Example: Only vectorize images (aka classification only)

.. code-block:: python

    from raic.foundry.datasources import Datasource
    from raic.foundry.inference import InferenceRun

    # Look up existing data source record
    data_source = Datasource.from_existing('My Existing Data Source')

    # Start new inference run
    run = InferenceRun.new(name='My New Inference Run', data_source=data_source, universal_detector=None)

    while not run.is_complete():
        time.sleep(10)

    data_frame = run.fetch_results_as_dataframe()
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

    while not run.is_complete():
        time.sleep(10)

    data_frame = run.fetch_results_as_dataframe()
    print(data_frame)

    
Example: Iterating results from query as an alternative

.. code-block:: python

    from raic.foundry.inference import InferenceRun

    ...
    for detection in run.iter_results():
        print(detection)


"""
import csv
import uuid
import tempfile
import pandas as pd
from typing import Optional, Any, Iterator
from raic.foundry.datasources import Datasource
from raic.foundry.models import UniversalDetector, VectorizerModel, PredictionModel, CascadeVisionModel
from raic.foundry.client.inference_job import InferenceClient
from raic.foundry.client.cascade_vision_job import CascadeVisionClient
from raic.foundry.cli.console import clear_console

class InferenceRun():
    def __init__(self, record: dict, is_cascade_vision: bool = False):
        """Manage an inference run

        Args:
            record (dict): Inference run record from the API
        """
        self.id = record['id']
        self._record = record
        self._is_cascade_vision = is_cascade_vision

    def is_complete(self) -> bool:
        """Check whether the run has completed yet

        Returns:
            bool: True if run status is Completed
        """
        if self._is_cascade_vision:
            updated_record = CascadeVisionClient().get_run(self.id)
        else:
            updated_record = InferenceClient().get_inference_run(self.id)

        return updated_record['status'] == 'Completed'

    def restart(self):
        """In the event that an inference run gets stuck it can be restarted from the beginning.  Any frames already processed will be skipped.
        """
        if self._is_cascade_vision:
            CascadeVisionClient().restart_run(self.id)
        else:
            InferenceClient().restart_inference_run(self.id)

    def iter_results(self, include_embeddings: bool = True) -> Iterator[dict]:
        """Iterate through all inference run detection results as they are queried from the API

        Args:
            include_embeddings (bool, optional): Include the embedding vector with each detection. Defaults to True.

        Yields:
            Iterator[dict]: All of the detection results as an iterator, optionally including the embeddings for each
        """
        if self._is_cascade_vision:
            return CascadeVisionClient().iter_detections(self.id, include_embeddings)
        else:
            return InferenceClient().iter_detections(self.id, include_embeddings)

    def fetch_results_as_dataframe(self, include_embeddings: bool = True) -> pd.DataFrame:
        """Collect all of the detection results from the inference run

        Args:
            include_embeddings (bool, optional): Include the embedding vector with each detection. Defaults to True.

        
        Returns:
            DataFrame: All of the detection results as a pandas DataFrame, optionally including the embeddings for each
        """
        if self._is_cascade_vision:
            iterator = CascadeVisionClient().iter_detections(self.id, include_embeddings)
        else:
            iterator = InferenceClient().iter_detections(self.id, include_embeddings)

        fieldnames=["inferenceRunId", "detectionId", "frameId", "frameUrl", 
                    "imageName", "labelClass", "confidence", "x0", "y0", "x1", "y1", 
                    "latitude", "longitude", "frameSequenceNumber", "embedding", "builderClassId"]

        with tempfile.NamedTemporaryFile(mode='w+t', delete=True) as tmpfile:
            writer = csv.DictWriter(tmpfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for record in iterator:
                writer.writerow(record)

            tmpfile.seek(0)
            return pd.read_csv(tmpfile)

    def delete(self):
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

        is_cascade_vision = False
        if cls._is_uuid(identifier):
            run_record = CascadeVisionClient().get_run(identifier)
            if run_record is not None:
                is_cascade_vision = True
            else:
                run_record = InferenceClient().get_inference_run(identifier)
        else:
            response = InferenceClient().find_inference_runs_by_name(identifier)
            if len(response['value']) == 0 or len(response['value']) > 1:
                raise Exception(f"{len(response['value'])} inference runs are named '{identifier}'")
            
            run_record = response['value'][0]

        return InferenceRun(run_record, is_cascade_vision)

    @classmethod
    def from_prompt(
        cls,
        data_source: Datasource,
        name: Optional[str] = None,
        universal_detector: Optional[UniversalDetector] = None,
        vectorizer_model: Optional[VectorizerModel] = None,
        prediction_model: Optional[PredictionModel] = None,
        cascade_vision_model: Optional[CascadeVisionModel] = None
    ):
        if bool(name):
            return cls.new(name=name, data_source=data_source, universal_detector=universal_detector, vectorizer_model=vectorizer_model, prediction_model=prediction_model)
        
        clear_console()
        print(f"Datasource: {data_source._record['name']}")

        if cascade_vision_model is None:
            universal_detector_name = "baseline" if universal_detector is None else universal_detector._record['name']
            vectorizer_model_name = "baseline" if vectorizer_model is None else vectorizer_model._record['name']

            print(f"Universal Detector: {universal_detector_name}")
            print(f"Vectorizer Model: {vectorizer_model_name}")

            default_name = f"{data_source._record['name']} ({universal_detector_name}) ({vectorizer_model_name})"

            if prediction_model is not None:
                print(f"Prediction Model: {prediction_model._record['name']}")
                default_name += f" ({prediction_model._record['name']})"
        else:
            print(f"Raic Vision Model: {cascade_vision_model._record['name']}")
            default_name = f"{data_source._record['name']} ({cascade_vision_model._record['name']})"
            
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
        cascade_vision_model: Optional[CascadeVisionModel|str] = None
    ):
        """Create a new inference run

        Args:
            name (str): Name of new inference run
            data_source (Datasource): Data source object representing imagery already uploaded to a blob storage container
            universal_detector (Optional[UniversalDetector | str], optional): Model for object detection. Defaults to 'baseline'.
            vectorizer_model (Optional[VectorizerModel | str]): Model for vectorizing detection drop images. Defaults to 'baseline'.
            prediction_model (Optional[PredictionModel | str], optional): Model for classifying detections without needing deep training. Defaults to None.
            cascade_vision_model (Optional[CascadeVisionModel | str], optional): Model combining all three previous models into one. Defaults to None.

        Raises:
            Exception: If no vectorizer model is specified

        Returns:
            InferenceRun
        """
        if vectorizer_model is None:
            vectorizer_model = 'baseline'
        
        if universal_detector is None:
            universal_detector = 'baseline'
        
        if isinstance(universal_detector, str):
            universal_detector = UniversalDetector.from_existing(universal_detector)

        if isinstance(vectorizer_model, str):
            vectorizer_model = VectorizerModel.from_existing(vectorizer_model)

        if isinstance(prediction_model, str):
            prediction_model = PredictionModel.from_existing(prediction_model)

        if isinstance(cascade_vision_model, str):
            cascade_vision_model = CascadeVisionModel.from_existing(cascade_vision_model)

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
            raic_vision_model_id=cascade_vision_model.id if cascade_vision_model is not None else None,
            raic_vision_model_version=cascade_vision_model.version if cascade_vision_model is not None else None
        )

        return InferenceRun(run_record, is_cascade_vision=cascade_vision_model is not None)

    @classmethod
    def _is_uuid(cls, uuid_to_test: str, version=4) -> bool:
        try:
            uuid.UUID(uuid_to_test, version=version)
            return True
        except ValueError:
            return False

