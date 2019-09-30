import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))
from car_model import Car
global car
# Tests to check that the variables are properly set
car = Car()


def test_no_velocity():
    assert(car.force_req(0) == 10.594800000000001)


def test_10_ms():
    assert(car.force_req(10) == 19.7823)


def test_energy_used():
    assert(car.energy_used([5, 7, 9, 13, 9.5, 7, 5], [-1, 1, 3, 3, 1, 1, 1.5])
           == 28267.47205752044)
