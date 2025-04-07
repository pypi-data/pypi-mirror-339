import time
from logging import Logger
from typing import Optional, Dict, Any, Union

from alpaca.dome import Dome
from alpaca.exceptions import NotImplementedException, ParkedException, SlavedException
import numpy as np
from astropy import units
from astropy.coordinates import AltAz

from goksis.errors import NotAvailable, AlreadyIs, Identity
from goksis.models import Device
from goksis.utils import Fixer, Checker


class Enclosure(Device):
    def __init__(self, address: str, port: int, device_no: int = 0, protocol: str = 'http',
                 logger: Optional[Logger] = None):
        self.logger = Fixer.logger(logger)

        try:
            self.device = Dome(f'{address}:{port}', device_no, protocol=protocol)
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
            When device is not connected
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
            When device is not connected
        """
        self.logger.info("Starting")

        return {
            "node": self.driver,
            "description": self.device.Description,
            "driver": self.device.DriverInfo,
            "driver_version": self.device.DriverVersion,
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
        try:
            return bool(self.device.Connected)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def get_shutter(self) -> int:
        """
        Returns shutter's status of the device

        Returns
        -------
        int
            The status of the shutter

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When device has not shutter
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            return int(self.device.ShutterStatus)
        except NotImplementedException:
            self.logger.error("Does not have a shutter")
            raise NotAvailable("Does not have a shutter")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def describe_shutter(self) -> str:
        """
        Return the description of the shutter

        Returns
        -------
        str
            The description of the shutter

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When device has not shutter
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            status: int = self.get_shutter()
            return ["Open", "Close", "Opening", "Closing", "Intervention"][status]
        except Exception as e:
            self.logger.warning(f"{e}")
            return "Unknown"

    @Checker.device_connected
    def is_shutter_moving(self) -> bool:
        """
        Checks if the shutter is moving

        Returns
        -------
        bool
            True if the shutter is moving

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When device has not shutter
        Identity
            All other errors
        """
        self.logger.info("Starting")

        return bool(self.get_shutter() > 1)

    @Checker.device_connected
    def open_shutter(self, wait: bool = False) -> None:
        """
        Opens the shutter

        Parameters
        ----------
        wait : bool
            Waits until the shutter is open

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When shutter is neither close nor is closing
        NotAvailable
            When device has not shutter
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if self.get_shutter() not in [3, 1, 4]:
            self.logger.error("Is neither close nor is closing")
            raise NotAvailable("Is neither close nor is closing")

        try:
            self.device.OpenShutter()

            if wait:
                while self.is_shutter_moving():
                    time.sleep(0.1)

        except NotImplementedException:
            self.logger.error("Does not have a shutter")
            raise NotAvailable("Does not have a shutter")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def close_shutter(self, wait: bool = False) -> None:
        """
        Opens the shutter

        Parameters
        ----------
        wait : bool
            Waits until the shutter is closed

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When shutter is neither open nor is opening
        NotAvailable
            When device has not shutter
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if self.get_shutter() not in [2, 0, 4]:
            self.logger.error("Is neither open nor is opening")
            raise NotAvailable("Is neither open nor is opening")

        try:
            self.device.CloseShutter()

            if wait:
                while self.is_shutter_moving():
                    time.sleep(0.1)

        except NotImplementedException:
            self.logger.error("Does not have a shutter")
            raise NotAvailable("Does not have a shutter")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def toggle_shutter(self, wait: bool = False) -> None:
        """
        Toggles the shutter. Opens it if it's closed, closes it if it's open

        Parameters
        ----------
        wait : bool
            Waits until the shutter is closed

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When device has not shutter
        Identity
            All other errors
        """
        self.logger.info("Starting")
        if self.get_shutter() in [1, 2]:
            self.open_shutter(wait=wait)
        else:
            self.close_shutter(wait=wait)

    @Checker.device_connected
    def get_current_position(self) -> AltAz:
        """
        Return's the current position of the device

        Returns
        -------
        AltAz
            position of the device in Horizontal Coordinates

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When the device cannot return both Altitude and Azimuth
        """
        self.logger.info("Starting")

        try:
            altitude = self.device.Altitude
        except NotImplementedException:
            self.logger.warning("Cannot get Altitude")
            altitude = np.nan

        try:
            azimuth = self.device.Azimuth
        except NotImplementedException:
            self.logger.warning("Cannot get Azimuth")
            azimuth = np.nan

        if np.isnan(altitude) and np.isnan(azimuth):
            self.logger.warning("Cannot get coordinates of the device")
            raise NotAvailable("Cannot get coordinates of the device")

        return AltAz(
            alt=altitude * units.degree,
            az=azimuth * units.degree
        )

    @Checker.device_connected
    def is_parked(self) -> bool:
        """
        Checks if the device is parked

        Returns
        -------
        bool
            True if the device is parked

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When the device cannot park
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if not self.device.CanPark:
            self.logger.error("Cannot park")
            raise NotAvailable("Cannot park")

        try:
            return bool(self.device.AtPark)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def park(self, wait: bool = False) -> None:
        """
        Parks the device

        Parameters
        ----------
        wait : bool
            Waits until the shutter is closed

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When the device cannot park
        AlreadyIs
            When the device is already parked
        NotAvailable
            When the device is slaved
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if self.is_parked():
            self.logger.error("Is already parked")
            raise AlreadyIs("Is already parked")

        try:
            self.device.Park()

            if wait:
                self.wait()

        except NotImplementedException:
            self.logger.error("Cannot park")
            raise NotAvailable("Cannot park")
        except ParkedException:
            self.logger.error("Is already parked")
            raise AlreadyIs("Is already parked")
        except SlavedException:
            self.logger.error("Is slaved")
            raise NotAvailable("Is slaved")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def set_park(self) -> None:
        """
        Sets the current position of the device to be the park position

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When the device cannot set park
        NotAvailable
            When the device cannot park
        NotAvailable
            When the device is slaved
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if not self.device.CanSetPark:
            self.logger.error("Cannot set park")
            raise NotAvailable("Cannot set park")

        try:
            self.device.SetPark()
        except NotImplementedException:
            self.logger.error("Cannot park")
            raise NotAvailable("Cannot park")
        except SlavedException:
            self.logger.error("Is slaved")
            raise NotAvailable("Is slaved")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def is_at_home(self) -> bool:
        """
        Checks if the device is at home

        Returns
        -------
        bool
            True if the device is at home


        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            return bool(self.device.AtHome)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def find_home(self, wait: bool = False) -> None:
        """
        Finds home

        Parameters
        ----------
        wait : bool
            Waits until the shutter is closed

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When the device cannot find home
        AlreadyIs
            When the device is already at home
        NotAvailable
            When the device is slaved
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if not self.device.CanFindHome:
            self.logger.error("Cannot find home")
            raise NotAvailable("Cannot find home")

        if self.is_at_home():
            self.logger.error("Is already at home")
            raise AlreadyIs("Is already at home")

        try:
            self.device.FindHome()
        except SlavedException:
            self.logger.error("Is slaved")
            raise NotAvailable("Is slaved")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        if wait:
            self.wait()

    @Checker.device_connected
    def sync_azimuth(self, azimuth: Union[int, float, units.Quantity]) -> None:
        """
        Synchronizes azimuth

        Parameters
        ----------
        azimuth : Union[int, float, units.Quantity]
            Azimuth to be synchronized to

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When the device cannot synchronize
        NotAvailable
            When the device is slaved
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: azimuth={azimuth}")

        if not self.device.CanSyncAzimuth:
            self.logger.error("Cannot sync")
            raise NotAvailable("Cannot sync")

        if self.device.Slaved:
            self.logger.error("Is slaved")
            raise NotAvailable("Is slaved")

        if isinstance(azimuth, units.Quantity):

            if not azimuth.unit.is_equivalent(units.deg):
                raise ValueError(f"{azimuth} is not a valid unit")

            azimuth = azimuth.to(units.degree).value

        try:
            self.device.SyncToAzimuth(azimuth)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def slew(self, altaz: AltAz, wait: bool = False) -> None:
        """
        Slews the device

        Parameters
        ----------
        altaz : AltAz
            The horizontal coordinates to slew to
        wait : bool
            Waits until the shutter is closed

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When the device is slaved
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: altaz={altaz}")

        if self.device.Slaved:
            self.logger.error("Is slaved")
            raise NotAvailable("Is slaved")

        if self.device.CanSetAzimuth:
            try:
                self.device.SlewToAzimuth(altaz.az.degree)
            except Exception as e:
                self.logger.error(f"{e}")
                raise Identity(f"{e}")

        if self.device.CanSetAltitude:
            try:
                self.device.SlewToAltitude(altaz.alt.degree)
            except Exception as e:
                self.logger.error(f"{e}")
                raise Identity(f"{e}")

        if wait:
            self.wait()

    @Checker.device_connected
    def is_slewing(self) -> bool:
        """
        Checks if the device is slewing

        Returns
        -------
        bool
            True if device is slewing

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            return bool(self.device.Slewing)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def is_moving(self) -> bool:
        """
        Checks if the device is moving

        Returns
        -------
        bool
            True if device is moving

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        return bool(self.is_slewing() or self.is_shutter_moving())

    @Checker.device_connected
    def abort(self) -> None:
        """
        Aborts the slewing action

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        AlreadyIs
            When the device already is not moving
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if not self.is_slewing():
            self.logger.error("Is not moving")
            raise AlreadyIs("Is not moving")

        try:
            self.device.AbortSlew()
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def wait(self, tolerance: float = 0.1) -> None:
        """
        Sleeps until the device is not slewing

        Parameters
        ----------
        tolerance : float
            the amount of seconds to sleep before recheck if the device is available

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
        self.logger.info(f"Starting with parameters: tolerance={tolerance}")

        while self.is_slewing():
            time.sleep(tolerance)
