import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

from solar import SolarDay      

global solar 
solar = SolarDay(1,2,3,4,5,6) 

def test_declination_angle():
    temp = round(solar.declination_angle(), 4)
    assert(temp == -23.0308)

def test_time_correction():
    temp = round(solar.time_correction(), 3)
    assert(temp == -232.027)

def test_sunrise():
    temp = round(solar.sunrise(), 5)
    assert(temp == 9.92382)

def test_sunset():
    temp = round(solar.sunset(), 4)
    assert(temp == 21.8104)

def test_solar_insolation():
    temp = round(solar.solar_insolation(5.1), 6)
    assert(temp == 0.604051)

def test_AM():
    temp = round(solar.AM(5.1), 5)
    assert(temp == 2.99414)

def test_time_to_HRA():
    temp = round(solar.time_to_HRA(5.7), 5)
    assert(temp == -2.66174)

def test_energy_recieved(): 
    """
    This sums up all the returned values in the energy list
    and compares that with the sum value I am expecting. Likely 
    a better way to do this since it doesnt technically compare
    the output of energy_received, it compares the sum.
    """
    temp = solar.energy_received()
    temp2 = 0
    for i in temp:
        for j in i:
            temp2 += j

    temp2 = round(temp2, 1)

    assert(temp2 == 16554.5)
    