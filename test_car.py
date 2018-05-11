import math
import unittest

from car import Car
from car import InvalidDestinationError, OverTheLimitError, BadInputError, InvalidOperationError


class TestCar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.car = Car(300)
        self.car.accelerate_by(100)

    def test_set_destination(self):
        self.car.set_destination('Thessaloniki')
        self.assertEqual(self.car.distance_to_destination, 9999)

    def test_accelerate_by(self):
        old_speed = self.car.speed
        self.car.accelerate_by(10)
        self.assertEqual(self.car.speed, old_speed+10)

    def test_accelerate_over_speed_limit(self):
        self.assertRaises(OverTheLimitError, self.car.accelerate_by, 340)

    def test_decelerate_by(self):
        self.car.accelerate_by(100)
        old_speed = self.car.speed
        self.car.decelerate_by(10)
        self.assertEqual(self.car.speed, old_speed-10)

    def test_decelerate_under_0(self):
        self.car.decelerate_by(9999)
        self.assertEqual(self.car.speed, 0)

    def test_stop(self):
        self.car.stop()
        self.assertEqual(self.car.speed, 0)

        if self.car.speed == 0:
            self.assertRaises(InvalidOperationError, self.car.stop)

    def test_has_arrived(self):
        self.car.distance_to_destination = 0
        self.assertTrue(self.car.has_arrived())

        self.car.distance_to_destination = 100
        self.assertFalse(self.car.has_arrived())

    def test_drive(self):
        self.car.set_destination('Thessaloniki')
        self.car.drive()
        self.assertEqual(self.car.distance_to_destination, 9989)

        self.car.set_destination('Athens')
        new_distance = self.car.distance_to_destination - math.floor(self.car.speed / 10)
        self.car.drive()
        self.assertEqual(self.car.distance_to_destination, new_distance)


class TestCarBadInput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.car = Car(300)

    def test_accelerate_bad_input(self):
        self.assertRaises(BadInputError, self.car.accelerate_by, -10)
        self.assertRaises(BadInputError, self.car.accelerate_by, 'Hello')

    def test_destination_bad_input(self):
        self.assertRaises(BadInputError, self.car.set_destination, 10)
        self.assertRaises(BadInputError, self.car.set_destination, 10.0)
        self.assertRaises(BadInputError, self.car.set_destination, True)
        self.assertRaises(InvalidDestinationError, self.car.set_destination, 'Giannitsa')

    def test_deceleration_bad_input(self):
        self.assertRaises(BadInputError, self.car.decelerate_by, -10)
        self.assertRaises(BadInputError, self.car.decelerate_by, 10.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
