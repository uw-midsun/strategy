import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

from cell import SolarCell

def test_efficiency_decrease_under_25():
    cell = SolarCell(0,0)
    assert(cell.total_efficiency_decrease() == .243)

def test_efficiency_decrease_over_25():
    cell = SolarCell(0,100)
    assert(round(cell.total_efficiency_decrease(),6) == 0.0255) 
