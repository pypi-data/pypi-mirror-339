import unittest

from astropy import units
from astropy.coordinates import AltAz, SkyCoord

from goksis import Telescope
from goksis.errors import Identity
from goksis.utils import TelescopePosition


class TestTelescope(unittest.TestCase):
    def test_wrong_connection(self):
        with self.assertRaises(Identity):
            _ = Telescope("127.0.0.2", 11111, 0)

    def test_connection(self):
        _ = Telescope("127.0.0.1", 11111, 0)

    def test_driver(self):
        telescope = Telescope("127.0.0.1", 11111, 0)

        self.assertIsInstance(telescope.driver, str)

    def test_description(self):
        telescope = Telescope("127.0.0.1", 11111, 0)

        self.assertIsInstance(telescope.description(), dict)

    def test_is_connected(self):
        telescope = Telescope("127.0.0.1", 11111, 0)

        self.assertTrue(telescope.is_connected())

    def test_get_mount_type(self):
        telescope = Telescope("127.0.0.1", 11111, 0)

        self.assertIsInstance(telescope.get_mount_type(), int)

    def test_describe_mount_type(self):
        telescope = Telescope("127.0.0.1", 11111, 0)

        self.assertIsInstance(telescope.describe_mount_type(), str)

    def test_get_current_position(self):
        telescope = Telescope("127.0.0.1", 11111, 0)

        self.assertIsInstance(telescope.get_current_position(), TelescopePosition)

    def test_is_parked(self):
        telescope = Telescope("127.0.0.1", 11111, 0)

        if not telescope.is_parked():
            telescope.park(wait=True)

        self.assertTrue(telescope.is_parked())

    def test_park(self):
        telescope = Telescope("127.0.0.1", 11111, 0)

        if not telescope.is_parked():
            telescope.park(wait=True)

        telescope.unpark(wait=True)
        self.assertFalse(telescope.is_parked())
        telescope.park(wait=True)
        self.assertTrue(telescope.is_parked())

    def test_is_at_home(self):
        telescope = Telescope("127.0.0.1", 11111, 0)

        if telescope.is_parked():
            telescope.unpark(wait=True)

        if telescope.is_at_home():
            current_pos = telescope.get_current_position()
            new_position = AltAz(alt=current_pos.altaz.alt, az=current_pos.altaz.az + 15 * units.deg)
            telescope.slew(new_position, wait=True)

        self.assertFalse(telescope.is_at_home())
        telescope.find_home(wait=True)
        self.assertTrue(telescope.is_at_home())

    def test_get_tracking_rate(self):
        telescope = Telescope("127.0.0.1", 11111, 0)

        self.assertIsInstance(telescope.get_tracking_rate(), int)

    def test_start_tracking(self):
        telescope = Telescope("127.0.0.1", 11111, 0)

        if not telescope.is_tracking():
            telescope.start_tracking()

        self.assertTrue(telescope.is_tracking())
        telescope.stop_tracking()
        self.assertFalse(telescope.is_tracking())

        telescope.toggle_tracking()
        self.assertTrue(telescope.is_tracking())
        telescope.toggle_tracking()
        self.assertFalse(telescope.is_tracking())

    def test_describe_tracking_rate(self):
        telescope = Telescope("127.0.0.1", 11111, 0)

        self.assertIsInstance(telescope.describe_tracking_rate(), str)

    def test_set_tracking_rate(self):
        telescope = Telescope("127.0.0.1", 11111, 0)

        tracking_rate = telescope.get_tracking_rate()
        telescope.set_tracking_rate((tracking_rate + 1) % 4)
        self.assertNotEqual(telescope.get_tracking_rate(), tracking_rate)
        telescope.set_tracking_rate(0)

    def test_abort(self):
        telescope = Telescope("127.0.0.1", 11111, 0)

        if telescope.is_parked():
            telescope.unpark(wait=True)

        current_pos = telescope.get_current_position()

        new_position = SkyCoord(ra=current_pos.equatorial.ra + 10 * units.degree, dec=current_pos.equatorial.dec)

        telescope.slew(new_position)
        telescope.abort()
        self.assertNotEqual(telescope.get_current_position().equatorial, new_position)

        telescope.park(wait=True)
