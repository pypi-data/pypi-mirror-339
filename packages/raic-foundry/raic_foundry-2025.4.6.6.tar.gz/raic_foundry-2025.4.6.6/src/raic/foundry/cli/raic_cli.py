import typer
from typing import Optional
from pathlib import Path
from typing_extensions import Annotated
from raic.foundry.cli.console import clear_console
import raic.foundry.cli.initialize as cli_initialize
from raic.foundry.client.context import login_if_not_already
from raic.foundry.inputs.datasource import prepare as datasource_prepare
from raic.foundry.datasources import Datasource
from raic.foundry.inference import InferenceRun

raic_commands = typer.Typer()

# -------- Login -------- ----------------------------------------------------

@raic_commands.command("login")
def login():
    login_if_not_already()


# -------- Data Source -------------------------------------------------------

data_source_commands = typer.Typer()
raic_commands.add_typer(data_source_commands, name="datasource")

@data_source_commands.command("prepare")
def prepare_datasource(
    source_path: Annotated[str, typer.Argument(help="Reformat, reproject, and break apart geospatial and non-geospatial imagery to raic-compatible")]
):
    """Search the local folder for usable imagery files.  
    
    PLEASE NOTE: this may require more than twice the original disk space as the original imagery
    
    For each found the following transformations will be made:
    1) Archive files (.zip, .tar, .bz2, .gz, .xz) will be unpacked
    2) Geospatial raster files (all single-file formats supported by gdal, multifile not yet supported) will be transformed to EPSG:4326 geotiff (.tif)
    3) Geotiff (.tif) files larger than 9792px in width or height will be separated into smaller tiles of 9792px
    4) Imagery formats (.jpg, .png, .bmp, .gif) are read and left unchanged

    Args:
        source_path (str, optional): Local imagery path or individual file

    Raises:
        Exception: If local folder does not exist
        Exception: If local folder contains not files
    """

    manifest = datasource_prepare(Path(source_path))
    print(manifest)

@data_source_commands.command("upload")
def upload_datasource(
    name: Annotated[str, typer.Argument(help="Name of the data source being created")],
    source_path: Annotated[str, typer.Argument(help="Local folder containing imagery or path of single file")],
    prepare: Annotated[bool, typer.Option(help="Reformat, reproject, and break apart geospatial and non-geospatial imagery to raic-compatible")]=True,
):
    """If this datasource is newly created from local imagery, upload to the data source blob storage

    Args:
        name (str, optional): Name of the data source being created
        source_path (str, optional): Local folder containing imagery or path of single file
        prepare (bool, optional): Reformat, reproject, and break apart geospatial and non-geospatial imagery to raic-compatible, Defaults to True
    
    Raises:
        Exception: If local folder does not exist
        Exception: If local folder contains not files
    """

    data_source_record = Datasource.new_from_local_folder(name=name, local_path=source_path, prepare_imagery=prepare)
    print(f'Data source {data_source_record._record['name]']} ({data_source_record.datasource_id}) created')


# -------- Inference -------------------------------------------------------

inference_app = typer.Typer()
raic_commands.add_typer(inference_app, name="inference")

@inference_app.command("start")
def start_inference(
    name: Annotated[Optional[str], typer.Option(help="Name of inference run")] = None,
    datasource: Annotated[Optional[str], typer.Option(help="Local path or UUID of existing data source")] = None,
    vision_model: Annotated[Optional[str], typer.Option(help="UUID of registered Raic Vision Model")] = None,
    vision_model_version: Annotated[Optional[int], typer.Option(help="Version of registered Raic Vision Model")] = None,
    core_model: Annotated[Optional[str], typer.Option(help="UUID of registered Core Model")] = None,
    core_model_version: Annotated[Optional[int], typer.Option(help="Version of registered Core Model")] = None,
    vectorizer: Annotated[Optional[str], typer.Option(help="UUID of registered Vectorizer Model")] = None,
    vectorizer_version: Annotated[Optional[int], typer.Option(help="Version of registered Vectorizer Model")] = None,
    prediction_model: Annotated[Optional[str], typer.Option(help="UUID of registered Prediction Model")] = None,
    prediction_model_version: Annotated[Optional[int], typer.Option(help="Version of registered Prediction Model")] = None,
    iou: Annotated[float, typer.Option(help="Core model IOU threshold")]=0.5,
    confidence: Annotated[float, typer.Option(help="Core model confidence threshold")]=0.01,
    max_detects: Annotated[int, typer.Option(help="Core model maximum detections per image")]=50,
    small_objects: Annotated[bool, typer.Option(help="Apply slicing to each image to detect small objects")]=False
) -> str:
    """Create a new inference run

    Args:
        name (str, optional): Name of inference run. Defaults to None.
        datasource (str, optional): Local path or UUID of existing data source. Defaults to None.
        vision_model (str, optional): UUID of registered Raic Vision Model. Defaults to None.
        vision_model_version (int, optional): Version of registered Raic Vision Model. Defaults to None.
        core_model (str, optional): UUID of registered Core Model. Defaults to None.
        core_model_version (int, optional): Version of registered Core Model. Defaults to None.
        vectorizer (str, optional): UUID of registered Vectorizer Model. Defaults to None.
        vectorizer_version (int, optional): Version of registered Vectorizer Model. Defaults to None.
        prediction_model (str, optional): UUID of registered Prediction Model. Defaults to None.
        prediction_model_version (int, optional): Version of registered Prediction Model. Defaults to None.
        iou (float, optional): Core model IOU threshold. Defaults to 0.5.
        confidence (float, optional): Core model confidence threshold. Defaults to 0.01.
        max_detects (int, optional): Core model maximum detections per image. Defaults to 50.
        small_objects (bool, optional): Apply slicing to each image to detect small objects. Defaults to False.

    Raises:
        Exception: If no vectorizer model is specified
    
    Returns:
        str: Inference run id
    """

    clear_console()
    print()
    print("------------------------------------------------------")
    print()
    print("  Welcome to the RAIC Foundry CLI")
    print()
    print("------------------------------------------------------")
    print()

    cli_initialize.authenticate()

    # Select datasource, model, etc from cli args or user input
    inference_run = cli_initialize.select_inputs(
        inference_run_id=None,
        name=name,
        datasource=datasource,
        core_model=core_model,
        core_model_version=core_model_version,
        vectorizer=vectorizer,
        vectorizer_version=vectorizer_version,
        prediction_model=prediction_model,
        prediction_model_version=prediction_model_version,
        vision_model=vision_model,
        vision_model_version=vision_model_version,
        iou=iou,
        confidence=confidence,
        max_detects=max_detects,
        small_objects=small_objects
    )

    print()
    print("------------------------------------------------------")
    print(" Inference Run Started Successfully")
    print(f"  Name: {inference_run._record['name']}")
    print(f"  Id:   {inference_run.id}")
    print("------------------------------------------------------")
    print()

    return inference_run.id


@inference_app.command("restart")
def resume_inference(inference_run_id: Annotated[str, typer.Option(help="Identifier of inference run or raic vision run")]):
    """In the event that an inference run gets stuck it can be restarted from the beginning.  Any frames already processed will be skipped.

    Args:
        inference_run_id (str, optional): Identifier of inference run or raic vision run.
    """
    run = InferenceRun.from_existing(inference_run_id)
    run.restart()


if __name__ == "__main__":
    raic_commands()