import math
import PIL.Image
from io import BytesIO
from typing import Generator, Iterator, Any
from pathlib import Path
import datetime
import rasterio
import rasterio.crs
import rasterio.warp
import rasterio.windows
import rasterio.transform
from rasterio.enums import ColorInterp
from rasterio.io import MemoryFile, DatasetReader
from rio_tiler.io import Reader
from rio_tiler.reader import Options
from rio_tiler.constants import WGS84_CRS
from shapely import Polygon, Point
from ..entities.artifacts import GeospatialInfo, ImageArtifact
import raic.foundry.inputs.image as image
import raic.foundry.inputs.exif

def prepare(image_file_path: Path, root_path: Path, max_size_px: int = 9792) -> Generator[Path, Any, None]:
    if isinstance(image_file_path, Iterator) or isinstance(image_file_path, Generator):
        for img in image_file_path:
            yield from prepare(img, root_path)

        return

    dataset = load_raster(image_file_path)
    if dataset is None or dataset.crs is None:
        return
    
    if dataset.width > max_size_px or dataset.height > max_size_px:
        tile_paths = tile_raster(dataset)
        for tile_path in tile_paths:
            yield tile_path.relative_to(root_path)   
    elif dataset.driver == 'GTiff':
        yield image_file_path.relative_to(root_path) 
    else:
        geotiff_dataset = to_geotiff(dataset)
        dataset_path = Path(geotiff_dataset.name)
        yield dataset_path.relative_to(root_path)       


def get_info(image: Path | PIL.Image.Image | DatasetReader) -> GeospatialInfo | None:
    dataset = load_raster(image)
    if dataset is not None:
        with dataset:
            info = get_raster_info(dataset)
            if info is not None:
                return info
            
    return _get_exif_info(image)


def to_geotiff(source_dataset: DatasetReader, output_file: Path | str | None = None):
    if source_dataset.driver == 'GTiff':
        return source_dataset
    
    output_file = Path(output_file if output_file is not None else source_dataset.name)
    output_file = output_file.with_suffix(".tif")
    options = {"compress": "jpeg"}

    source_crs = source_dataset.crs
    profile = source_dataset.profile
    profile.update(
        crs=WGS84_CRS,
        driver="GTiff",
        **options
    )

    with rasterio.open(output_file, "w", **profile) as destination_dataset:
        num_bands = source_dataset.count 

        for band_index in range(1, num_bands + 1):
            color_interp = source_dataset.colorinterp[band_index - 1]
            print(f"Band {band_index}: {color_interp}")

            rasterio.warp.reproject(
                source=rasterio.band(source_dataset, band_index),
                destination=rasterio.band(destination_dataset, band_index),
                src_transform=source_dataset.transform,
                src_crs=source_crs,
                dst_transform=destination_dataset.transform,
                dst_crs=WGS84_CRS,
                resampling=rasterio.warp.Resampling.cubic
            )

        return  destination_dataset


def tile_raster(source_dataset: DatasetReader, output_folder: Path | str | None = None, tile_size_px: int = 9792, tile_oxerlap_px: int = 0, bindexes = None,  src_alpha = None, dst_alpha = None) -> list[Path]:
    # https://dpird-dma.github.io/blog/How-to-efficiently-create-millions-of-overlapping-raster-tiles/
    # https://www.gpxz.io/blog/rasterio-cropping
    # https://github.com/mapbox/rio-mbtiles/blob/main/mbtiles/worker.py

    source_dataset_path = Path(source_dataset.name)

    if source_dataset.width <= tile_size_px and source_dataset.height <= tile_size_px:
        return [source_dataset_path]
    
    source_compression = source_dataset.profile['compress'] if 'compress' in source_dataset.profile else None
    if source_compression is None:
        source_compression = source_dataset.profile['COMPRESS'] if 'COMPRESS' in source_dataset.profile else None

    if output_folder is not None:
        output_folder = Path(output_folder, source_dataset_path.stem)
    else:
        output_folder = Path(source_dataset_path.parent, source_dataset_path.stem)
        
    output_folder.mkdir(parents=True, exist_ok=True)

    tile_paths = []
    with Reader(input=None, dataset=source_dataset) as rio_reader:
        column_count = math.ceil(source_dataset.width / tile_size_px)
        row_count = math.ceil(source_dataset.height / tile_size_px)
        for row_index in range(row_count):
            for column_index in range(column_count):
                ulx = column_index * tile_size_px
                uly = row_index * tile_size_px
                lrx = min(ulx + tile_size_px, source_dataset.width - 1)
                lry = min(uly + tile_size_px, source_dataset.height - 1)
                (left, bottom, right, top) = _get_geodetic_bounds(ulx=ulx, uly=uly, lrx=lrx, lry=lry, transform=source_dataset.transform) # (left, bottom, right, top)
                tile_image = rio_reader.part(bbox=(left, bottom, right, top), max_size=tile_size_px, dst_crs=WGS84_CRS)

                options = {"compress": source_compression if source_compression is not None else "jpeg"}
                buffer = tile_image.render(img_format="GTIFF", **options)

                top_string = f"{'N' if top >= 0.0 else 'S'}{abs(top):0.9f}".replace('.', '')
                left_string = f"{'E' if left >= 0.0 else 'W'}{abs(left):0.9f}".replace('.', '')
                tile_destination_path = Path(output_folder, f"{top_string}_{left_string}.tif")
                with tile_destination_path.open("wb") as f:
                    f.write(buffer)

                tile_paths.append(tile_destination_path)

    return tile_paths


def get_geodetic_extents(geo_info: GeospatialInfo, x0:int, y0:int, x1:int, y1:int):
    coordinates = _get_geodetic_coordinates(geo_info.transform, [[x0, y0], [x1, y0], [x1, y1], [x0, y1]])
    return Polygon([
        [coordinates[0][0], coordinates[0][1]], 
        [coordinates[1][0], coordinates[1][1]], 
        [coordinates[2][0], coordinates[2][1]],
        [coordinates[3][0], coordinates[3][1]], 
        [coordinates[0][0], coordinates[0][1]]
    ])


def get_geodetic_coordinate(geo_info: GeospatialInfo, x:int, y:int):
    coordinates = _get_geodetic_coordinates(geo_info.transform, (x, y))[0]
    return Point(coordinates[0], coordinates[1])


def load_raster(image_path: str | Path | PIL.Image.Image | DatasetReader):
    try:
        if isinstance(image_path, str):
            return rasterio.open(image_path)

        if isinstance(image_path, Path):
            return rasterio.open(str(image_path))
            
        elif isinstance(image_path, DatasetReader):
            return image_path
            
        elif isinstance(image_path, PIL.Image.Image):
            with BytesIO() as buffer:
                image_path.save(buffer, format='TIF')
                image_path.close()
                with MemoryFile(buffer.getvalue()) as memfile:
                    return memfile.open()
    
    except Exception as e:
        pass

    return None


def get_raster_info(dataset: DatasetReader) -> GeospatialInfo | None:
    if dataset.crs is None:
        return None
        
    extents = _get_extents_feature(dataset)

    info = GeospatialInfo(
        crs=dataset.crs,
        transform=dataset.transform,
        extents=extents,
        centroid=Point(extents.centroid),
        collected_on=_get_datetime_from_tags(dataset)
    )  

    if dataset.count >= 3:
        try:
            info.red_band=dataset.colorinterp.index(ColorInterp.red)
            info.green_band=dataset.colorinterp.index(ColorInterp.green)
            info.blue_band=dataset.colorinterp.index(ColorInterp.blue)
            info.alpha_band=dataset.colorinterp.index(ColorInterp.alpha)
        except:
            print("Warning: The color bands aren't explicitly defined in the image, falling back to a guess of RGB order")
            info.red_band=0
            info.green_band=1
            info.blue_band=2

    return info
    

def _get_exif_info(image: Path | PIL.Image.Image) -> GeospatialInfo | None:
    frame_location = raic.foundry.inputs.exif.get_location(image)
    if frame_location is None:
        return None
    
    return GeospatialInfo(
            centroid=frame_location
        )


def _get_geodetic_bounds(ulx, uly, lrx, lry, transform) -> tuple:
    columns = [ulx, lrx]
    rows = [uly, lry]
    lons, lats = rasterio.transform.xy(transform, rows, columns)
    return (lons[0], lats[1], lons[1], lats[0])


def _get_geodetic_coordinates(transform, pixel_coordinates):
    rows = [coordinate[1] for coordinate in pixel_coordinates]
    columns = [coordinate[0] for coordinate in pixel_coordinates]
    lons, lats = rasterio.transform.xy(transform, rows, columns)

    return [[lat, lon] for lat, lon in zip(lats, lons)]


def _get_extents_feature(dataset: DatasetReader) -> Polygon:
    bbox = dataset.bounds
    
    return Polygon([
            [bbox.left, bbox.top],
            [bbox.right, bbox.top],
            [bbox.right, bbox.bottom],
            [bbox.left, bbox.bottom],
            [bbox.left, bbox.top],
        ])

def _get_datetime_from_tags(dataset: DatasetReader):
    tags = dataset.tags()
    if 'TIFFTAG_DATETIME' in tags:
        try:
            return datetime.datetime.strptime(tags['TIFFTAG_DATETIME'], '%Y:%m:%d %H:%M:%s')
        except:
            print("Warning: Couldn't parse raster tag TIFFTAG_DATETIME")
            pass 

    if 'DateTime' in tags:
        try:
            return datetime.datetime.strptime(tags['DateTime'], '%Y:%m:%d %H:%M:%s')
        except:
            print("Warning: Couldn't parse raster tag DateTime")
            pass  

    return None 
