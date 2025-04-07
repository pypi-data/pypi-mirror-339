import json
import logging
from dataclasses import dataclass
from logging import Logger
from typing import Optional, List

from alpaca import discovery
from astropy.wcs import WCS

import numpy as np
from astropy import units
from astropy.coordinates import AltAz, SkyCoord

from goksis.errors import DeviceNotConnected



@dataclass
class WeatherElement:
    value: units.Quantity
    last_seen: units.Quantity


@dataclass
class WeatherValues:
    cloudCov: Optional[WeatherElement] = WeatherElement(np.nan * units.pct, np.nan * units.second)
    dewPt: Optional[WeatherElement] = WeatherElement(np.nan * units.deg_C, np.nan * units.second)
    humidity: Optional[WeatherElement] = WeatherElement(np.nan * units.pct, np.nan * units.second)
    pressure: Optional[WeatherElement] = WeatherElement(np.nan * units.pascal, np.nan * units.second)
    rainRt: Optional[WeatherElement] = WeatherElement(np.nan * units.mm / units.hour, np.nan * units.second)
    skyBri: Optional[WeatherElement] = WeatherElement(np.nan * units.lx, np.nan * units.second)
    skyQual: Optional[WeatherElement] = WeatherElement(units.Magnitude(np.nan) * units.arcsec ** -2,
                                                       np.nan * units.second)
    skyTemp: Optional[WeatherElement] = WeatherElement(np.nan * units.deg_C, np.nan * units.second)
    seeing: Optional[WeatherElement] = WeatherElement(np.nan * units.arcsec, np.nan * units.second)
    temp: Optional[WeatherElement] = WeatherElement(np.nan * units.deg_C, np.nan * units.second)
    windDir: Optional[WeatherElement] = WeatherElement(np.nan * units.deg, np.nan * units.second)
    windGus: Optional[WeatherElement] = WeatherElement(np.nan * units.m / units.second, np.nan * units.second)
    windSpd: Optional[WeatherElement] = WeatherElement(np.nan * units.m / units.second, np.nan * units.second)

    def __str__(self):
        fields = {k: v for k, v in self.__dict__.items() if not np.isnan(v.value)}
        return f"WeatherValues({', '.join(f'{k}={v}' for k, v in fields.items())})"

    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class CameraSize:
    width: units.Quantity
    height: units.Quantity


@dataclass
class CameraPixelSize:
    width: units.Quantity
    height: units.Quantity


@dataclass
class CameraTemperature:
    chip: units.Quantity
    ambient: units.Quantity


@dataclass
class CameraBin:
    x: units.Quantity
    y: units.Quantity


@dataclass
class CameraSubframe:
    x: units.Quantity
    y: units.Quantity
    w: units.Quantity
    h: units.Quantity


@dataclass
class FocuserPosition:
    step: int
    dist: units.Quantity


def compute_wcs(focal_length_mm: float, pixel_size_micron: tuple[float, float], image_size: tuple[int, int],
                center_ra: float, center_dec: float) -> WCS:
    """
    Compute the World Coordinate System (WCS) for a telescope-CCD system with potentially different pixel widths and heights.

    The function calculates the transformation from pixel coordinates to celestial coordinates
    based on the telescope's focal length, pixel size, and image dimensions.

    Parameters:
        focal_length_mm (float): Focal length of the telescope in millimeters.
        pixel_size_micron (tuple[float, float]): Pixel size in microns (µm) as (width, height).
        image_size (tuple[int, int]): Tuple containing (width, height) in pixels.
        center_ra (float): Right Ascension (RA) of the image center in degrees.
        center_dec (float): Declination (Dec) of the image center in degrees.

    Returns:
        WCS: Astropy WCS object with computed header containing coordinate transformation details.
    """
    pixel_size_mm_x = pixel_size_micron[0] / 1000
    pixel_size_mm_y = pixel_size_micron[1] / 1000
    pixel_scale_x = (pixel_size_mm_x / focal_length_mm) * 206.265
    pixel_scale_y = (pixel_size_mm_y / focal_length_mm) * 206.265

    wcs = WCS(naxis=2)
    wcs.wcs.crpix = [image_size[0] / 2, image_size[1] / 2]
    wcs.wcs.cdelt = [-pixel_scale_x / 3600, pixel_scale_y / 3600]
    wcs.wcs.crval = [center_ra, center_dec]
    wcs.wcs.ctype = ["RA---TAN", "DEC--TAN"]

    return wcs


def nmap_v4() -> List[str]:
    return discovery.search_ipv4()


def nmap_v6() -> List[str]:
    return discovery.search_ipv6()


@dataclass
class TelescopePosition:
    altaz: AltAz
    equatorial: SkyCoord


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "filename": record.filename,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage()
        }
        return json.dumps(log_data)


class Fixer:
    @staticmethod
    def logger(logger: Optional[Logger] = None):
        if logger is not None:
            return logger

        new_logger = logging.getLogger()
        new_logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(JSONFormatter())

        new_logger.addHandler(console_handler)

        return new_logger


class Checker:
    @staticmethod
    def device_connected(func):
        def wrapper(self, *args, **kwargs):
            if not self.is_connected():
                raise DeviceNotConnected("The device is not connected")
            return func(self, *args, **kwargs)

        return wrapper
