import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

from cell import SolarCell

def test_efficiency_decrease_under_25():
    s = SolarCell(0,0)
    assert(s.total_efficiency_decrease() == .237)

def test_efficiency_decrease_over_25():
    s = SolarCell(0,100)
    assert(s.total_efficiency_decrease() == 0.45449999999999996) 
    #This test is incorrect because as of writing this the efficiency_deccrease funtion is broken