import time
from logging import Logger
from typing import Optional, Dict, Any, Union, Tuple

from alpaca.camera import Camera as Ascom
from alpaca.exceptions import NotImplementedException

from myraflib import Fits, FitsArray
import numpy as np
from astropy import units
from astropy.wcs import WCS

from goksis import FilterWheel
from goksis.constants import STATUS_CODES
from goksis.errors import NotFound, NotAvailable, AlreadyIs, Identity
from goksis.models import Device
from goksis.utils import Fixer, Checker, CameraSize, CameraTemperature, CameraPixelSize, CameraBin, \
    CameraSubframe, compute_wcs


class Camera(Device):
    def __init__(self, address: str, port: int, device_no: int = 0, protocol: str = 'http',
                 filter_wheel: Optional[FilterWheel] = None, logger: Optional[Logger] = None):
        self.logger = Fixer.logger(logger)

        try:
            self.device = Ascom(f'{address}:{port}', device_no, protocol=protocol)
            self.filter_wheel = filter_wheel
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
        self.logger.info(f"Starting")

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
        self.logger.info(f"Starting")

        try:
            node = self.driver
        except Exception as e:
            self.logger.warning(f"{e}")
            node = None

        try:
            description = self.device.Description
        except Exception as e:
            self.logger.warning(f"{e}")
            description = None

        try:
            driver = self.device.DriverInfo
        except Exception as e:
            self.logger.warning(f"{e}")
            driver = None

        try:
            driver_version = self.device.DriverVersion
        except Exception as e:
            self.logger.warning(f"{e}")
            driver_version = None

        try:
            sensor = self.device.SensorName
        except Exception as e:
            self.logger.warning(f"{e}")
            sensor = None

        try:
            sensor_type = self.device.SensorType
        except Exception as e:
            self.logger.warning(f"{e}")
            sensor_type = None

        return {
            "node": node,
            "description": description,
            "driver": driver,
            "driver_version": driver_version,
            "sensor": sensor,
            "sensor_type": sensor_type
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
        self.logger.info(f"Starting")
        try:
            return bool(self.device.Connected)
        except Exception as e:
            self.logger.warning(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def get_status(self) -> str:
        """
        Returns the status of the device

        Returns
        -------
        str
            Status of the device

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        """
        self.logger.info(f"Starting")

        try:
            return STATUS_CODES[int(self.device.CameraState)]
        except Exception as e:
            self.logger.error(f"{e}")
            raise NotAvailable(f"{e}")

    @Checker.device_connected
    def get_size(self) -> CameraSize:
        """
        Returns size of the device in pixels

        Returns
        -------
        CameraSize
            The shape of the device in pixels

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        """
        self.logger.info(f"Starting")

        try:
            width = self.device.CameraXSize * units.pix
        except Exception as e:
            self.logger.warning(f"{e}")
            width = np.nan * units.pix

        try:
            height = self.device.CameraYSize * units.pix
        except Exception as e:
            self.logger.warning(f"{e}")
            height = np.nan * units.pix

        return CameraSize(width, height)

    @Checker.device_connected
    def get_temperature(self) -> CameraTemperature:
        """
        Returns temperature of the device

        Returns
        -------
        CameraTemperature
            Temperature of the device

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        """
        self.logger.info(f"Starting")

        try:
            chip = self.device.CCDTemperature
        except NotImplementedException:
            self.logger.warning("Cannot get CCDTemperature")
            chip = np.nan

        try:
            ambient = self.device.HeatSinkTemperature
        except NotImplementedException:
            self.logger.warning("Cannot get HeatSinkTemperature")
            ambient = np.nan

        return CameraTemperature(
            chip * units.deg_C,
            ambient * units.deg_C
        )

    @Checker.device_connected
    def get_cooler_power(self) -> units.Quantity:
        """
        Returns cooler power of the device

        Returns
        -------
        units.Quantity
            Returns cooler power of the device as percentage

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        """
        self.logger.info(f"Starting")

        if self.device.CanGetCoolerPower:
            return self.device.CoolerPower * units.percent

        return np.nan * units.percent

    @Checker.device_connected
    def get_gain(self) -> units.Quantity:
        """
        Returns device's gain value

        Returns
        -------
        units.Quantity
            Returns device's gain value as Electrons/ADU

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        """
        self.logger.info(f"Starting")

        try:
            adu = self.device.ElectronsPerADU
        except NotImplementedException:
            self.logger.warning("Cannot get ElectronsPerADU")
            adu = np.nan

        return adu * units.electron / units.adu

    @Checker.device_connected
    def get_pixel_size(self) -> CameraPixelSize:
        """
        Returns the size of each pixel of the device

        Returns
        -------
        CameraPixelSize
            The size of each pixel of the device in micron

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        """
        self.logger.info(f"Starting")

        try:
            x_size = self.device.PixelSizeX
        except NotImplementedException:
            self.logger.warning("Cannot get PixelSizeX")
            x_size = np.nan

        try:
            y_size = self.device.PixelSizeY
        except NotImplementedException:
            self.logger.warning("Cannot get PixelSizeY")
            y_size = np.nan

        return CameraPixelSize(x_size * units.micron, y_size * units.micron)

    @Checker.device_connected
    def get_progress(self) -> units.Quantity:
        """
        Returns progress of the device

        Returns
        -------
        CameraPixelSize
            Progress of the device as percentage

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        """
        self.logger.info(f"Starting")

        try:
            progress = self.device.PercentCompleted
        except Exception as e:
            self.logger.warning(f"{e}")
            progress = np.nan

        return progress * units.percent

    @Checker.device_connected
    def get_bin(self) -> CameraBin:
        """
        Returns the bin status of the device

        Returns
        -------
        CameraBin
            The bin status of the device

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        """
        self.logger.info(f"Starting")

        try:
            x_bin = self.device.BinX
            y_bin = self.device.BinY
        except NotImplementedException:
            self.logger.warning("Cannot get BinX/BinY")
            x_bin = 1
            y_bin = 1

        return CameraBin(x_bin * units.pix, y_bin * units.pix)

    @Checker.device_connected
    def set_bin(self, bin_value: Union[Tuple[int, int], int]) -> None:
        """
        Sets the binning of the device

        Parameters
        ----------
        bin_value : Union[Tuple[int, int], int]
            an integer of a tuple of two integers (For asymmetric)

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When asymmetric binning is not available
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: bin_value={bin_value}")

        if isinstance(bin_value, tuple):
            bin_x, bin_y = bin_value
        else:
            bin_x, bin_y = bin_value, bin_value

        try:
            if bin_x != bin_y and not self.device.CanAssymetricBin:
                raise NotAvailable("Asymmetric Binning is unavailable")

            old_bin_x, old_bin_y = self.device.BinX, self.device.BinY

            self.device.BinX = bin_x
            self.device.BinY = bin_y

            self.device.NumX = max(1, (self.device.CameraXSize // bin_x))
            self.device.NumY = max(1, (self.device.CameraYSize // bin_y))

            self.device.StartX = max(0, (self.device.StartX * old_bin_x) // bin_x)
            self.device.StartY = max(0, (self.device.StartY * old_bin_y) // bin_y)

        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def reset_bin(self) -> None:
        """
        Resets the binning of the device. `Camera.set_bin(1)`

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When asymmetric binning is not available
        Identity
            All other errors
        """
        self.logger.info("Starting")
        self.set_bin(1)

    @Checker.device_connected
    def get_subframe(self) -> CameraSubframe:
        """
        Returns subframe status of teh device

        Returns
        -------
        CameraSubframe
            The subframe status of teh device

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info(f"Starting")

        try:
            x_start = self.device.StartX
            y_start = self.device.StartY
            x_num = self.device.NumX
            y_num = self.device.NumY
        except NotImplementedException:
            self.logger.warning("Cannot get StartX/StartY or NumX/NumY")
            x_start = 0
            y_start = 0
            x_num = np.nan
            y_num = np.nan
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        return CameraSubframe(
            x_start * units.pix, y_start * units.pix,
            x_num * units.pix, y_num * units.pix
        )

    @Checker.device_connected
    def set_subframe(self, x: int, y: int, w: int, h: int) -> None:
        """
        Sets subframe status of teh device

        Parameters
        ----------
        x : int
            The x value of top-left corner of the subframe
        y : int
            The y value of top-left corner of the subframe
        w : int
            The width of the subframe
        h : int
            The height of the subframe

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
        self.logger.info(f"Starting with parameters: x={x}, y={y}, w={w}, h={h}")

        try:
            self.device.StartX = x
            self.device.StartY = y
            self.device.NumX = w
            self.device.NumY = h
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def reset_subframe(self) -> None:
        """
        Resets the subframe of teh device

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
        self.logger.info(f"Starting")

        try:
            self.device.StartX = 0
            self.device.StartY = 0
            self.device.NumX = self.device.CameraXSize
            self.device.NumY = self.device.CameraYSize
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def is_cooler_on(self) -> bool:
        """
        Resets the cooler's status of the device

        Returns
        -------
        bool:
            True if cooler is on

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info(f"Starting")

        try:
            return bool(self.device.CoolerOn)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def activate_cooler(self) -> None:
        """
        Activates the cooler on the device

        Returns
        -------
        bool:
            True if cooler is on

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info(f"Starting")

        if self.is_cooler_on():
            self.logger.error("Cooler is already activated")
            raise AlreadyIs("Cooler is already activated")

        try:
            self.device.CoolerOn = True
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def deactivate_cooler(self) -> None:
        """
        Deactivates the cooler on the device

        Returns
        -------
        bool:
            True if cooler is off

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info(f"Starting")

        if not self.is_cooler_on():
            self.logger.error("Cooler is already deactivated")
            raise AlreadyIs("Cooler is already deactivated")

        try:
            self.device.CoolerOn = False
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def toggle_cooler(self) -> None:
        """
        Toggles the cooler on the device

        Returns
        -------
        bool:
            True if cooler is on

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info(f"Starting")

        try:
            self.device.CoolerOn = not self.is_cooler_on()
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def set_temperature(self, temperature: Union[int, float, units.Quantity]) -> None:
        """
        Sets temperature of the device

        Parameters
        ----------
        temperature : Union[int, float, units.Quantity]
            temperature to set

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When the device cannot set temperature
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: temperature={temperature}")

        if not self.device.CanSetCCDTemperature:
            self.logger.error("Does not support temperature setting")
            raise NotAvailable("Does not support temperature setting")

        if isinstance(temperature, units.Quantity):

            if not temperature.unit.is_equivalent(units.deg_C):
                raise ValueError(f"{temperature} is not a valid unit")

            temperature_to_set = temperature.to(
                units.deg_C, equivalencies=units.temperature()
            ).value
        else:
            temperature_to_set = temperature

        try:
            self.device.SetCCDTemperature = temperature_to_set
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def get_set_temperature(self) -> units.Quantity:
        """
        Returns the temperature set to the device

        Returns
        -------
        units.Quantity
            set temperature on the device

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When the device cannot set temperature
        Identity
            All other errors
        """
        self.logger.info(f"Starting")

        if not self.device.CanSetCCDTemperature:
            self.logger.error("Does not support temperature setting")
            raise NotAvailable("Does not support temperature setting")

        try:
            return self.device.SetCCDTemperature * units.deg_C
        except Exception as e:
            self.logger.error(f"{e}")
            return np.nan * units.deg_C

    @Checker.device_connected
    def is_cool(self, tolerance: float = 0.1) -> bool:
        """
        Check if the device's current temperature is within the specified tolerance

        Parameters
        ----------
        tolerance : float
            temperature tolerance

        Returns
        -------
        bool
            True if is cool

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When the device cannot set temperature
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: tolerance={tolerance}")

        if not self.device.CanSetCCDTemperature:
            self.logger.error("Does not support temperature setting")
            raise NotAvailable("Does not support temperature setting")

        return bool(
            abs(self.get_temperature().chip.value - self.get_set_temperature().value) < tolerance
        )

    @Checker.device_connected
    def is_available(self) -> bool:
        """
        Check if the device is available

        Returns
        -------
        bool
            True if is available

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info(f"Starting")

        return bool(self.device.CameraState == 0)

    @Checker.device_connected
    def start_exposure(self, duration: Union[int, float, units.Quantity],
                       light: bool = True, filter_order: Optional[int] = None) -> None:
        """
        Start's an exposure

        Parameters
        ----------
        duration : Union[int, float, units.Quantity]
            exposure duration
        light: bool
            True if Light (light or flat), False if (bias or dark)
        filter_order: Optional[int]
            The order of filter wheel if filter whell is available

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When the device is not available (already exposing)
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: duration={duration}, light={light}")

        if not self.is_available():
            self.logger.error(self.get_status())
            raise NotAvailable(self.get_status())

        if isinstance(duration, units.Quantity):

            if not duration.unit.is_equivalent(units.second):
                raise ValueError(f"{duration} is not a valid unit")

            duration_to_use = duration.to(units.second).value
        else:
            duration_to_use = duration

        try:

            if self.filter_wheel is not None:
                if not self.filter_wheel.is_available():
                    raise NotAvailable("Connected filter wheel is not available")

                if filter_order is not None:
                    self.filter_wheel.set_position(filter_order, wait=True)

            self.device.StartExposure(duration_to_use, light)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def is_image_ready(self) -> bool:
        """
        Returns the availability of the image

        Returns
        -------
        bool
            True if the image is ready

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        try:
            return bool(self.device.ImageReady)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def get_image(self, wait: bool = True, telescope=None) -> Union[Fits, FitsArray]:
        """
        Returns a Fits object of the Image

        Parameters
        ----------
        wait : bool
            If an exposure is ongoing wait till the end and return the image
        telescope : Telescope
            If provided it creates the WCS headers

        Returns
        -------
        Union[Fits, FitsArray]
            The Fits object of the Image

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When the device is not available (already exposing)
        Identity
            All other errors
        NotImplemented
            Right now FitsArray is not implemented
        """
        self.logger.info(f"Starting with parameters: wait={wait}")

        if wait:
            self.wait()

        if not self.is_image_ready():
            self.logger.error("No image available")
            raise NotFound("No image available")

        try:
            image = np.array(self.device.ImageArray)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        if image.ndim == 2:
            try:
                fts = Fits.from_data_header(image)
            except Exception as e:
                self.logger.error(f"{e}")
                raise Identity(f"{e}")
        else:
            self.logger.error("Fits Cube is not implemented yet")
            raise NotImplementedError("Fits Cube is not implemented yet")
        try:
            fts.hedit(
                ["s_time", "exposure", "gain"],
                [
                    self.device.LastExposureStartTime,
                    self.device.LastExposureDuration,
                    str(self.get_gain().value)
                ],
                ["UTC", (1 * units.second).unit.to_string(), self.get_gain().unit.to_string()]
            )
        except Exception as e:
            self.logger.error(f"{e}")

        if telescope is not None:
            try:
                wcs = self.wcs(telescope)
                wcs_header = wcs.to_header()
                keys = []
                values = []
                for card in wcs_header:
                    keys.append(card)
                    values.append(wcs_header[card])

                fts.hedit(keys, values)
            except Exception as e:
                self.logger.warning(f"{e}")

        return fts

    @Checker.device_connected
    def abort_exposure(self) -> None:
        """
        Aborts an ongoing exposure

        Returns
        -------
        None

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When the device does not support exposure abortion
        NotAvailable
            When the device is not exposing
        NotImplemented
            Right now FitsArray is not implemented
        Identity
            All other errors
        """
        self.logger.info(f"Starting")

        if not self.device.CanAbortExposure:
            self.logger.error("Does not support abort exposure")
            raise NotAvailable("Does not support abort exposure")

        if self.get_status() != "CameraExposing Exposure currently in progress":
            self.logger.error("Is not exposed")
            raise NotAvailable("Is not exposed")

        try:
            self.device.AbortExposure()
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def wait(self, verbose: bool = False, tolerance=0.1) -> None:
        """
        Sleeps until the device is available

        Parameters
        ----------
        verbose : bool
            If True print progress
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
        self.logger.info(f"Starting with parameters: verbose={verbose}, tolerance={tolerance}")

        while not self.is_available():
            if verbose:
                print(self.get_progress())
            time.sleep(tolerance)

    def wcs(self, telescope) -> WCS:
        """
        Creates a WCS object for the given telescope and returns it

        Parameters
        ----------
        telescope : Telescope
            The telescope object

        Returns
        -------
        WCS
            The WCS object

        Raises
        ------
        DeviceNotConnected
            When the device is not connected
        NotAvailable
            When cannot get any position
        Identity
            All other errors
        """
        self.logger.info("Starting with parameters: telescope={telescope}")

        current_position = telescope.get_current_position()
        center_ra = current_position.equatorial.ra.degree
        center_dec = current_position.equatorial.dec.degree

        focal_length = telescope.description()["optics"]["focal_length"].to(units.mm).value
        pixel_size = self.get_pixel_size()
        pixel_size_micron = pixel_size.width.to(units.micron).value, pixel_size.height.to(units.micron).value
        camera_siz = self.get_size()
        camera_siz_pixel = int(camera_siz.width.to(units.pix).value), int(camera_siz.height.to(units.pix).value)
        try:
            return compute_wcs(focal_length, pixel_size_micron, camera_siz_pixel, center_ra, center_dec)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")
