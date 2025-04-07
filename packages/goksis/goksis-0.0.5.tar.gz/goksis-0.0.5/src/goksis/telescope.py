import time
from logging import Logger
from typing import Optional, Dict, Union, Literal, Any

from alpaca.telescope import Telescope as Ascom
from alpaca.exceptions import NotImplementedException, ParkedException, InvalidOperationException, \
    InvalidValueException
from alpaca.telescope import DriveRates

import numpy as np
from astropy import units
from astropy.coordinates import AltAz, SkyCoord, EarthLocation
from astropy.time import Time

from goksis.errors import NotAvailable, AlreadyIs, Identity, WrongSelect
from goksis.models import Device
from goksis.utils import Fixer, TelescopePosition, Checker


def check_parked(func):
    def wrapper(self, *args, **kwargs):
        if self.device.CanPark:
            if self.is_parked():
                self.logger.error("Telescope is parked")
                raise NotAvailable("Telescope is parked")
        return func(self, *args, **kwargs)

    return wrapper


class Telescope(Device):
    def __init__(self, address: str, port: int, device_no: int = 0, protocol: str = 'http',
                 logger: Optional[Logger] = None):
        self.logger = Fixer.logger(logger)

        try:
            self.device = Ascom(f'{address}:{port}', device_no, protocol=protocol)
            _ = self.device.Connected

        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        self.lower_limit = np.nan * units.deg

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(@: '{id(self)}', driver:'{self.device}')"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.device}')"

    @property
    def lower_limit(self) -> units.Quantity:
        """
        Returns the lower limit of the telescope.

        Returns
        -------
        units.Quantity
            The altitude of the lower limit
        """
        return self.__lower_limit

    @lower_limit.setter
    def lower_limit(self, value: Union[float, units.Quantity]) -> None:
        if isinstance(value, units.Quantity):
            if not value.unit.is_equivalent(units.deg):
                raise ValueError(f"{value} is not a valid unit")
            self.__lower_limit = value
        else:
            self.__lower_limit = value * units.deg

    def disable_lower_limit(self) -> None:
        """
        Resets the lower limit of the telescope
        """
        self.lower_limit = np.nan * units.deg

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

        try:
            area = self.device.ApertureArea
        except Exception as e:
            self.logger.warning("Cannot get ApertureArea")
            area = np.nan

        try:
            diameter = self.device.ApertureDiameter
        except:
            self.logger.warning("Cannot get ApertureDiameter")
            diameter = np.nan

        try:
            focal_length = self.device.FocalLength
        except:
            self.logger.warning("Cannot get FocalLength")
            focal_length = np.nan

        return {
            "node": self.driver,
            "description": self.device.Description,
            "driver": self.device.DriverInfo,
            "driver_version": self.device.DriverVersion,
            "mount_type": self.describe_mount_type(),
            "optics": {
                "aperture": {
                    "area": area * units.m ** 2,
                    "diameter": diameter * units.m
                },
                "focal_length": focal_length * units.m
            },
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
    @property
    def now(self) -> Time:
        """
        Rerurns the current time

        Returns
        -------
        Time
            An astropy time object of current time

        Raises
        ------
        Identity
            All other errors
        """
        try:
            return Time(self.device.UTCDate, format='datetime', scale='utc')
        except Exception as e:
            self.logger.warning(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def get_mount_type(self) -> int:
        """
        Returns mount type of device

        Returns
        -------
        int
            The type of the mount

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")
        try:
            return int(self.device.AlignmentMode)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def describe_mount_type(self) -> str:
        """
        Returns description of mount type of device

        Returns
        -------
        str
            The description of mount type of device

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        return str(
            [
                "Altitude-Azimuth alignment",
                "Equatorial (Not German)",
                "German Equatorial"
            ][self.get_mount_type()]
        )

    @Checker.device_connected
    def get_location(self) -> EarthLocation:
        try:
            latitude = self.device.SiteLatitude
            longitude = self.device.SiteLongitude
            height = self.device.SiteElevation
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")
        return EarthLocation(lat=latitude * units.degree, lon=longitude * units.degree, height=height * units.m)

    @Checker.device_connected
    def get_current_position(self) -> TelescopePosition:
        """
        Returns current position of device

        Returns
        -------
        TelescopePosition
            The position of the device both in Equatorial and Horizontal

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When cannot get any position
        """
        self.logger.info("Starting")

        try:
            alt = self.device.Altitude * units.degree
            az = self.device.Azimuth * units.degree
        except Exception as e:
            self.logger.warning(f"{e}")
            alt = np.nan * units.deg
            az = np.nan * units.deg

        try:
            ra = self.device.RightAscension * units.hourangle
            dec = self.device.Declination * units.degree

        except Exception as e:
            self.logger.warning(f"{e}")
            ra = np.nan * units.hourangle
            dec = np.nan * units.deg

        if np.isnan(ra) and np.isnan(dec) and np.isnan(alt) and np.isnan(az):
            self.logger.error("Cannot get Equatorial or Horizontal coordinates")
            raise NotAvailable("Cannot get Equatorial or Horizontal coordinates")

        return TelescopePosition(
            AltAz(alt=alt, az=az),
            SkyCoord(ra=ra, dec=dec)
        )

    @Checker.device_connected
    def is_parked(self) -> bool:
        """
        Check if the device is parked

        Returns
        -------
        bool
            True if the device is parked

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
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
            Waits until the device is parked

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device cannot park
        AlreadyIs
            When the device is already parked
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if not self.device.CanPark:
            self.logger.error("Cannot park")
            raise NotAvailable("Cannot park")

        if self.is_parked():
            self.logger.error("Is already parked")
            raise AlreadyIs("Is already parked")

        try:
            self.device.Park()
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        if wait:
            self.wait()

    @Checker.device_connected
    def unpark(self, wait: bool = False) -> None:
        """
        Unparks the device

        Parameters
        ----------
        wait : bool
            Waits until the device unparked

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device cannot unpark
        AlreadyIs
            When the device is already unparked
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if not self.device.CanUnpark:
            self.logger.error("Cannot unpark")
            raise NotAvailable("Cannot unpark")

        if not self.is_parked():
            self.logger.error("Is already unparked")
            raise AlreadyIs("Is already unparked")

        try:
            self.device.Unpark()
        except NotImplementedException:
            self.logger.error("Cannot Unpark")
            raise NotAvailable("Cannot Unpark")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        if wait:
            self.wait()

    @Checker.device_connected
    def is_at_home(self) -> bool:
        """
        Check if the device is at home

        Returns
        -------
        bool
            True if the device is at home

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
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
    @check_parked
    def find_home(self, wait: bool = False) -> None:
        """
        Finds home of the device

        Parameters
        ----------
        wait : bool
            Waits until the device finds home

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device cannot find home
        NotAvailable
            Whe the device is parked
        AlreadyIs
            When the device is already at home
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
        except NotImplementedException:
            self.logger.error("Cannot find home")
            raise NotAvailable("Cannot find home")
        except InvalidOperationException:
            self.logger.error("Telescope is parked")
            raise NotAvailable("Telescope is parked")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        if wait:
            self.wait()

    @Checker.device_connected
    @check_parked
    def set_park(self) -> None:
        """
        Sets the devices current position to the park position

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device cannot set park
        NotAvailable
            When the device is moving
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if not self.device.CanSetPark:
            self.logger.error("Cannot set park")
            raise NotAvailable("Cannot set park")

        if self.is_moving():
            self.logger.error("Must not moving to set park")
            raise NotAvailable("Must not moving to set park")

        try:
            self.device.SetPark()
        except NotImplementedException:
            self.logger.error("Cannot set park")
            raise NotAvailable("Cannot set park")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    @check_parked
    def set_pier_side(self, direction: Literal["EAST", "WEST"]) -> None:
        """
        Sets the devices current pier side

        Parameters
        ----------
        direction : Literal["EAST", "WEST"]
            The side that pier wanted to be set

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device is not german mount
        NotAvailable
            When the device cannot set pier side
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: direction={direction}")

        if self.get_mount_type() != 2:
            self.logger.error("Is not german mount")
            raise NotAvailable("Is not german mount")

        if not self.device.CanSetPierSide:
            self.logger.error("Cannot set pier side")
            raise NotAvailable("Cannot set pier side")

        if "EAST".startswith(direction.upper()):
            side = 0
        else:
            side = 1

        try:
            self.device.SideOfPier = side
        except NotImplementedException:
            self.logger.error("Cannot set pier side")
            raise NotAvailable("Cannot set pier side")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def get_pier_side(self) -> int:
        """
        Returns pier side status of the device

        Returns
        -------
        int
            The side of the pier of the device

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device is not german mount
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if self.get_mount_type() != 2:
            self.logger.error("Is not german mount")
            raise NotAvailable("Is not german mount")

        try:
            return int(self.device.SideOfPier)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    @check_parked
    def toggle_pier_side(self) -> None:
        """
        Toggles the pier side of the device

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if self.get_mount_type() != 2:
            self.logger.error("Is not german mount")
            raise NotAvailable("Is not german mount")

        try:
            self.device.SideOfPier = int(not self.get_pier_side())
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def describe_pier_side(self) -> str:
        """
        Describes the pier side of the device

        Returns
        -------
        str
            The description of the pier side of the device
        """
        self.logger.info("Starting")

        try:
            return str(["EAST", "WEST"][self.get_pier_side()])
        except Exception as e:
            self.logger.warning(f"{e}")
            return "Unknown"

    @Checker.device_connected
    def is_tracking(self) -> bool:
        """
        Checks if the device is tracking

        Returns
        -------
        bool
            True if the device is tracking

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device cannot track
        Identity
            All other errors
        """
        self.logger.info(f"Starting")

        if not self.device.CanSetTracking:
            self.logger.error("Cannot set tracking")
            raise NotAvailable("Cannot set tracking")

        try:
            return bool(self.device.Tracking)
        except NotImplementedException:
            self.logger.error("Cannot set tracking")
            raise NotAvailable("Cannot set tracking")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    @check_parked
    def start_tracking(self) -> None:
        """
        Starts the tracking for the device

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device cannot track
        AlreadyIs
            When the device is already tacking
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if not self.device.CanSetTracking:
            self.logger.error("Cannot track")
            raise NotAvailable("Cannot track")

        if self.is_tracking():
            self.logger.error("Is already tracking")
            raise AlreadyIs("Is already tracking")

        try:
            self.device.Tracking = True
        except NotImplementedException:
            self.logger.error("Cannot set tracking")
            raise NotAvailable("Cannot set tracking")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def stop_tracking(self) -> None:
        """
        Stops the tracking for the device

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device cannot track
        AlreadyIs
            When the device is already tacking
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if not self.device.CanSetTracking:
            self.logger.error("Cannot track")
            raise NotAvailable("Cannot track")

        if not self.is_tracking():
            self.logger.error("Is already not tracking")
            raise AlreadyIs("Is already not tracking")

        try:
            self.device.Tracking = False
        except NotImplementedException:
            self.logger.error("Cannot set tracking")
            raise NotAvailable("Cannot set tracking")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    @check_parked
    def toggle_tracking(self) -> None:
        """
        Toggles the tracking for the device

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device cannot track
        AlreadyIs
            When the device is already tacking
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if not self.device.CanSetTracking:
            self.logger.error("Cannot track")
            raise NotAvailable("Cannot track")

        try:
            self.device.Tracking = not self.is_tracking()
        except NotImplementedException:
            self.logger.error("Cannot set tracking")
            raise NotAvailable("Cannot set tracking")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    @check_parked
    def slew_altaz(self, coordinates: AltAz, wait: bool = False) -> None:
        """
        Slews the device to a horizontal coordinate

        Parameters
        ----------
        coordinates : AltAz
            Waits until the shutter is closed
        wait : bool
            Waits until the device slews

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device is parked
        ValueError
            When the given coordinate is not valid
        NotAvailable
            When the device cannot slew to horizontal coordinate
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: coordinates={coordinates}")

        if not np.isnan(self.lower_limit.value):
            if coordinates.alt < self.lower_limit:
                raise ValueError("Coordinate is out of range")

        if not self.device.CanSlewAltAz:
            self.logger.error("Cannot slew to horizontal coordinates")
            raise NotAvailable("Cannot slew to horizontal coordinates")

        try:
            self.device.SlewToAltAzAsync(coordinates.az.degree, coordinates.alt.degree)
        except ParkedException:
            self.logger.error("Telescope is parked")
            raise NotAvailable("Telescope is parked")
        except InvalidValueException:
            self.logger.error("Invalid coordinates")
            raise ValueError("Invalid coordinates")
        except NotImplementedException:
            self.logger.error("Cannot slew to horizontal coordinates")
            raise NotAvailable("Cannot slew to horizontal coordinates")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        if wait:
            self.wait()

    @Checker.device_connected
    @check_parked
    def slew_radec(self, coordinates: SkyCoord, wait: bool = False):
        """
        Slews the device to an equatorial coordinate

        Parameters
        ----------
        coordinates : AltAz
            Waits until the shutter is closed
        wait : bool
            Waits until the device slews

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device is parked
        ValueError
            When the given coordinate is not valid
        NotAvailable
            When the device cannot slew to horizontal coordinate
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: coordinates={coordinates}")
        frame = AltAz(obstime=self.now, location=self.get_current_location())
        altaz = coordinates.transform_to(frame)

        if not np.isnan(self.lower_limit.value):
            if altaz.az.degree.value < self.lower_limit:
                raise ValueError("Coordinate is out of range")

        if not self.device.CanSlew:
            self.logger.error("Cannot slew to equatorial coordinates")
            raise NotAvailable("Cannot slew to equatorial coordinates")

        try:
            self.device.SlewToCoordinates(coordinates.ra.hourangle, coordinates.dec.degree)
        except ParkedException:
            self.logger.error("Telescope is parked")
            raise NotAvailable("Telescope is parked")
        except InvalidValueException:
            self.logger.error("Invalid coordinates")
            raise ValueError("Invalid coordinates")
        except NotImplementedException:
            self.logger.error("Cannot slew to equatorial coordinates")
            raise NotAvailable("Cannot slew to equatorial coordinates")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        if wait:
            self.wait()

    @Checker.device_connected
    def slew_name(self, name: str, wait: bool = False):
        try:
            sky_coordinate = SkyCoord.from_name(name)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        self.slew_radec(sky_coordinate, wait=wait)

    @Checker.device_connected
    @check_parked
    def slew(self, to: Union[AltAz, SkyCoord, str], wait: bool = False):
        """
        Slews the device to an equatorial or a horizontal coordinate

        Parameters
        ----------
        to : Union[AltAz, SkyCoord, str]
            Either object ro coordinate to slew to
        wait : bool
            Waits until the device slews

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device is parked
        ValueError
            When the given coordinate is not valid
        NotAvailable
            When the device cannot slew to horizontal coordinate
        NotAvailable
            When the device cannot slew to equatorial coordinate
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: to={to}")

        if isinstance(to, AltAz):
            self.slew_altaz(to, wait=wait)
        elif isinstance(to, SkyCoord):
            self.slew_radec(to, wait=wait)
        else:
            self.slew_name(to, wait=wait)

    @Checker.device_connected
    def is_slewing(self) -> bool:
        """
        Checks if the device is slewing

        Returns
        -------
        bool
            True if the device is slewing

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
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
            True if the device is moving

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        return bool(self.is_tracking() or self.is_slewing())

    @Checker.device_connected
    def get_tracking_rate(self) -> int:
        """
        Returns the tracking rate

        Returns
        -------
        int
            The tracking rate as integer

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device cannot track
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if not self.device.CanSetTracking:
            self.logger.error("Cannot track")
            raise NotAvailable("Cannot track")

        try:
            return int(self.device.TrackingRate)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def describe_tracking_rate(self) -> str:
        """
        Returns a description of the tracking rate

        Returns
        -------
        int
            The description of the tracking rate
        """
        self.logger.info("Starting")

        try:
            return str(["SIDERAL", "LUNAR", "SOLAR", "KING"][self.get_tracking_rate()])
        except Exception as e:
            self.logger.warning(f"{e}")
            return "Unknown"

    @Checker.device_connected
    def set_tracking_rate(self,
                          rate: Union[Literal["SIDEREAL", "LUNAR", "SOLAR", "KING"], Literal[0, 1, 2, 3]]) -> None:
        """
        Sets the tracking rate

        Parameters
        ----------
        rate : Union[Literal["SIDEREAL", "LUNAR", "SOLAR", "KING"], Literal[0, 1, 2, 3]]
            The tracking rate as either integer ot string

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device cannot track
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: rate={rate}")

        if not self.device.CanSetTracking:
            self.logger.error("Cannot track")
            raise NotAvailable("Cannot track")

        if isinstance(rate, str):
            if "SIDERAL".startswith(rate.upper()):
                tracking_rate = DriveRates.driveSidereal
            elif "LUNAR".startswith(rate.upper()):
                tracking_rate = DriveRates.driveLunar
            elif "SOLAR".startswith(rate.upper()):
                tracking_rate = DriveRates.driveSolar
            elif "KING".startswith(rate.upper()):
                tracking_rate = DriveRates.driveKing
            else:
                self.logger.error("Unknown track rate")
                raise WrongSelect("Unknown track rate")
        else:
            if rate == 0:
                tracking_rate = DriveRates.driveSidereal
            elif rate == 1:
                tracking_rate = DriveRates.driveLunar
            elif rate == 2:
                tracking_rate = DriveRates.driveSolar
            else:
                tracking_rate = DriveRates.driveKing

        try:
            self.device.TrackingRate = tracking_rate
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    @check_parked
    def abort(self) -> None:
        """
        Aborts ongoing slew

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device is not slewing
        NotAvailable
            When the device is parked
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if not self.is_slewing():
            self.logger.error("Is not slewing")
            raise NotAvailable("Is not slewing")

        try:
            self.device.AbortSlew()
        except InvalidValueException:
            self.logger.error("Telescope is parked")
            raise NotAvailable("Telescope is parked")
        except NotImplementedException:
            self.logger.error("Cannot abort slew")
            raise NotAvailable("Cannot abort slew")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    @check_parked
    def sync_altaz(self, coordinates: AltAz) -> None:
        """
        Synchronizes to a horizontal coordinate

        Parameters
        ----------
        coordinates : AltAz
            The coordinate that the device is going to be synchronized to

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device is slewing
        NotAvailable
            When the device cannot synchronize to horizontal coordinate
        NotAvailable
            When the device is parked
        ValueError
            When the coordinates is invalid
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: coordinates={coordinates}")

        if self.is_slewing():
            self.logger.error("Cannot sync while slewing")
            raise NotAvailable("Cannot sync while slewing")

        if self.device.CanSyncAltAz:
            self.logger.error("Cannot sync to AltAz")
            raise NotAvailable("Cannot sync to AltAz")

        if self.is_tracking():
            self.logger.error("Telescope is tracking")
            raise NotAvailable("Telescope is tracking")

        try:
            self.device.SyncToAltAz(coordinates.az.degree, coordinates.alt.degree)
        except ParkedException:
            self.logger.error("Telescope is parked")
            raise NotAvailable("Telescope is parked")
        except InvalidValueException:
            self.logger.error("Invalid coordinates")
            raise ValueError("Invalid coordinates")
        except NotImplementedException:
            self.logger.error("Cannot sync to AltAz")
            raise NotAvailable("Cannot sync to AltAz")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    @check_parked
    def sync_radec(self, coordinates: SkyCoord) -> None:
        """
        Synchronizes to an equatorial coordinate

        Parameters
        ----------
        coordinates : SkyCoord
            The coordinate that the device is going to be synchronized to

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When the device is slewing
        NotAvailable
            When the device cannot synchronize to equatorial coordinate
        NotAvailable
            When the device is parked
        ValueError
            When the coordinates is invalid
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: coordinates={coordinates}")

        if self.is_slewing():
            self.logger.error("Cannot sync while slewing")
            raise NotAvailable("Cannot sync while slewing")

        if not self.device.CanSync:
            self.logger.error("Cannot sync")
            raise NotAvailable("Cannot sync")

        if self.is_tracking():
            self.logger.error("Telescope is Tracking")
            raise NotAvailable("Telescope is Tracking")

        try:
            self.device.SyncToCoordinates(coordinates.ra.hourangle, coordinates.dec.degree)
        except ParkedException:
            self.logger.error("Telescope is parked")
            raise NotAvailable("Telescope is parked")
        except InvalidValueException:
            self.logger.error("Invalid coordinates")
            raise ValueError("Invalid Coordinates")
        except NotImplementedException:
            self.logger.error("Cannot sync to Coordinates")
            raise NotAvailable("Cannot sync to Coordinates")
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def wait(self, tolerance=0.1):
        """
        Sleeps until the device is not moving

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
