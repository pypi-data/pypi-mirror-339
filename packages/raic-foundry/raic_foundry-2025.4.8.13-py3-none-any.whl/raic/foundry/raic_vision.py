"""
Raic Vision models are a powerful tool to perform object detection and classification without costly model training.

Here are some quickstart examples on creating a run for these models. Make sure to first login to Raic Foundry

.. code-block:: python

    from raic.foundry.client.context import login_if_not_already

    # Login to Raic Foundry (prompted on the command line)
    login_if_not_already()


Example: Perform objection detection with a raic vision model

.. code-block:: python

    from raic.foundry.datasources import Datasource
    from raic.foundry.raic_vision import RaicVisionRun

    # Look up existing data source record
    data_source = Datasource.from_existing('My Existing Data Source')

    # Look up models from model registry
    raic_vision_model = RaicVisionModel.from_existing('My Raic Vision Model', version='latest')

    # Start new raic vision run
    run = RaicVisionRun.new(name='My New Inference Run', data_source=data_source, raic_vision_model=raic_vision_model)

    while not run.is_complete():
        time.sleep(10)

    data_frame = run.fetch_predictions_as_dataframe()
    print(data_frame)

    
Example: Iterating results from query as an alternative

.. code-block:: python

    from raic.foundry.inference import RaicVisionRun

    ...
    for prediction in run.iterate_predictions():
        print(prediction)


"""

from typing import Optional
from raic.foundry.datasources import Datasource
from raic.foundry.models import RaicVisionModel
from raic.foundry.client.raic_vision_job import CascadeVisionClient
from raic.foundry.inference import InferenceRun

class RaicVisionRun(InferenceRun):
    def __init__(self, record: dict):
        """Manage a raic vision run

        Args:
            record (dict): Inference run record from the API
        """
        super().__init__(record, is_raic_vision=True)
    
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

        if cls._is_uuid(identifier):
            run_record = CascadeVisionClient().get_run(identifier)

        if run_record is None:
            raise Exception(f"Raic vision run {identifier} cannot be found")

        return InferenceRun(run_record, is_raic_vision=True)

    @classmethod
    def from_prompt(
        cls,
        data_source: Datasource,
        name: Optional[str] = None,
        raic_vision_model: Optional[RaicVisionModel] = None
    ):
        return InferenceRun.from_prompt(name=name, data_source=data_source, raic_vision_model=raic_vision_model)
        
    @classmethod
    def new(
        cls,
        name: str,
        data_source: Datasource,
        raic_vision_model: RaicVisionModel|str
    ):
        """Create a new raic vision inference run

        Args:
            name (str): Name of new inference run
            data_source (Datasource): Data source object representing imagery already uploaded to a blob storage containers
            raic_vision_model (RaicVisionModel | str): Model combining all three previous models into one.

        Raises:
            Exception: If no vectorizer model is specified

        Returns:
            InferenceRun
        """
        return InferenceRun.new(name=name, data_source=data_source, raic_vision_model=raic_vision_model)



