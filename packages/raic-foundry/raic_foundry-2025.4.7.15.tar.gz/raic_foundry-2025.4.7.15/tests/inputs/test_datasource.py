import os
import shutil
import pytest
from pathlib import Path
import raic.foundry.inputs.datasource as datasource

# Get the directory of the current script
root_dir = Path(os.path.abspath(__file__)).parent.parent.absolute()


def test_double_unpack_via_file(setUp):
    workspace_path, output_directory = setUp
    input_path = Path(workspace_path, 'datasources', 'trimble_3_zip/trimble_3.zip')
    remove_files_except(input_path, "trimble_3.zip")

    source_zip_file_path = Path(input_path)
    manifest = datasource.prepare(source_zip_file_path)
    assert 3 == len(manifest.relative_paths)

    manifest = datasource.prepare(source_zip_file_path)
    assert 3 == len(manifest.relative_paths)

    
def test_double_unpack_via_folder(setUp):
    workspace_path, output_directory = setUp
    input_path = Path(workspace_path, 'datasources', 'trimble_3_zip/trimble_3.zip')
    remove_files_except(input_path, "trimble_3.zip")

    source_zip_folder_path = Path(input_path).parent
    manifest = datasource.prepare(source_zip_folder_path)
    assert 3 == len(manifest.relative_paths)

    manifest = datasource.prepare(source_zip_folder_path)
    assert 3 == len(manifest.relative_paths)


@pytest.fixture
def setUp(request: pytest.FixtureRequest):
    workspace_path = Path(root_dir, '.ignore')
    output_directory = Path(workspace_path, 'test', request.node.name)

    if os.path.exists(output_directory) and os.path.isdir(output_directory):
        print(f'Cleaning up any previous runs of {request.node.name} before starting...')
        shutil.rmtree(output_directory)

    os.makedirs(output_directory, exist_ok=True)

    # Clear scaling variables
    if 'BATCH_SIZE' in os.environ:
        del os.environ['BATCH_SIZE']

    if 'NUM_WORKERS' in os.environ:
        del os.environ['NUM_WORKERS']

    print(f'Setup for {request.node.name} complete')
    yield workspace_path, output_directory


def remove_files_except(directory, keep_files):
    if os.path.isfile(directory):
        directory = os.path.dirname(directory)

    for file_or_folder_name in os.listdir(directory):
        filepath = os.path.join(directory, file_or_folder_name)

        if os.path.isfile(filepath) and file_or_folder_name not in keep_files:
            os.remove(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath)

