import time
import unittest

from astropy import units

from goksis import Camera
from goksis.errors import Identity
from goksis.utils import CameraSize, CameraTemperature, CameraPixelSize, CameraBin, CameraSubframe


class TestCamera(unittest.TestCase):
    def test_wrong_connection(self):
        with self.assertRaises(Identity):
            _ = Camera("127.0.0.2", 11111, 0)

    def test_connection(self):
        _ = Camera("127.0.0.1", 11111, 0)

    def test_driver(self):
        camera = Camera("127.0.0.1", 11111, 0)

        self.assertIsInstance(camera.driver, str)

    def test_description(self):
        camera = Camera("127.0.0.1", 11111, 0)

        self.assertIsInstance(camera.description(), dict)

    def test_is_connected(self):
        camera = Camera("127.0.0.1", 11111, 0)

        self.assertTrue(camera.is_connected())

    def test_get_size(self):
        camera = Camera("127.0.0.1", 11111, 0)

        size = camera.get_size()
        self.assertIsInstance(size, CameraSize)
        self.assertIsInstance(size.width, units.Quantity)
        self.assertIsInstance(size.height, units.Quantity)

    def test_get_temperature(self):
        camera = Camera("127.0.0.1", 11111, 0)

        temperature = camera.get_temperature()
        self.assertIsInstance(temperature, CameraTemperature)
        self.assertIsInstance(temperature.chip, units.Quantity)
        self.assertIsInstance(temperature.ambient, units.Quantity)

    def test_get_cooler_power(self):
        camera = Camera("127.0.0.1", 11111, 0)

        cooler_power = camera.get_cooler_power()
        self.assertIsInstance(cooler_power, units.Quantity)

    def test_get_gain(self):
        camera = Camera("127.0.0.1", 11111, 0)

        gain = camera.get_gain()
        self.assertIsInstance(gain, units.Quantity)

    def test_get_pixel_size(self):
        camera = Camera("127.0.0.1", 11111, 0)

        pixel_size = camera.get_pixel_size()
        self.assertIsInstance(pixel_size, CameraPixelSize)
        self.assertIsInstance(pixel_size.width, units.Quantity)
        self.assertIsInstance(pixel_size.height, units.Quantity)

    def test_get_progress(self):
        camera = Camera("127.0.0.1", 11111, 0)

        progress = camera.get_progress()
        self.assertIsInstance(progress, units.Quantity)

    def test_get_bin(self):
        camera = Camera("127.0.0.1", 11111, 0)

        bin_shape = camera.get_bin()
        self.assertIsInstance(bin_shape, CameraBin)
        self.assertIsInstance(bin_shape.x, units.Quantity)
        self.assertIsInstance(bin_shape.y, units.Quantity)

    def test_get_subframe(self):
        camera = Camera("127.0.0.1", 11111, 0)

        subframe_shape = camera.get_subframe()
        self.assertIsInstance(subframe_shape, CameraSubframe)
        self.assertIsInstance(subframe_shape.x, units.Quantity)
        self.assertIsInstance(subframe_shape.y, units.Quantity)
        self.assertIsInstance(subframe_shape.w, units.Quantity)
        self.assertIsInstance(subframe_shape.h, units.Quantity)

    def test_is_cooler_on(self):
        camera = Camera("127.0.0.1", 11111, 0)

        is_cooler_on = camera.is_cooler_on()
        self.assertIsInstance(is_cooler_on, bool)

    def test_is_available(self):
        camera = Camera("127.0.0.1", 11111, 0)

        is_available = camera.is_available()
        self.assertIsInstance(is_available, bool)

    def test_get_status(self):
        camera = Camera("127.0.0.1", 11111, 0)

        self.assertIsInstance(camera.get_status(), str)

    def test_set_bin(self):
        camera = Camera("127.0.0.1", 11111, 0)

        factor = 4

        camera.set_bin(factor)
        camera.start_exposure(0.1)
        binned_image = camera.get_image(wait=True)

        camera.set_bin(1)

        shape = camera.get_size()
        binned_x, binned_y = binned_image.data().shape
        self.assertEqual(shape.width.value, binned_x * factor)
        self.assertEqual(shape.height.value, binned_y * factor)

    def test_reset_bin(self):
        camera = Camera("127.0.0.1", 11111, 0)

        factor = 4

        camera.set_bin(factor)
        camera.reset_bin()
        camera.start_exposure(0.1)
        binned_image = camera.get_image(wait=True)

        shape = camera.get_size()
        binned_x, binned_y = binned_image.data().shape
        self.assertEqual(shape.width.value * factor, binned_x * factor)
        self.assertEqual(shape.height.value * factor, binned_y * factor)

    def test_set_subframe(self):
        camera = Camera("127.0.0.1", 11111, 0)

        camera.set_subframe(1, 1, 100, 100)
        cropped_subframe = camera.get_subframe()
        self.assertEqual(cropped_subframe.x.value, 1)
        self.assertEqual(cropped_subframe.y.value, 1)
        self.assertEqual(cropped_subframe.w.value, 100)
        self.assertEqual(cropped_subframe.h.value, 100)

    def test_activate_cooler(self):
        camera = Camera("127.0.0.1", 11111, 0)

        self.assertFalse(camera.is_cooler_on())
        camera.activate_cooler()
        self.assertTrue(camera.is_cooler_on())
        camera.toggle_cooler()
        self.assertFalse(camera.is_cooler_on())
        camera.toggle_cooler()
        self.assertTrue(camera.is_cooler_on())
        camera.deactivate_cooler()
        self.assertFalse(camera.is_cooler_on())

    def test_set_temperature(self):
        camera = Camera("127.0.0.1", 11111, 0)

        original_set_temperature = camera.get_set_temperature()

        camera.set_temperature(-10)
        set_set_temperature = camera.get_set_temperature()
        self.assertEqual(set_set_temperature.value, -10)

        camera.set_temperature(original_set_temperature)
        reset_set_temperature = camera.get_set_temperature()
        self.assertEqual(reset_set_temperature.value, original_set_temperature)

    def test_abort_exposure(self):
        camera = Camera("127.0.0.1", 11111, 0)

        camera.start_exposure(20)
        time.sleep(1)
        camera.abort_exposure()
