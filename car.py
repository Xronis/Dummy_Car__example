import math

import numpy as np
import pandas as pd

world_towns = pd.read_csv('./world-cities_csv.csv')

distance_col = np.random.randint(low=1000, high=10000, size=len(world_towns))
world_towns = world_towns.assign(distance=distance_col)
world_towns.at['23018'] = ['Thessaloniki', 'Greece', 'Macedonia', 123456, 9999]


class InvalidDestinationError(ValueError):
    pass


class OverTheLimitError(ValueError):
    pass


class BadInputError(ValueError):
    pass


class InvalidOperationError(RuntimeError):
    pass


class Car:

    def __init__(self, speed_limit, speed=0, distance_to_destination=0, destination=None):
        self.speed = speed
        self.speed_limit = speed_limit
        self.distance_to_destination = distance_to_destination
        self.destination = destination

    def set_destination(self, destination):
        if not isinstance(destination, str):
            raise BadInputError('Not supported type as destination. Try using a string.')

        if destination not in world_towns.name.tolist():
            raise InvalidDestinationError('Selected destination not available: {}'.format(destination))

        self.destination = destination
        self.distance_to_destination = world_towns[world_towns['name'] == destination].values.tolist()[-1][-1]

    def accelerate_by(self, acceleration):

        if not isinstance(acceleration, int):
            raise BadInputError('Not supported type for acceleration. Try using a number.')

        if acceleration < 0:
            raise BadInputError('Accelerating by negative number is impossible.')

        if self.speed + acceleration > self.speed_limit:
            raise OverTheLimitError('Can\'t accelerate by {}. Over speed limitation of car'.format(acceleration))

        self.speed += acceleration

    def decelerate_by(self, deceleration):
        if not isinstance(deceleration, int):
            raise BadInputError('Not supported type for deceleration. Try using a number.')

        if deceleration < 0:
            raise BadInputError('Accelerating by negative number is impossible.')

        if self.speed - deceleration < 0:
            self.speed = 0
            return

        self.speed -= deceleration

    def stop(self):
        if self.speed == 0:
            raise InvalidOperationError('Operation unavailable since car is already stopped.')

        self.speed = 0

    def drive(self):
        distance = self.distance_to_destination - math.floor(self.speed / 10)
        new_distance = 0 if distance < 0 else distance

        print('Distance to destination: {}'.format(new_distance))

        self.distance_to_destination = new_distance

    def has_arrived(self):
        if self.distance_to_destination == 0:
            print('Destination Reached')
            return True

        return self.distance_to_destination == 0


def print_world_towns_names():
    for name in world_towns.name:
        print(name)


if __name__ == '__main__':
    car = Car(160, speed=100)
    car.set_destination('Thessaloniki')

    while not car.has_arrived():
        car.drive()

    print(world_towns)
