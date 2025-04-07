import os
import pytz
from pathlib import Path
import raic.foundry.inputs.exif as exif

# Get the directory of the current script
current_dir = Path(os.path.abspath(__file__)).parent.absolute()

def test_no_exif():
    image_path = Path(current_dir, 'data', 'no_exif.jpg')
    result = exif.get_exif_data(image_path)
    assert result == None

def test_get_datetime_from_gps():
    image_path = Path(current_dir, 'data', 'mx50_example.jpg')
    result = exif.get_datetime(image_path)
    assert result is not None and result.strftime("%Y-%m-%d %H:%M:%S") == '2024-03-06 20:57:39'

def test_get_datetime_from_created():
    image_path = Path(current_dir, 'data', 'time_stamp_example.jpg')
    result = exif.get_datetime(image_path)
    assert result is not None and result.strftime("%Y-%m-%d %H:%M:%S") == '2024-12-17 06:00:00'
    assert result.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S") == '2024-12-17 12:00:00'

def test_get_location():
    image_path = Path(current_dir, 'data', 'mx50_example.jpg')
    result = exif.get_location(image_path)
    assert result is not None and result.geom_type == 'Point'
    assert result.x == 42.40971305555556
    assert result.y == -83.07517388888888
    assert result.z == 157.3527386

