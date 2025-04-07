from __future__ import annotations

from abc import abstractmethod, ABC

from typing import Dict, Any
from alpaca.device import Device as AlpacaDevice


class Device(ABC):
    device: AlpacaDevice

    @abstractmethod
    def description(self) -> Dict[str, Any]:
        """Retrieve the device description"""

    @abstractmethod
    def is_connected(self) -> bool:
        """Checks if the device is connected"""
