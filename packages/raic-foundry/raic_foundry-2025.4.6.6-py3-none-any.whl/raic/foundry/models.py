import abc
import uuid
from typing import Optional
from raic.foundry.client.model import ModelClient
from raic.foundry.cli.console import clear_console

class MLModel(abc.ABC):
    def __init__(
        self, 
        id: str, 
        version: int,
        record: dict
    ):
        self.id = id
        self.version = version
        self._record = record
        
    @classmethod
    def _get_record(cls, type: str, identifier: str):
        if cls._is_uuid(identifier):
            model_record = ModelClient().get_model(identifier)
        else:
            response = ModelClient().find_models_by_type_and_name(type=type, name=identifier)
            if len(response['value']) == 0 or len(response['value']) > 1:
                raise Exception(f"{len(response['value'])} models are named '{identifier}'")
            
            model_record = response['value'][0]

        return model_record

    @classmethod
    def _is_uuid(cls, uuid_to_test: str, version=4) -> bool:
        try:
            uuid.UUID(uuid_to_test, version=version)
            return True
        except ValueError:
            return False

    @classmethod
    def _from_existing(cls, identifier: str, version: int | str | None, model_type: str):
        model_record = cls._get_record(model_type, identifier)
        if version is None or version == 'latest':
            version = int(model_record['currentVersion'])
        else:
            model_version = next((v for v in model_record['modelVersions'] if v['versionNumber'] == version), None)
            if model_version is None:
                raise Exception(f'Version {version} of model {model_record['name']} ({model_record['id']}) cannot be found')

        return cls(id=model_record['id'], version=int(version), record=model_record)
    
    @classmethod
    def _from_prompt(cls, model_type: str):
        embedder_selected = False
        while not embedder_selected:
            clear_console()

            count = 10
            skip = 0
            existing_embedders = []
            selection = None

            while not bool(selection) or not selection.isnumeric():
                embedders_page = ModelClient().get_recent_embedders(top=count, skip=skip)
                existing_embedders.extend(embedders_page)
                for index, emb in enumerate(embedders_page):
                    print(f'{skip + index + 1}. {emb["name"]}')

                if len(embedders_page) > 0:
                    selection = input("Select vectorizer [more]: ")
                else:
                    selection = input("Select vectorizer (that's all): ")

                print()
                skip += count
            
            embedder_selected = True
        
        selected_model_record = existing_embedders[int(selection) - 1]
        return cls._from_existing(identifier=selected_model_record['name'], version=selected_model_record['currentVersion'], model_type=model_type)
    
    # Order matters for python decorators
    @classmethod
    @abc.abstractmethod
    def from_prompt(cls) -> "type[MLModel]":
        pass

    @classmethod
    @abc.abstractmethod
    def from_existing(cls, identifier: str, version: int | str | None = 'latest', **kwargs) -> "type[MLModel]":
        pass

class UniversalDetector(MLModel):
    def __init__(
        self, 
        id: str,
        version: int,
        record: dict,
        iou: Optional[float] = None,
        confidence: Optional[float] = None,
        max_detects: Optional[int] = None,
        small_objects: Optional[bool] = None,
    ):
        super().__init__(id, version, record)
        self.iou = iou
        self.confidence = confidence
        self.max_detects = max_detects
        self.small_objects = small_objects

    @classmethod
    def from_existing(cls, identifier: str, version: int | str | None = 'latest', iou: Optional[float] = None, confidence: Optional[int] = None, max_detects: Optional[int] = None) -> "UniversalDetector":
        model_record = super()._get_record('ObjectDetection', identifier)
        if isinstance(version, str) or version == None:
            version = int(model_record['currentVersion'])
        else:
            model_version = next((v for v in model_record['modelVersions'] if v['versionNumber'] == version), None)
            if model_version is None:
                raise Exception(f'Version {version} of model {model_record['name']} ({model_record['id']}) cannot be found')

        return UniversalDetector(
            id=model_record['id'], 
            version=int(version),
            iou=iou if iou is not None else model_record['versionDetails']['iou'],
            confidence=confidence if confidence is not None else model_record['versionDetails']['confidence'],
            max_detects=max_detects if max_detects is not None else model_record['versionDetails']['maxDetects'],
            record=model_record
        )

    @classmethod
    def from_prompt(cls) -> "UniversalDetector":
        return super()._from_prompt(model_type='ObjectDetection')   

class VectorizerModel(MLModel):
    def __init__(
        self, 
        id: str, 
        version: int,
        record: dict
    ):
        super().__init__(id, version, record)

    @classmethod
    def from_existing(cls, identifier: str, version: int | str | None = 'latest') -> "VectorizerModel":
        return super()._from_existing(identifier=identifier, version=version, model_type='Embedder')   

    @classmethod
    def from_prompt(cls) -> "VectorizerModel":
        return super()._from_prompt(model_type='Embedder')    

class PredictionModel(MLModel):
    def __init__(
        self, 
        id: str, 
        version: int,
        record: dict
    ):
        super().__init__(id, version, record)

    @classmethod
    def from_existing(cls, identifier: str, version: int | str | None = 'latest') -> "PredictionModel":
        return super()._from_existing(identifier=identifier, version=version, model_type='Prediction')   

    @classmethod
    def from_prompt(cls) -> "PredictionModel":
        return super()._from_prompt(model_type='Prediction')   

class CascadeVisionModel(MLModel):
    def __init__(
        self, 
        id: str, 
        version: int,
        record: dict
    ):
        super().__init__(id, version, record)

    @classmethod
    def from_existing(cls, identifier: str, version: int | str | None = 'latest') -> "CascadeVisionModel":
        return super()._from_existing(identifier=identifier, version=version, model_type='CascadeVision')   

    @classmethod
    def from_prompt(cls) -> "CascadeVisionModel":
        return super()._from_prompt(model_type='CascadeVision')   
 
