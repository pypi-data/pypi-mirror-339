import unittest
from goksis import FilterWheel
from goksis.errors import Identity


class TestFilterWheel(unittest.TestCase):
    def test_wrong_connection(self):
        with self.assertRaises(Identity):
            _ = FilterWheel("127.0.0.2", 11111, 0)

    def test_connection(self):
        _ = FilterWheel("127.0.0.1", 11111, 0)

    def test_driver(self):
        filter_wheel = FilterWheel("127.0.0.1", 11111, 0)

        self.assertIsInstance(filter_wheel.driver, str)

    def test_description(self):
        filter_wheel = FilterWheel("127.0.0.1", 11111, 0)

        self.assertIsInstance(filter_wheel.description(), dict)

    def test_is_connected(self):
        filter_wheel = FilterWheel("127.0.0.1", 11111, 0)

        self.assertTrue(filter_wheel.is_connected())

    def test_get_focuser_offset(self):
        filter_wheel = FilterWheel("127.0.0.1", 11111, 0)

        self.assertIsInstance(filter_wheel.get_focuser_offset(), tuple)

    def test_get_names(self):
        filter_wheel = FilterWheel("127.0.0.1", 11111, 0)

        self.assertIsInstance(filter_wheel.get_names(), list)

    def test_named_offset(self):
        filter_wheel = FilterWheel("127.0.0.1", 11111, 0)

        self.assertIsInstance(filter_wheel.named_offset(), dict)

    def test_get_number_of_slots(self):
        filter_wheel = FilterWheel("127.0.0.1", 11111, 0)

        self.assertIsInstance(filter_wheel.get_number_of_slots(), int)

    def test_get_position(self):
        filter_wheel = FilterWheel("127.0.0.1", 11111, 0)

        self.assertIsInstance(filter_wheel.get_position(), int)

    def test_get_current_filter(self):
        filter_wheel = FilterWheel("127.0.0.1", 11111, 0)

        self.assertIsInstance(filter_wheel.get_current_filter(), str)

    def test_set_position(self):
        filter_wheel = FilterWheel("127.0.0.1", 11111, 0)

        current_pos = filter_wheel.get_position()
        filter_wheel.set_position(current_pos + 1, wait=True)
        new_pos = filter_wheel.get_position()
        self.assertEqual(current_pos + 1, new_pos)

    def test_move(self):
        filter_wheel = FilterWheel("127.0.0.1", 11111, 0)

        current_pos = filter_wheel.get_position()
        filter_wheel.move(2, wait=True)
        new_pos = filter_wheel.get_position()
        self.assertEqual((current_pos + 2) % filter_wheel.get_number_of_slots(), new_pos)

    def test_next(self):
        filter_wheel = FilterWheel("127.0.0.1", 11111, 0)

        current_pos = filter_wheel.get_position()
        filter_wheel.next(wait=True)
        new_pos = filter_wheel.get_position()
        self.assertEqual((current_pos + 1) % filter_wheel.get_number_of_slots(), new_pos)

    def test_previous(self):
        filter_wheel = FilterWheel("127.0.0.1", 11111, 0)

        current_pos = filter_wheel.get_position()
        filter_wheel.previous(wait=True)
        new_pos = filter_wheel.get_position()
        self.assertEqual((current_pos - 1) % filter_wheel.get_number_of_slots(), new_pos)
