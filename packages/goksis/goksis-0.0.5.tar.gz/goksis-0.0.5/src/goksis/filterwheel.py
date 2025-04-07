import time
from logging import Logger
from typing import Optional, Dict, Any, Tuple, Union, List

from alpaca.filterwheel import FilterWheel as Ascom

from goksis import Focuser
from goksis.errors import Identity, NotAvailable
from goksis.models import Device
from goksis.utils import Fixer, Checker


class FilterWheel(Device):
    def __init__(self, address: str, port: int, device_no: int = 0, protocol: str = 'http',
                 focuser: Optional[Focuser] = None, logger: Optional[Logger] = None):
        self.logger = Fixer.logger(logger)

        try:
            self.device = Ascom(f'{address}:{port}', device_no, protocol=protocol)
            self.focuser = focuser
            _ = self.device.Connected

        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(@: '{id(self)}', driver:'{self.device}')"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.device}')"

    @Checker.device_connected
    def __set_offset(self, target_filter: Union[str, int]) -> None:
        """
        Moves connected focuser with the available offset.

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if self.focuser is None:
            return
        try:
            if isinstance(target_filter, str):
                target_filter_to_use = target_filter
            else:
                target_filter_to_use = self.get_names()[target_filter]

            offsets = self.named_offset()
            current_offset = offsets[self.get_current_filter()]
            next_offset = offsets[target_filter_to_use]
            absolute_amount = next_offset - current_offset
            self.focuser.move(absolute_amount, wait=True)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

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

        return bool(self.device.Connected)

    @Checker.device_connected
    def get_focuser_offset(self) -> Tuple[int, ...]:
        """
        Returns the focuser offset for the device

        Returns
        -------
        Tuple[int, ...]
            Tuple of offsets

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            return tuple(each for each in self.device.FocusOffsets)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def get_names(self) -> List[str]:
        """
        Returns the names filters on the device

        Returns
        -------
        List[str]
            List of names of filters on the device

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            return list(self.device.Names)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def named_offset(self) -> Dict[str, int]:
        """
        Returns dictionary of named offsets of each filter on the device

        Returns
        -------
        Dict[str, int]
            Dictionary of named offsets of each filter on the device

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            return dict(zip(self.get_names(), self.get_focuser_offset()))
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def get_number_of_slots(self) -> int:
        """
        Return the number of filters on the device

        Returns
        -------
        int
            The number of filters on the device

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        return len(self.get_names())

    @Checker.device_connected
    def get_position(self) -> int:
        """
        Return the position of the device

        Returns
        -------
        int
            The position of the device

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            return int(self.device.Position)
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
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        return bool(self.get_position() == -1)

    @Checker.device_connected
    def is_available(self) -> bool:
        """
        Checks if the device is available

        Returns
        -------
        bool
            True if the device is available

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if self.focuser is not None:
            if not self.focuser.is_available():
                self.logger.error("Connected focuser is not available")
                return False

        return not self.is_moving()

    @Checker.device_connected
    def get_current_filter(self) -> str:
        """
        Returns the current filter name on the device

        Returns
        -------
        str
            The name of the filter on the focal plate on the device

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        NotAvailable
            When device is moving
        Identity
            All other errors
        """
        self.logger.info("Starting")

        if self.is_moving():
            self.logger.error("Is not available")
            raise NotAvailable("Is not available")

        try:
            return str(self.get_names()[self.get_position()])
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def set_position(self, pos: Union[int, str], wait: bool = False) -> None:
        """
        Set the position of the device

        Parameters
        ----------
        pos: Union[int, str]
            The filter that wanted to be on the focal plate. Either name or order
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
            When the device is moving
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: pos={pos}")

        if self.is_moving():
            self.logger.error("Cannot move while it's moving")
            raise NotAvailable("Cannot move while it's moving")

        if isinstance(pos, int):
            position = pos % self.get_number_of_slots()
        else:
            position = self.get_names().index(pos)

        try:
            self.__set_offset(position)

            self.device.Position = position
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        if wait:
            self.wait()

    @Checker.device_connected
    def move(self, step: int, wait: bool = False) -> None:
        """
         Moves the filter on the device

        Parameters
        ----------
        step: int
            The number of steps to move
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
            When the device is moving
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: step={step}")

        self.set_position((self.get_position() + step) % self.get_number_of_slots(), wait=wait)

    @Checker.device_connected
    def next(self, wait: bool = False) -> None:
        """
         Moves to the next filter. `FilterWheel.move(1, wait=wait)`

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
            When the device is moving
        Identity
            All other errors
        """
        self.logger.info("Starting")

        self.move(1, wait=wait)

    @Checker.device_connected
    def previous(self, wait: bool = False) -> None:
        """
         Moves to the previous filter. Not that most of FilterWheel's cannot move backward.
         In that case the wheel would do a full rotation. `FilterWheel.move(1, wait=wait)`

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
            When the device is moving
        Identity
            All other errors
        """
        self.logger.info("Starting")

        self.move(-1, wait=wait)

    @Checker.device_connected
    def wait(self, tolerance=0.1) -> None:
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

        while self.is_moving():
            time.sleep(tolerance)
