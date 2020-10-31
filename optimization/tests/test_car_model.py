import sys
import os.path
import pytest
import mock
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from car_model import Car

@pytest.fixture
def car_min_0_max_1000():
    car = Car()
    car.speed_min_ms = 0
    car.speed_max_ms = 1000
    return car

@pytest.fixture
def car_min_15_max_45():
    car = Car()
    car.speed_min_ms = 15
    car.speed_max_ms = 45
    return car

def test_no_velocity(car_min_0_max_1000, car_min_15_max_45):
    assert(car_min_0_max_1000.force_req(0) == 10.594800000000001)
    assert(round(car_min_15_max_45.force_req(0), 3) == 31.267)

def test_10_ms(car_min_0_max_1000, car_min_15_max_45):
    assert(car_min_0_max_1000.force_req(10) == 19.7823)
    assert(round(car_min_15_max_45.force_req(10), 3) == 31.267)

def test_force_req_more_parameters(car_min_0_max_1000, car_min_15_max_45):
    # doesn't touch limits
    assert(round(car_min_0_max_1000.force_req(20, vwind=10, v_old=5, theta=0, timestep=30), 3) == 453.282)
    # doesn't touch limits
    assert(round(car_min_15_max_45.force_req(20, vwind=10, v_old=16, theta=0, timestep=30), 3) == 189.282)
    # v_old gets limited, 55 -> 45
    assert(round(car_min_15_max_45.force_req(20, vwind=10, v_old=55, theta=0, timestep=30), 3) == -506.718)
    # v_old gets limited, 55 -> 45 and v gets limited 80 -> 45
    assert(round(car_min_15_max_45.force_req(80, vwind=10, v_old=55, theta=0, timestep=30), 3) == 288.517)

def test_force_req_errors(car_min_0_max_1000):
    # divide by timestep
    with pytest.raises(ZeroDivisionError):
        car_min_0_max_1000.force_req(80, vwind=10, v_old=55, theta=0, timestep=0)

@mock.patch('car_model.Car.force_req', return_value=0)
def test_max_velocity(mock_force_req, car_min_0_max_1000, car_min_15_max_45):
    # mock
    assert(car_min_0_max_1000.force_req(0) == 0)
    # limits not used
    assert(car_min_0_max_1000.max_velocity(0) == 3000)
    # limits used 500 -> 45
    assert(car_min_15_max_45.max_velocity(500) == 3045)
    # more parameters, limits 520 -> 45
    assert(car_min_15_max_45.max_velocity(520, vwind=20, theta=0, timestep=20) == 2045)

def test_energy_used(car_min_0_max_1000, car_min_15_max_45):
    assert(car_min_0_max_1000.energy_used([5, 7, 9, 13, 9.5, 7, 5],
                           [(-1, 100), (1, 100), (3, 100), (3, 100),
                           (1, 100), (1, 100), (1.5, 100)])
           == 28267.47205752044)
    
    # limits all velocities -> 15 m/s
    # same as making call with [15, 15, 15, 15, 15, 15, 15] as velocity profiles
    assert(round(car_min_15_max_45.energy_used([5, 7, 9, 13, 9.5, 7, 5],
                           [(-1, 100), (1, 100), (3, 100), (3, 100),
                           (1, 100), (1, 100), (1.5, 100)]), 3)
           == 36414.488)

def test_energy_used_errors(car_min_0_max_1000):
    with pytest.raises(IndexError):
        # if velocity points array and the elevation points array are not equal, then the test raises a IndexError.
        # velocity profiles too long (8 velocity points, 7 elevation points)
        car_min_0_max_1000.energy_used([5, 7, 9, 13, 9.5, 7, 5, 20], [(-1, 100), (1, 100), (3, 100), (3, 100), (1, 100), (1, 100), (1.5, 100)])
    
    with pytest.raises(IndexError):
        # If the above test works, then this test will be NOT called 
        # velocity profiles too short (6 velocity points, 7 elevation points)
        car_min_0_max_1000.energy_used([5, 7, 9, 13, 9.5, 7], [(-1, 100), (1, 100), (3, 100), (3, 100), (1, 100), (1, 100), (1.5, 100)])   
    
    with pytest.raises(IndexError):
        # divide by dist = e_profile[point][1]
        car_min_0_max_1000.energy_used([5, 7, 9, 13, 9.5, 7], [(-1, 0), (1, 100), (3, 100), (3, 100), (1, 100), (1, 100), (1.5, 100)])

    with pytest.raises(ZeroDivisionError):
        # divide by v_avg = (v_new + v_old) / 2
        # two consecutive points add to zero
        car_min_0_max_1000.energy_used([0, 0, 9, 13, 9.5, 7], [(-1, 100), (1, 100), (3, 100), (3, 100), (1, 100), (1, 100)])