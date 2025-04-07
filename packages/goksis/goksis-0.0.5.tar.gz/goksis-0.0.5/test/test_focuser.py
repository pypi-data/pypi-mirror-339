import unittest

from astropy import units

from goksis import Focuser
from goksis.errors import Identity
from goksis.utils import FocuserPosition


class TestFocuser(unittest.TestCase):
    def test_wrong_connection(self):
        with self.assertRaises(Identity):
            _ = Focuser("127.0.0.2", 11111, 0)

    def test_connection(self):
        _ = Focuser("127.0.0.1", 11111, 0)

    def test_driver(self):
        focuser = Focuser("127.0.0.1", 11111, 0)

        self.assertIsInstance(focuser.driver, str)

    def test_description(self):
        focuser = Focuser("127.0.0.1", 11111, 0)

        self.assertIsInstance(focuser.description(), dict)

    def test_is_connected(self):
        focuser = Focuser("127.0.0.1", 11111, 0)

        self.assertTrue(focuser.is_connected())

    def test_get_current_position(self):
        focuser = Focuser("127.0.0.1", 11111, 0)

        self.assertIsInstance(focuser.get_current_position(), FocuserPosition)

    def test_step_size(self):
        focuser = Focuser("127.0.0.1", 11111, 0)

        self.assertIsInstance(focuser.step_size(), units.Quantity)

    def test_goto(self):
        focuser = Focuser("127.0.0.1", 11111, 0)

        current_position = focuser.get_current_position()

        next_position = current_position.dist - 2000 * units.micron
        focuser.goto(next_position, wait=True)

        self.assertEqual(focuser.get_current_position().dist, next_position)

    def test_move(self):
        focuser = Focuser("127.0.0.1", 11111, 0)

        current_position = focuser.get_current_position()
        amount = 100 * units.micron
        focuser.move(amount, wait=True)

        self.assertEqual(focuser.get_current_position().dist, current_position.dist + amount)

    def test_halt(self):
        focuser = Focuser("127.0.0.1", 11111, 0)

        current_position = focuser.get_current_position()
        amount = 1000 * units.micron
        focuser.move(amount)
        focuser.halt()

        self.assertNotEqual(focuser.get_current_position().dist, current_position.dist + amount)

    def test_get_temperature(self):
        focuser = Focuser("127.0.0.1", 11111, 0)

        self.assertIsInstance(focuser.get_temperature(), units.Quantity)
