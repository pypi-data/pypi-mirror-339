import io
import traceback
import PIL.Image
from pathlib import Path
from ..entities.artifacts import (
    ImageArtifact, 
    ImageInfo, 
    CropInfo, 
    FrameDetectionsArtifact, 
    DetectionArtifact
)
import raic.foundry.shared.azure as azure
import raic.foundry.inputs.exif as exif

# Global Constants
TIFF_COMPRESSION = "tiff_lzw"  # TIFF compression to reduce file size
PIL.Image.MAX_IMAGE_PIXELS = 500000000

def load_from_local_file(file_path: Path, root_path: Path, sequence_number: int | None = None, keep_image_open: bool = True):
    image = None
    image_artifact = None

    try:
        image = _lazyload_image(file_path)

        if image is None:
            print(f'Skipping {file_path.name}, not an image file')
            return None

        image_artifact = ImageArtifact(
            info = ImageInfo(
                name=file_path.name,
                relative_path=file_path.relative_to(root_path),
                local_path=file_path,
                width=image.width,
                height=image.height,
                collected_on=exif.get_datetime(image),
                geospatial=None,
                sequence_number=sequence_number
            ),
            image=image        
        )
    finally:
        if not keep_image_open:
            if image is not None:
                image.close() # in case the image was not yet assigned to the artifact, explicitly close the image object

            if image_artifact is not None:
                image_artifact.close_image()

    return image_artifact


def save_to_local_file(image_artifact : ImageArtifact, output_directory: Path, keep_image_open: bool = False, png_compress_level: int = 6) -> ImageArtifact:
    try:
        local_path = Path(output_directory, image_artifact.info.relative_path)
        local_path.parent.mkdir(parents=True, exist_ok=True)
        image_artifact.image = image_artifact.image.convert('RGB')
        if 'png' in str(local_path).lower():
            image_artifact.image.save(str(local_path), compress_level=png_compress_level)
        else:
            image_artifact.image.save(str(local_path))
        image_artifact.info.local_path = local_path
    finally:
        if not keep_image_open:
            image_artifact.close_image()

    return image_artifact


def generate_crops(
    detection_frame: FrameDetectionsArtifact,
    output_path: Path | None = None,
    keep_source_image_open: bool = False
) -> list[DetectionArtifact]:
    detections_with_crops = []
    for detection in detection_frame.boxes:
        detections_with_crops.append(crop_detection_image(detection, detection_frame.parent_artifact, output_path, keep_source_image_open=keep_source_image_open))

    if not keep_source_image_open:
        detection_frame.parent_artifact.close_image()

    return detections_with_crops


def crop_detection_image(detection: DetectionArtifact, parent_artifact: ImageArtifact, output_path: Path | None = None, keep_source_image_open: bool = False) -> DetectionArtifact:
    try:
        frame_image = parent_artifact.get_image()
        cropped_image = frame_image.crop(
            (
                int(detection.box.topX * parent_artifact.info.width),
                int(detection.box.topY * parent_artifact.info.height),
                int(detection.box.bottomX * parent_artifact.info.width),
                int(detection.box.bottomY * parent_artifact.info.height),
            )
        )

        crop_image_info = CropInfo(
            uid=detection.uid,
            name=f"{detection.uid}.png",
            relative_path=Path(f"{detection.uid}.png"),
            width=cropped_image.width,
            height=cropped_image.height,
            parent_info=parent_artifact.info
        )

        crop_artifact = ImageArtifact(info=crop_image_info, image=cropped_image)

        if output_path is not None:
            detection.crop = save_to_local_file(crop_artifact, output_path, png_compress_level=1)
        else:
            detection.crop = crop_artifact
    finally:
        if not keep_source_image_open:
            parent_artifact.close_image()

    return detection


def resize_image(image_artifact: ImageArtifact, output_directory: Path, target_dimension: int = 1280, force_format: str | None = None):
    file_extension = image_artifact.info.relative_path.suffix.strip('.')
    output_path = Path(output_directory, image_artifact.info.uid)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if force_format is not None:
        file_extension = force_format.strip('.').lower()
        output_path = output_path.with_suffix(f'.{file_extension}')

    with image_artifact:
        image = image_artifact.get_image()
        if image.width > target_dimension or image.height > target_dimension:
            if image.width > image.height:
                image = image.resize((target_dimension, int(image.height/image.width*target_dimension)))
            else:
                image = image.resize((int(image.width/image.height*target_dimension), target_dimension))

        image = image.convert('RGB')
        if file_extension in ["tif", "tiff"]:
            image.save(output_path, format="TIFF", compression=TIFF_COMPRESSION)
        elif file_extension in ["jpg", "jpeg"]:
            image.save(output_path, compress_level=4)
        else:
            image.save(output_path, compress_level=4)

    resized_image_artifact = ImageArtifact(
        info=ImageInfo(
            uid=image_artifact.info.uid,
            name=output_path.name,
            relative_path=output_path.relative_to(output_directory),
            local_path=output_path,
            width=image.width,
            height=image.height,
            geospatial=image_artifact.info.geospatial
        ),
        image=image
    )

    return resized_image_artifact


def resize_image_by_target_kb(image_artifact: ImageArtifact, output_directory: Path, target_size_kb: int = 500, down_step_factor: float = 0.75, force_format: str | None = None):
    file_extension = image_artifact.info.relative_path.suffix.strip('.')
    output_path = Path(output_directory, image_artifact.info.uid)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if force_format is not None:
        file_extension = force_format.strip('.').lower()
        output_path = output_path.with_suffix(f'.{file_extension}')

    with image_artifact.get_image() as image:
        format = ''
        if file_extension in ["jpg", "jpeg"]:
            format="JPEG"
        elif file_extension == "png":
            format="PNG"
        elif file_extension in ["tif", "tiff"]:
            format="TIFF"
        else:
            raise Exception(f"Unsupported file type: {image_artifact.info.relative_path}")
        
        image = image.convert('RGB')
        img_resized, step_count = _downscale_image_by_kb(image, format, target_size_kb, down_step_factor)

        if format == "TIFF":
            img_resized.save(output_path, format=format, compression=TIFF_COMPRESSION)
        else:
            img_resized.save(output_path, format=format, optimize=True)

    lowres_image_artifact = ImageArtifact(
        info=ImageInfo(
            uid=image_artifact.info.uid,
            name=output_path.name,
            relative_path=output_path.relative_to(output_directory),
            local_path=output_path,
            width=img_resized.width,
            height=img_resized.height,
            geospatial=image_artifact.info.geospatial
        ),
        image=img_resized
    )

    return output_path, step_count, lowres_image_artifact


def _download_image(container_url, blob_name, local_path: Path | None = None) -> tuple[PIL.Image.Image | None, Path | None]:
    try:
        local_file_path = None
        if local_path is not None:
            local_file_path = Path(local_path, blob_name)
            local_file_path.parent.mkdir(parents=True, exist_ok=True)
            azure.download_blob_to_file(container_url, blob_name, str(local_file_path))
            image = _lazyload_image(local_file_path)
        else:
            blob_stream = azure.download_blob_to_stream(container_url, blob_name)
            byte_stream = io.BytesIO()
            blob_stream.readinto(byte_stream)
            image = PIL.Image.open(byte_stream)

        return image, local_file_path
    except (OSError, PIL.Image.UnidentifiedImageError):
        # This file isn't openable by Pillow
        return None, None
    except:
        print(traceback.format_exc())
        return None, None


def _lazyload_image(file_path: Path) -> PIL.Image.Image | None:
    try:
        return PIL.Image.open(str(file_path))
    except (OSError, PIL.Image.UnidentifiedImageError):
        return None
    except:
        print(traceback.format_exc())
        return None


def _local_images(source_folder: Path):
    if source_folder.is_dir():
        paths = [str(path) for path in source_folder.rglob("*.*")]
    elif source_folder.is_file():
        paths = [source_folder]
    else:
        raise Exception(f"{str(source_folder)} data source is not a valid input.")
    
    return paths


# General downscale utility
def _resize_image(img, step: float):
    """Resizes the image by a given step factor."""
    width, height = img.size
    new_width = int(width * step)
    new_height = int(height * step)
    return img.resize((new_width, new_height), PIL.Image.Resampling.LANCZOS)


def _downscale_image_by_kb(image, format: str, target_size_kb: int, step: float = 0.75):
    current_image = image
    step_count = 0
    while True:
        step_count += 1

        # Resize image
        current_image = _resize_image(current_image, step)
        
        # Try saving with current quality
        temp_file = io.BytesIO()

        if format == "TIFF":
            current_image.save(temp_file, format="TIFF", compression=TIFF_COMPRESSION)
        else:
            current_image.save(temp_file, format=format, optimize=True)

        file_size_kb = len(temp_file.getvalue()) / 1024  # Convert to KB
        
        if file_size_kb <= target_size_kb:
            return current_image, step_count
