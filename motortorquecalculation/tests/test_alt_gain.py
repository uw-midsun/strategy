import sys
import os.path
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from alt_gain import Car

@pytest.fixture
def car_default():
    car = Car(720, 0.15, 0.0015)
    return car

def test_no_velocity(car_default):
    assert(round(car_default.force(0, 0, 1), 1) == 10.6)
    assert(round(car_default.energy_use(100, 0, 0, 30), 1) == 1059.5)
    assert(round(car_default.torque_req(0, 0, 30), 1) == 1.4)

def test_force_accel(car_default):
    assert(round(car_default.force(0, 16.6, 30), 1) == 434.3)

def test_energy_accel(car_default):
    assert(round(car_default.energy_use(100, 0, 16.6, 30), 1) == 43431.2)

def test_torque_req_accel(car_default):
    assert(round(car_default.torque_req(0, 16.6, 30), 1) == 56.5)