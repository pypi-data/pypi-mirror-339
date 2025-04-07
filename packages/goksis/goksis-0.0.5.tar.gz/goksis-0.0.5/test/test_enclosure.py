import time
import unittest
from unittest import skip

from astropy import units
from astropy.coordinates import AltAz

from goksis import Enclosure
from goksis.errors import Identity, AlreadyIs


class TestEnclosure(unittest.TestCase):
    def test_wrong_connection(self):
        with self.assertRaises(Identity):
            _ = Enclosure("127.0.0.2", 11111, 0)

    def test_connection(self):
        _ = Enclosure("127.0.0.1", 11111, 0)

    def test_driver(self):
        enclosure = Enclosure("127.0.0.1", 11111, 0)

        self.assertIsInstance(enclosure.driver, str)

    def test_description(self):
        enclosure = Enclosure("127.0.0.1", 11111, 0)

        self.assertIsInstance(enclosure.description(), dict)

    def test_is_connected(self):
        enclosure = Enclosure("127.0.0.1", 11111, 0)

        self.assertTrue(enclosure.is_connected())

    def test_get_shutter(self):
        enclosure = Enclosure("127.0.0.1", 11111, 0)

        self.assertIsInstance(enclosure.get_shutter(), int)

    def test_describe_shutter(self):
        enclosure = Enclosure("127.0.0.1", 11111, 0)

        self.assertIsInstance(enclosure.describe_shutter(), str)

    def test_is_shutter_moving(self):
        enclosure = Enclosure("127.0.0.1", 11111, 0)

        self.assertIsInstance(enclosure.is_shutter_moving(), bool)

    def test_open_shutter(self):
        enclosure = Enclosure("127.0.0.1", 11111, 0)

        if enclosure.get_shutter() in [2, 0]:
            enclosure.close_shutter(wait=True)

        enclosure.open_shutter()
        self.assertEqual(enclosure.get_shutter(), 2)
        self.assertTrue(enclosure.is_shutter_moving())
        while enclosure.is_shutter_moving():
            time.sleep(0.1)

        enclosure.close_shutter(wait=True)

    def test_close_shutter(self):
        enclosure = Enclosure("127.0.0.1", 11111, 0)

        if enclosure.get_shutter() in [3, 1]:
            enclosure.open_shutter(wait=True)

        enclosure.close_shutter()
        self.assertEqual(enclosure.get_shutter(), 3)
        self.assertTrue(enclosure.is_shutter_moving())
        while enclosure.is_shutter_moving():
            time.sleep(0.1)

    def test_toggle_shutter(self):
        enclosure = Enclosure("127.0.0.1", 11111, 0)

        if enclosure.get_shutter() in [2, 0]:
            enclosure.close_shutter(wait=True)

        enclosure.toggle_shutter(wait=True)
        self.assertEqual(enclosure.get_shutter(), 0)
        enclosure.toggle_shutter(wait=True)
        self.assertEqual(enclosure.get_shutter(), 1)

    def test_get_current_position(self):
        enclosure = Enclosure("127.0.0.1", 11111, 0)

        pos = enclosure.get_current_position()
        self.assertIsInstance(pos, AltAz)

    def test_is_parked(self):
        enclosure = Enclosure("127.0.0.1", 11111, 0)

        if not enclosure.is_parked():
            enclosure.park(wait=True)

        self.assertTrue(enclosure.is_parked())

    def test_park_not_parked(self):
        enclosure = Enclosure("127.0.0.1", 11111, 0)

        if enclosure.is_parked():
            current_pos = enclosure.get_current_position()
            new_position = AltAz(alt=current_pos.alt, az=current_pos.az + 15 * units.deg)
            enclosure.slew(new_position, wait=True)

        self.assertFalse(enclosure.is_parked())
        enclosure.park(wait=True)

    def test_park_already_parked(self):
        enclosure = Enclosure("127.0.0.1", 11111, 0)

        if not enclosure.is_parked():
            enclosure.park(wait=True)

        with self.assertRaises(AlreadyIs):
            enclosure.park(wait=True)

    @skip("Cannot test")
    def test_park_set_park(self):
        enclosure = Enclosure("127.0.0.1", 11111, 0)

        if not enclosure.is_parked():
            enclosure.park(wait=True)

        current_pos = enclosure.get_current_position()
        new_position = AltAz(alt=current_pos.alt, az=current_pos.az + 15 * units.deg)
        enclosure.slew(new_position, wait=True)
        enclosure.set_park()

        try:
            enclosure.park(wait=True)
        except AlreadyIs:
            pass

        self.assertEqual(
            enclosure.get_current_position(), new_position
        )

        enclosure.slew(current_pos, wait=True)
        enclosure.set_park()

    def test_test_find_home(self):
        enclosure = Enclosure("127.0.0.1", 11111, 0)

        if enclosure.is_at_home():
            current_pos = enclosure.get_current_position()
            new_position = AltAz(alt=current_pos.alt, az=current_pos.az + 15 * units.deg)
            enclosure.slew(new_position, wait=True)

        enclosure.find_home()

    def test_sync_azimuth(self):
        enclosure = Enclosure("127.0.0.1", 11111, 0)

        current_pos = enclosure.get_current_position()
        new_position = AltAz(alt=current_pos.alt, az=current_pos.az + 15 * units.deg)

        enclosure.sync_azimuth(new_position.az)

    def test_abort(self):
        enclosure = Enclosure("127.0.0.1", 11111, 0)

        current_pos = enclosure.get_current_position()
        new_position = AltAz(alt=current_pos.alt, az=current_pos.az + 180 * units.deg)
        enclosure.slew(new_position)
        time.sleep(0.5)
        enclosure.abort()
        time.sleep(0.5)

        self.assertNotEqual(new_position.az.degree, enclosure.get_current_position().az.degree)
