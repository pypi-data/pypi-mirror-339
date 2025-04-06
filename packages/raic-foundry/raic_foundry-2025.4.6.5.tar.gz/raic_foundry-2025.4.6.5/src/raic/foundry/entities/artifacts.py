import json
import uuid
import datetime
import PIL.Image
import numpy as np
import pandas as pd
import shapely
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator
from shapely import Point, Polygon

class DataSourceArtifact(BaseModel):
    model_config = ConfigDict()

    root_path: Path
    files: list[Path]

class GeospatialInfo(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    crs: Optional[object] = None
    transform: Optional[object] = None
    extents: Optional[Polygon] = None
    centroid: Point
    collected_on: Optional[datetime.datetime] = None
    red_band: Optional[int] = None
    green_band: Optional[int] = None
    blue_band: Optional[int] = None
    alpha_band: Optional[int] = None

    def latitude(self):
        return self.centroid.y

    def longitude(self):
        return self.centroid.x

    def altitude(self):
        return self.centroid.z if self.centroid.has_z else 0.0
    
    # @staticmethod
    # def from_legacy_metadata(metadata_df):
    #     geo_crs = rasterio.crs.CRS.from_string(metadata_df['geo_crs']) if 'geo_crs' in metadata_df and pd.notnull(metadata_df['geo_crs']) else None
    #     geo_transform = rasterio.transform.Affine(*json.loads(metadata_df['geo_transform'])) if 'geo_transform' in metadata_df and pd.notnull(metadata_df['geo_transform']) else None
    #     geo_centroid = Point(float(metadata_df['longitude']), float(metadata_df['latitude'])) if 'longitude' in metadata_df and pd.notnull(metadata_df['longitude']) else None
    #     extents = shapely.from_geojson(metadata_df['geo_extents']) if 'geo_extents' in metadata_df and pd.notnull(metadata_df['geo_extents']) else None

    #     if geo_crs is not None or geo_transform is not None:
    #         return GeospatialInfo(crs=geo_crs, transform=geo_transform, centroid=geo_centroid, extents=extents)
    #     else:
    #         return None
        
    # def serialize_crs(self):
    #     return str(self.crs) if self.crs is not None else None
    
    # def deserialize_crs(cls, value, info):
    #     return rasterio.crs.CRS.from_string(value) if value is not None else None
            
    # def serialize_transform(self):
    #     return json.dumps(self.transform) if self.transform is not None else None
     
    # def deserialize_transform(cls, value, info):
    #     return rasterio.transform.Affine(*json.loads(value)) if value is not None else None
               
    # def serialize_extents(self):
    #     return shapely.to_geojson(self.extents) if self.extents is not None else None
    
    # def deserialize_extents(cls, value, info):
    #     return shapely.from_geojson(value) if value is not None else None
                
    # def serialize_centroid(self):
    #     return shapely.to_geojson(self.centroid) if self.centroid is not None else None
    
    # def deserialize_centroid(cls, value, info):
    #     return shapely.from_geojson(value) if value is not None else None
        

class ImageInfo(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    uid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    relative_path: Path
    local_path: Optional[Path] = None
    url: Optional[str] = None
    width: int
    height: int
    collected_on: Optional[datetime.datetime] = None
    sequence_number: Optional[int] = None
    geospatial: Optional[GeospatialInfo] = None

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

class MetatileInfo(ImageInfo):
    model_config = ConfigDict()
        
    tile_x_offset: int
    tile_y_offset: int 
    tile_width: int
    tile_height: int 
    parent_info: ImageInfo

    def to_metadata_json(self):
        metadata = {
            "src_id": 0, 
            "src_path": str(self.parent_info.relative_path), 
            "src_hw": [self.parent_info.height, self.parent_info.width], 
            "metatileId": str(uuid.uuid4()),
            "metatile_crop_path": str(self.relative_path), 
            "metatile_coord": [self.tile_x_offset, self.tile_y_offset, self.tile_x_offset+self.tile_width, self.tile_y_offset+self.tile_height], 
            "metatile_hw": [self.tile_height, self.tile_width]
        }

        if self.parent_info.geospatial is not None and self.parent_info.geospatial.centroid is not None:
            if self.parent_info.geospatial.centroid is not None:
                metadata['latitude'] = self.parent_info.geospatial.latitude()
                metadata['longitude'] = self.parent_info.geospatial.longitude()
                metadata['altitude'] = self.parent_info.geospatial.altitude()
                metadata['altitude_ref'] = 0

            if self.parent_info.geospatial.crs is not None:
                metadata['geo_crs'] = str(self.parent_info.geospatial.crs)

            if self.parent_info.geospatial.transform is not None:
                metadata['geo_transform'] = json.dumps(self.parent_info.geospatial.transform)

            if self.parent_info.geospatial.extents is not None:
                metadata['geo_extents'] = shapely.to_geojson(self.parent_info.geospatial.extents)

        return json.dumps(metadata)


class CropInfo(ImageInfo):
    model_config = ConfigDict()
        
    parent_info: ImageInfo


class ImageArtifact(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    info: ImageInfo
    image: Optional[PIL.Image.Image] = Field(exclude=True, default=None)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_image()

    def get_image(self) -> PIL.Image.Image:
        if self._is_image_open() and isinstance(self.image, PIL.Image.Image):
            return self.image
        elif self.info.local_path is not None:
            self.image = PIL.Image.open(str(self.info.local_path))
            return self.image
        else:
            raise Exception(f'Cannot open image artifact {self.info.name}, no local path available')
        
    def close_image(self):
        if self.image is not None:
            self.image.close()
            self.image = None # Note this appear to help greatly with avoid memory leaks
    
    def _is_image_open(self):
        try:
            if self.image is None:
                return False
            
            self.image.load()
            return True
        except ValueError:
            return False

    def __hash__(self):
        return hash((type(self), self.info.__hash__()))
   

class DetectionBoxArtifact(BaseModel):   
    topX: float
    topY: float
    bottomX: float
    bottomY: float

class DetectionArtifact(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    parent_info: ImageInfo
    inference_run_id: str
    uid: str
    label: str
    label_index: Optional[int] = None
    score: float
    box: DetectionBoxArtifact
    crop: Optional[ImageArtifact] = None
    embedding: Optional[np.ndarray] = None
    geospatial_centroid: Optional[Point] = None
    geospatial_extent: Optional[Polygon] = None
    distance: Optional[float] = None

    def latitude(self):
        return self.geospatial_centroid.y if self.geospatial_centroid is not None else None

    def longitude(self):
        return self.geospatial_centroid.x if self.geospatial_centroid is not None else None

    def altitude(self):
        if self.geospatial_centroid is None:
            return None
        return self.geospatial_centroid.z if self.geospatial_centroid.has_z else 0.0

    def serialize_extents(self):
        return shapely.to_geojson(self.geospatial_extent) if self.geospatial_extent is not None else None
    
    @classmethod
    def deserialize_extents(cls, value):
        return shapely.from_geojson(value) if value is not None else None
                
    def serialize_centroid(self):
        return shapely.to_geojson(self.geospatial_centroid) if self.geospatial_centroid is not None else None
    
    @classmethod
    def deserialize_centroid(cls, value):
        return shapely.from_geojson(value) if value is not None else None
        
    @field_serializer('embedding')
    def serialize_embedding(self, value):
        return value.tolist() if value is not None else None
    
    @classmethod
    @field_validator('embedding')
    def deserialize_embedding(cls, value):
        return np.array(json.loads(value)) if value is not None else None

class MetatileDetectionsArtifact(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    parent_artifact: ImageArtifact
    boxes: list[DetectionArtifact]


class TrackWaypointArtifact(BaseModel):
    track_id: int
    detection_id: str
    score: float
    velocity_angle: Optional[float]
    velocity_magnitude: Optional[float]
    type: Optional[str]


class FrameDetectionsArtifact(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    inference_run_id: str
    parent_artifact: ImageArtifact
    boxes: list[DetectionArtifact]
    tracks: Optional[list[TrackWaypointArtifact]] = None
    folder: Optional[str] = None

    def get_detection_by_uid(self, detection_id):
        for detection in self.boxes:
            if detection.uid == detection_id:
                return detection       
        return None
            
    def to_obb(self):
        boxes = []
        for detection in self.boxes:
            x1 = detection.box.topX * detection.parent_info.width
            y1 = detection.box.topY * detection.parent_info.height 
            x2 = detection.box.bottomX * detection.parent_info.width
            y2 = detection.box.bottomY * detection.parent_info.height
            cls = [detection.label_index] if detection.label_index is not None else None
            boxes.append(box_obb(xyxy=[(x1, y1, x2, y2)], cls=cls, detection_artifact=detection))

        return [frame_obb(boxes=boxes)]


class ClusterArtifact(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    identifier: str
    centroid_detection_record_id: int
    centroid_detection_id: str
    detections: pd.DataFrame
    
    @staticmethod
    def to_json_summary_by_class(inference_run_id: str, cluster_artifacts: list["ClusterArtifact"]):
        cluster_results = {}
        cluster_results["inference_run_id"] = inference_run_id
        class_label = str(cluster_artifacts[0].detections.iloc[0]['class_label'])

        cluster_data = []
        for cluster in cluster_artifacts:
            tmp = {}
            tmp["cluster_label"] = class_label
            tmp["clusterId"] = cluster.identifier
            example_detection =  cluster.detections.loc[cluster.detections['detection_id'] == cluster.centroid_detection_id].iloc[0]
            
            latitude = None
            longitude = None
            if example_detection['detection_centroid'] is not None:
                geo_centroid = shapely.from_wkt(str(example_detection['detection_centroid']))
                latitude = geo_centroid.centroid.y
                longitude = geo_centroid.centroid.x

            tmp["example"] = {
                "detectionId": str(example_detection['detection_id']),
                "image_name": str(example_detection['image_name']),
                "x0": float(example_detection['x0']),
                "y0": float(example_detection['y0']),
                "x1": float(example_detection['x1']),
                "y1": float(example_detection['y1']),
                "label_class": class_label,
                "latitude": latitude,
                "longitude": longitude,
                "confidence": float(example_detection['confidence'])
            }
            tmp["count"] = len(cluster.detections)
            cluster_data.append(tmp)

        # Save the json file containing info for clusters
        cluster_results["class_name"] = class_label
        cluster_results["clusters"] = cluster_data
        return cluster_results


class box_obb(BaseModel):
    xyxy: list[tuple]
    cls: Optional[list[int]] = None
    detection_artifact: DetectionArtifact


class frame_obb(BaseModel):
    boxes: list[box_obb]


class CoordsLatentsInfo(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    image_id: int
    image_name: str
    detection_id: str
    x0: float
    y0: float
    x1: float
    y1: float
    embedding: Optional[np.ndarray] = None
    
    @classmethod
    def from_numpy(cls, image_name: str, image_width: int, image_height: int, coords: np.ndarray, latents: Optional[np.ndarray] = None):
        """
        Parses coords array with columns names as

        [img_id, xyxy]

        (5 columns total)
        """
        return cls(
            image_id=coords[0],
            image_name=image_name,
            detection_id=str(uuid.uuid4()),
            x0=coords[1]/image_width,
            y0=coords[2]/image_height,
            x1=coords[3]/image_width,
            y1=coords[4]/image_height,
            embedding=latents
        )

class FacetCoordsLatentsInfo(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    image_id: int
    image_name: str
    detection_id: str
    x0: float
    y0: float
    x1: float
    y1: float
    score: float
    class_index: int
    zoom_level: int
    topLatitude: float
    topLongitude: float
    bottomLatitude: float
    bottomLongitude: float
    embedding: Optional[np.ndarray] = None

    def get_geodetic_extents(self) -> shapely.Polygon:
        return shapely.Polygon([
            [self.topLongitude, self.topLatitude], 
            [self.topLongitude, self.bottomLatitude], 
            [self.bottomLongitude, self.bottomLatitude],
            [self.bottomLongitude, self.topLatitude], 
            [self.topLongitude, self.topLatitude]
        ])

    def get_geodetic_centroid(self) -> shapely.Point:
        return self.get_geodetic_extents().centroid
    
    @classmethod
    def from_numpy(cls, image_name: str, coords: np.ndarray, latents: Optional[np.ndarray] = None):
        """
        Parses coords array with columns names as

        [img_id, xyxy, conf, cls_id, objconf, mapz, mapxyxy, latlngyxyx]

        (17 columns total)
        """
        return cls(
            image_id=coords[0],
            image_name=image_name,
            detection_id=str(uuid.uuid4()),
            x0=coords[1],
            y0=coords[2],
            x1=coords[3],
            y1=coords[4],
            score=coords[7],
            class_index=int(coords[6]),
            zoom_level=int(coords[8]),
            topLatitude=coords[13],
            topLongitude=coords[14],
            bottomLatitude=coords[15],
            bottomLongitude=coords[16],
            embedding=latents
        )