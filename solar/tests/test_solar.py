import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

from solar import SolarDay      

global solar 
solar = SolarDay(1,2,3,4,5,6) 

def test_declination_angle():
    assert(solar.declination_angle() == -23.030845457604613)

def test_time_correction():
    assert(solar.time_correction() == -232.02665347346084)

def test_sunrise():
    assert(solar.sunrise() == 9.923817382442401)

def test_sunset():
    assert(solar.sunset() == 21.810404400006295)

def test_solar_insolation():
    assert(solar.solar_insolation(5.1) == 0.604050501550471)

def test_AM():
    assert(solar.AM(5.1) == 2.9941439864507515)

def test_time_to_HRA():
    assert(solar.time_to_HRA(5.7) == -2.6617434070085983)

def test_energy_recieved(): 
    """
    This sums up all the returned values in the energy list
    and compares that with the sum value I am expecting. Likely 
    a better way to do this since it doesnt technically compare
    the output of energy_received, it compares the sum.
    """
    temp = solar.energy_received()
    temp2=0
    for i in temp:
        for j in i:
            temp2+=j

    assert(temp2==16554.45895476286)