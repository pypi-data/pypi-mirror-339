from typing import Optional
from pathlib import Path
from raic.foundry.client.environment import EnvironmentEnum
import raic.foundry.client.context as context

from raic.foundry.datasources import Datasource
from raic.foundry.models import MLModel, UniversalDetector, VectorizerModel, PredictionModel, CascadeVisionModel
from raic.foundry.inference import InferenceRun

def authenticate():
    print()

    context.login_if_not_already()

    current_environment = context.get_environment()
    current_user = context.get_username()

    proceed_with_existing_context = False
    if current_environment != EnvironmentEnum.Unspecified and current_user is not None:
        selection = input(f"Use existing setup ({current_environment.name}, {current_user})? (y/n) [y]: ")
        print()
        if not bool(selection) or selection.lower() == 'y':
            proceed_with_existing_context = True

    if proceed_with_existing_context:
        context.login_if_not_already()
    else:     
        environment = _determine_environment()
        context.set_environment(environment)
        context.login_if_not_already()


def select_inputs(
    inference_run_id: Optional[str] = None,
    name: Optional[str] = None,
    datasource: Optional[str | Path] = None,
    core_model: Optional[str] = None,
    core_model_version: Optional[int] = None,
    vectorizer: Optional[str] = None,
    vectorizer_version: Optional[int] = None,
    prediction_model: Optional[str] = None,
    prediction_model_version: Optional[int] = None,
    vision_model: Optional[str] = None,
    vision_model_version: Optional[int] = None,
    iou: Optional[float] = None,
    confidence: Optional[float] = None,
    max_detects: Optional[int] = None,
    small_objects: Optional[bool] = None
) -> InferenceRun:

    if inference_run_id is not None:
        # inference_record = InferenceClient().get_inference_run(inference_run_id)
        # data_source_obj = Datasource.from_existing(identifier=inference_record['dataSourceId'])

        # if inference_record['raicVisionModelId'] is None:
        #     universal_detector_obj = UniversalDetector.from_existing(identifier=inference_record['modelId'], version=inference_record['modelVersion'])
        #     vectorizer_obj = VectorizerModel.from_existing(identifier=inference_record['vectorizerId'], version=inference_record['vectorizerVersion'])
        #     prediction_model_obj = PredictionModel.from_existing(identifier=inference_record['predictionModelId'], version=inference_record['predictionModelVersion'])
        # else:
        #     cascade_vision_model_obj = CascadeVisionModel.from_existing(identifier=inference_record['raicVisionModelId'], version=inference_record['raicVisionModelVersion'])

        inference_run_obj = InferenceRun.from_existing(inference_run_id)
    else:
        data_source_obj = _prompt_for_data_source(datasource, prepare_imagery=False, upload_imagery=False)

        if vision_model is None:
            cascade_vision_model_obj = None
            universal_detector_obj = _prompt_for_model(UniversalDetector, core_model, core_model_version) if core_model is not None else None
            vectorizer_obj = _prompt_for_model(VectorizerModel, vectorizer, vectorizer_version) if vectorizer is not None else None
            prediction_model_obj = _prompt_for_model(PredictionModel, prediction_model, prediction_model_version) if prediction_model is not None else None

            if isinstance(universal_detector_obj, UniversalDetector):
                universal_detector_obj.iou = iou if iou is not None else universal_detector_obj.iou
                universal_detector_obj.confidence = confidence if confidence is not None else universal_detector_obj.confidence
                universal_detector_obj.max_detects = max_detects if max_detects is not None else universal_detector_obj.max_detects
                universal_detector_obj.small_objects = small_objects if small_objects is not None else universal_detector_obj.small_objects
        else:
            cascade_vision_model_obj = CascadeVisionModel.from_existing(vision_model, vision_model_version)

        inference_run = InferenceRun.from_prompt(
            name=name, 
            data_source=data_source_obj, 
            universal_detector=universal_detector_obj if isinstance(universal_detector_obj, UniversalDetector) else None,
            vectorizer_model=vectorizer_obj if isinstance(vectorizer_obj, VectorizerModel) else None,
            prediction_model=prediction_model_obj if isinstance(prediction_model_obj, PredictionModel) else None, 
            cascade_vision_model=cascade_vision_model_obj if isinstance(cascade_vision_model_obj, CascadeVisionModel) else None
        )

    print()
    if data_source_obj != None and data_source_obj._needs_upload == True: 
        data_source_obj.prepare()
        data_source_obj.upload()
        context.set_datasource(data_source_obj)
    
    print()
    print("Let's light this candle.")

    return inference_run

def _prompt_for_data_source(data_source: Optional[Path | str] = None, prepare_imagery: bool = True, upload_imagery: bool = True) -> Datasource:
    if isinstance(data_source, Path) and Path(data_source).exists():
        return Datasource.new_from_local_folder(Path(data_source).stem, data_source, prepare_imagery=prepare_imagery, upload_imagery=upload_imagery)
    elif isinstance(data_source, str):
        return Datasource.from_existing(identifier=data_source)
    else:
        return Datasource.from_prompt(prepare_imagery=prepare_imagery, upload_imagery=upload_imagery)


def _prompt_for_model(model_type: type[MLModel], identifier: str, version: int | str | None = 'latest') -> type[MLModel]:
    if identifier is not None:
        return model_type.from_existing(identifier=identifier, version=version)
    else:
        return model_type.from_prompt()


def _determine_environment() -> EnvironmentEnum:
    print(f"Please select your environment")
    print(f"  1. {EnvironmentEnum.Dev.name}")
    print(f"  2. {EnvironmentEnum.QA.name}")
    print(f"  3. {EnvironmentEnum.Prod.name}")
    print()
    environment_selection = input(f"[default is {EnvironmentEnum.Dev.name}]: ")
    
    environment = EnvironmentEnum.Dev

    if environment_selection.isnumeric():
        environment_selection = int(environment_selection)
        if environment_selection == 1:
            environment = EnvironmentEnum.Dev
        elif environment_selection == 2:
            environment = EnvironmentEnum.QA
        elif environment_selection == 3:
            environment = EnvironmentEnum.Prod
    else:
        environment_selection = environment_selection.lower()
        if environment_selection == 'dev':
            environment = EnvironmentEnum.Dev
        elif environment_selection == 'qa':
            environment = EnvironmentEnum.QA
        elif environment_selection == 'prod' or environment_selection == 'prd':
            environment = EnvironmentEnum.Prod

    return environment

