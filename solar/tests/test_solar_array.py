import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

from solar_array import SolarArray
global test
test = SolarArray(182, 30.28, 97.73, 8, 0.5)

def test_totalEnergy():
    temp = round(test.totalEnergy(),2)
    assert(temp == 2822.69)

def test_data():
    temp = test.data()
    total = 0
    for i in temp[1:]:
        total += float(i["Angle"])
    total = round(total, 2)
    assert(total == 2590.05)
    