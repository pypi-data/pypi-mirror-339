import PIL.Image
from pathlib import Path
from PIL.ExifTags import TAGS, GPSTAGS
from shapely import Point
from datetime import datetime, time
import pytz

def get_datetime(image: PIL.Image.Image | Path | str) -> datetime | None:
    try:
        gps_info = get_gps_info(image)
        if gps_info is not None:   
            return _get_datetime_from_gps_info(gps_info)
        
        datetime_info = get_datetime_info(image)
        if datetime_info is not None:   
            return datetime_info
        
        return None
    except:
        return None    

def get_location(image: PIL.Image.Image | Path | str) -> Point | None:
    try:
        gps_info = get_gps_info(image)

        if gps_info is not None:   
            coordinates = _get_decimal_coordinates(gps_info)
            if coordinates:
                return Point(coordinates)

        return None
    except:
        return None   

def get_gps_info(image: PIL.Image.Image | Path | str) -> dict[str, object] | None:
    value = _get_tag_value(get_exif_data(image), 'GPSInfo')
    if value is not None:
        gps_info = {
            GPSTAGS.get(subtag, subtag): subvalue
            for subtag, subvalue in value.items()
            if subtag in GPSTAGS
        }

        return gps_info
    
    return None


def get_datetime_info(image: PIL.Image.Image | Path | str) -> datetime | None:
    exif_data = get_exif_data(image)

    if exif_data:
        exif_datetime_value = _get_tag_value(exif_data, 'DateTimeOriginal')

        if exif_datetime_value is None:
            exif_datetime_value = _get_tag_value(exif_data, 'DateTimeDigitized')

        if exif_datetime_value is None:
            exif_datetime_value = _get_tag_value(exif_data, 'DateTime')

        if exif_datetime_value is not None:
            exif_datetime = datetime.strptime(exif_datetime_value, '%Y:%m:%d %H:%M:%S')
            exif_timezone_offset_value = _get_tag_value(exif_data, 'TimeZoneOffset')
            if exif_timezone_offset_value is not None:
                timezone_info = pytz.FixedOffset(int(exif_timezone_offset_value) * 60)
                exif_datetime = exif_datetime.replace(tzinfo=timezone_info)

            return exif_datetime
    
    return None


def get_exif_data(image: PIL.Image.Image | Path | str):
    """Gets EXIF data from an image file."""
    try:
        if isinstance(image, PIL.Image.Image):
            return image._getexif()
        else:
            with PIL.Image.open(str(image)) as img:
                return img._getexif()
    except AttributeError:
        return None
    

def _get_decimal_coordinates(gps_info):
    """Converts EXIF GPS data to decimal degrees."""
    latitude = None
    latitude_ref = None
    longitude = None
    longitude_ref = None
    altitude = 0.0
    altitude_ref = 0
    for key, value in gps_info.items():
        if key == "GPSLatitude":
            latitude = value
        elif key == "GPSLatitudeRef":
            latitude_ref = value
        elif key == "GPSLongitude":
            longitude = value
        elif key == "GPSLongitudeRef":
            longitude_ref = value
        elif key == "GPSAltitude":
            altitude = value
        elif key == "GPSAltitudeRef":
            altitude_ref = value

    if latitude and latitude_ref and longitude and longitude_ref:
        latitude = _convert_to_degrees(latitude)
        if latitude_ref != "N":
            latitude *= -1

        longitude = _convert_to_degrees(longitude)
        if longitude_ref != "E":
            longitude *= -1

        altitude = float(altitude)

        return latitude, longitude, altitude
    else:
        return None


def _convert_to_degrees(value):
    """Converts GPS coordinates from degrees, minutes, seconds to decimal degrees."""
    degrees, minutes, seconds = value
    return degrees + minutes / 60.0 + seconds / 3600.0


def _get_tag_value(exif_data, tag_name):
    if exif_data is None:
        return None
    
    for tag, value in exif_data.items():
        decoded = TAGS.get(tag, tag)
        if decoded == tag_name:
            return value


def _get_datetime_from_gps_info(gps_info):
    gps_date = datetime.strptime(gps_info['GPSDateStamp'], '%Y:%m:%d').date()
    hour = int(gps_info['GPSTimeStamp'][0])
    minute = int(gps_info['GPSTimeStamp'][1])
    second = int(gps_info['GPSTimeStamp'][2])
    gps_time = time(hour, minute, second)
    return datetime.combine(gps_date, gps_time)

