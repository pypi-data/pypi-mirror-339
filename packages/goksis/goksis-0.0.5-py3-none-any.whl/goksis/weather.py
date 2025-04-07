from collections.abc import Callable
from logging import Logger
from typing import Optional, Dict, Any, Union, List, Literal

from alpaca.exceptions import NotImplementedException
from alpaca.observingconditions import ObservingConditions
import numpy as np
from astropy import units

from goksis.errors import Identity
from goksis.models import Device
from goksis.utils import Fixer, WeatherElement, WeatherValues, Checker

AllowedWeatherElements = Literal[
    "cloud_coverage", "dew_point", "humidity", "pressure", "rain_rate", "sky_brightness", "sky_quality",
    "sky_temperature", "seeing", "temperature", "wind_direction", "wind_gust", "wind_speed"
]
AllowedWeather = Union[AllowedWeatherElements, List[AllowedWeatherElements]]


class Weather(Device):
    def __init__(self, address: str, port: int, device_no: int = 0, protocol: str = 'http',
                 logger: Optional[Logger] = None):
        self.logger = Fixer.logger(logger)

        try:
            self.device = ObservingConditions(f'{address}:{port}', device_no, protocol=protocol)
            _ = self.device.Connected

        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(@: '{id(self)}', driver:'{self.device}')"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.device}')"

    @property
    @Checker.device_connected
    def driver(self) -> str:
        """
        Returns the driver name

        Returns
        -------
        str
            The name of the driver

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        """
        self.logger.info("Starting")

        return str(self.device.Description)

    @Checker.device_connected
    def description(self) -> Dict[str, Any]:
        """
        Returns the driver description

        Returns
        -------
        Dict[str, Any]
            The driver description

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        """
        self.logger.info("Starting")

        return {
            "node": self.driver,
            "description": self.device.Description,
            "driver": self.device.DriverInfo,
            "driver_version": self.device.DriverVersion
        }

    def is_connected(self) -> bool:
        """
        Checks if the device is connected

        Returns
        -------
        bool
            Connected status of the device

        Raises
        ------
        Identity
            All other errors
        """
        self.logger.info("Starting")

        return bool(self.device.Connected)

    @Checker.device_connected
    def refresh(self) -> None:
        """
        Refreshes the data stored is the device

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            self.device.Refresh()
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def get_cloud_coverage(self) -> WeatherElement:
        """
        Returns the cloud coverage

        Returns
        -------
        WeatherElement
            The cloud coverage

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            value = self.device.CloudCover
            last_seen = self.device.TimeSinceLastUpdate("CloudCover")
        except NotImplementedException:
            self.logger.warning("Cannot get CloudCover")
            value = np.nan
            last_seen = np.nan
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        return WeatherElement(
            value * units.pct,
            last_seen * units.second
        )

    @Checker.device_connected
    def get_dew_point(self) -> WeatherElement:
        """
        Returns the dew point

        Returns
        -------
        WeatherElement
            The dew point

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            value = self.device.DewPoint
            last_seen = self.device.TimeSinceLastUpdate("DewPoint")
        except NotImplementedException:
            self.logger.warning("Cannot get DewPoint")
            value = np.nan
            last_seen = np.nan
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        return WeatherElement(
            value * units.deg_C,
            last_seen * units.second
        )

    @Checker.device_connected
    def get_humidity(self) -> WeatherElement:
        """
        Returns the humidity

        Returns
        -------
        WeatherElement
            The humidity

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            value = self.device.Humidity
            last_seen = self.device.TimeSinceLastUpdate("Humidity")
        except NotImplementedException:
            self.logger.warning("Cannot get Humidity")
            value = np.nan
            last_seen = np.nan
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        return WeatherElement(
            value * units.pct,
            last_seen * units.second
        )

    @Checker.device_connected
    def get_pressure(self) -> WeatherElement:
        """
        Returns the pressure

        Returns
        -------
        WeatherElement
            The pressure

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            value = self.device.Pressure
            last_seen = self.device.TimeSinceLastUpdate("Pressure")
        except NotImplementedException:
            self.logger.warning("Cannot get Pressure")
            value = np.nan
            last_seen = np.nan
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        return WeatherElement(
            value * 100 * units.pascal,
            last_seen * units.second
        )

    @Checker.device_connected
    def get_rain_rate(self) -> WeatherElement:
        """
        Returns the rain rate

        Returns
        -------
        WeatherElement
            The rain rate

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            value = self.device.RainRate
            last_seen = self.device.TimeSinceLastUpdate("RainRate")
        except NotImplementedException:
            self.logger.warning("Cannot get RainRate")
            value = np.nan
            last_seen = np.nan
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        return WeatherElement(
            value * units.mm / units.hour,
            last_seen * units.second
        )

    @Checker.device_connected
    def get_sky_brightness(self) -> WeatherElement:
        """
        Returns the sky brightness

        Returns
        -------
        WeatherElement
            The sky brightness

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            value = self.device.SkyBrightness
            last_seen = self.device.TimeSinceLastUpdate("SkyBrightness")
        except NotImplementedException:
            self.logger.warning("Cannot get SkyBrightness")
            value = np.nan
            last_seen = np.nan
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        return WeatherElement(
            value * units.lx,
            last_seen * units.second
        )

    @Checker.device_connected
    def get_sky_quality(self) -> WeatherElement:
        """
        Returns the sky quality

        Returns
        -------
        WeatherElement
            The sky quality

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            value = self.device.SkyQuality
            last_seen = self.device.TimeSinceLastUpdate("SkyQuality")
        except NotImplementedException:
            self.logger.warning("Cannot get SkyQuality")
            value = np.nan
            last_seen = np.nan
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        return WeatherElement(
            units.Magnitude(value) * units.arcsec ** -2,
            last_seen * units.second
        )

    @Checker.device_connected
    def get_sky_temperature(self) -> WeatherElement:
        """
        Returns the sky temperature

        Returns
        -------
        WeatherElement
            The sky temperature

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            value = self.device.SkyTemperature
            last_seen = self.device.TimeSinceLastUpdate("SkyTemperature")
        except NotImplementedException:
            self.logger.warning("Cannot get SkyTemperature")
            value = np.nan
            last_seen = np.nan
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        return WeatherElement(
            value * units.deg_C,
            last_seen * units.second
        )

    @Checker.device_connected
    def get_seeing(self) -> WeatherElement:
        """
        Returns the seeing

        Returns
        -------
        WeatherElement
            The seeing

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            value = self.device.StarFWHM
            last_seen = self.device.TimeSinceLastUpdate("StarFWHM")
        except NotImplementedException:
            self.logger.warning("Cannot get StarFWHM")
            value = np.nan
            last_seen = np.nan
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        return WeatherElement(
            value * units.arcsec,
            last_seen * units.second
        )

    @Checker.device_connected
    def get_temperature(self) -> WeatherElement:
        """
        Returns the temperature

        Returns
        -------
        WeatherElement
            The temperature

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            value = self.device.Temperature
            last_seen = self.device.TimeSinceLastUpdate("Temperature")
        except NotImplementedException:
            self.logger.warning("Cannot get Temperature")
            value = np.nan
            last_seen = np.nan
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        return WeatherElement(
            value * units.deg_C,
            last_seen * units.second
        )

    @Checker.device_connected
    def get_wind_direction(self) -> WeatherElement:
        """
        Returns the wind direction

        Returns
        -------
        WeatherElement
            The wind direction

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            value = self.device.WindDirection
            last_seen = self.device.TimeSinceLastUpdate("WindDirection")
        except NotImplementedException:
            self.logger.warning("Cannot get WindDirection")
            value = np.nan
            last_seen = np.nan
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        return WeatherElement(
            value * units.deg,
            last_seen * units.second
        )

    @Checker.device_connected
    def get_wind_gust(self) -> WeatherElement:
        """
        Returns the wind gust

        Returns
        -------
        WeatherElement
            The wind gust

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            value = self.device.WindGust
            last_seen = self.device.TimeSinceLastUpdate("WindGust")
        except NotImplementedException:
            self.logger.warning("Cannot get WindGust")
            value = np.nan
            last_seen = np.nan
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        return WeatherElement(
            value * units.m / units.second,
            last_seen * units.second
        )

    @Checker.device_connected
    def get_wind_speed(self) -> WeatherElement:
        """
        Returns the wind speed

        Returns
        -------
        WeatherElement
            The wind speed

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            value = self.device.WindSpeed
            last_seen = self.device.TimeSinceLastUpdate("WindSpeed")
        except NotImplementedException:
            self.logger.warning("Cannot get WindSpeed")
            value = np.nan
            last_seen = np.nan
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        return WeatherElement(
            value * units.m / units.second,
            last_seen * units.second
        )

    @Checker.device_connected
    def get(self, what: Optional[AllowedWeather] = None) -> Union[WeatherValues, WeatherElement]:
        """
        Returns Every available measurment

        Returns
        -------
        Union[WeatherValues, WeatherElement]
            Either a WeatherElement or a WeatherValues

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: what={what}")

        methods: Dict[str, Callable[..., WeatherElement]] = {
            "cloudCov": self.get_cloud_coverage,
            "dewPt": self.get_dew_point,
            "humidity": self.get_humidity,
            "pressure": self.get_pressure,
            "rainRt": self.get_rain_rate,
            "skyBri": self.get_sky_brightness,
            "skyQual": self.get_sky_quality,
            "skyTemp": self.get_sky_temperature,
            "seeing": self.get_seeing,
            "temp": self.get_temperature,
            "windDir": self.get_wind_direction,
            "windGus": self.get_wind_gust,
            "windSpd": self.get_wind_speed
        }

        if what is None:
            values = {}
            for attr, the_value in methods.items():
                values[attr] = the_value()
            return WeatherValues(**values)
        else:
            if isinstance(what, str):
                return methods[what]()
            else:
                values = {}
                for attr, the_value in methods.items():
                    if attr in what:
                        values[attr] = the_value()
                return WeatherValues(**values)
