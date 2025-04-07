import time
from logging import Logger
from typing import Optional, Any, Dict, Union

from alpaca.focuser import Focuser as Ascom
import numpy as np
from astropy import units

from goksis.errors import Identity, NotAvailable
from goksis.models import Device
from goksis.utils import Fixer, FocuserPosition, Checker


class Focuser(Device):
    def __init__(self, address: str, port: int, device_no: int = 0, protocol: str = 'http',
                 logger: Optional[Logger] = None):
        self.logger = Fixer.logger(logger)

        try:
            self.device = Ascom(f'{address}:{port}', device_no, protocol=protocol)
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

        return bool(self.device.Connected)

    @Checker.device_connected
    def get_current_position(self) -> FocuserPosition:
        """
        Returns the current position of the device

        Returns
        -------
        FocuserPosition
            The position of the device as both physical and steps

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            pos = int(self.device.Position)
        except Exception as e:
            self.logger.warning(f"{e}")
            pos = np.nan

        return FocuserPosition(pos, pos * self.step_size())

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

        try:
            return bool(self.device.IsMoving)
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

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

        try:
            return not self.is_moving()
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def step_size(self) -> units.Quantity:
        """
        Returns the physical length of each step on the device

        Returns
        -------
        units.Quantity
            The physical length of each step on the device

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        Identity
            All other errors
        """
        self.logger.info("Starting")

        try:
            step_size = float(self.device.StepSize)
        except Exception as e:
            self.logger.warning(f"{e}")
            step_size = np.nan

        return step_size * units.micron

    @Checker.device_connected
    def goto(self, position: Union[int, units.Quantity], wait: bool = False) -> None:
        """
        Sets the position of the device


        Parameters
        ----------
        position : Union[int, units.Quantity]
            The position to be set to
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
            When the focuser is moving
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: position={position}")

        if self.is_moving():
            self.logger.error("Focuser is moving")
            raise NotAvailable("Focuser is moving")

        if isinstance(position, units.Quantity):

            if not position.unit.is_equivalent(units.m):
                raise ValueError(f"{position} is not a valid unit")

            position_to_use = (position.to(units.micron) / self.step_size()).value
        else:
            position_to_use = position

        try:
            if self.device.Absolute:
                self.device.Move(int(position_to_use))
            else:
                self.device.Move(int(self.get_current_position().step - position_to_use))
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        if wait:
            self.wait()

    @Checker.device_connected
    def move(self, amount: Union[int, units.Quantity], wait: bool = False) -> None:
        """
        Moves the device


        Parameters
        ----------
        amount : Union[int, units.Quantity]
            The amount to move the device
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
            When the focuser is moving
        Identity
            All other errors
        """
        self.logger.info(f"Starting with parameters: amount={amount}")

        if self.is_moving():
            self.logger.error("Focuser is moving")
            raise NotAvailable("Focuser is moving")

        if isinstance(amount, units.Quantity):

            if not amount.unit.is_equivalent(units.m):
                raise ValueError(f"{amount} is not a valid unit")

            amount_to_use = (amount.to(units.micron) / self.step_size()).value
        else:
            amount_to_use = amount

        if amount_to_use >= self.device.MaxIncrement:
            self.logger.error("Cannot move this much")
            raise NotAvailable("Cannot move this much")

        try:
            if self.device.Absolute:
                self.device.Move(int(self.get_current_position().step + amount_to_use))
            else:
                self.device.Move(int(amount_to_use))
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

        if wait:
            self.wait()

    @Checker.device_connected
    def halt(self) -> None:
        """
        Halts this device

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
            self.device.Halt()
        except Exception as e:
            self.logger.error(f"{e}")
            raise Identity(f"{e}")

    @Checker.device_connected
    def get_temperature(self) -> units.Quantity:
        """
        Returns the temperature of the device

        Returns
        -------
        units.Quantity
            The temperature of the device

        Raises
        ------
        DeviceNotConnected
            When device is not connected
        """
        self.logger.info("Starting")

        try:
            temperature = self.device.Temperature
        except Exception as e:
            self.logger.warning(f"{e}")
            temperature = np.nan

        return temperature * units.deg_C

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
