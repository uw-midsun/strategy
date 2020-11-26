import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from PackEfficiency import PackEfficiency
import mock
import pytest
import math
import cmath

global packEfficiency
packEfficiency = PackEfficiency()

@mock.patch('PackEfficiency.get_pack_ocv', return_value=140.0)
def test_draw_power_no_power_outside_pack(mock_get_pack_ocv):
    with pytest.raises(ZeroDivisionError):
        assert(packEfficiency.draw_power(0) == 0)

def test_draw_power_1000W_outside_pack():
    with mock.patch('PackEfficiency.get_pack_ocv', return_value=140.0):
        assert(round(packEfficiency.draw_power(1000).real, 3) == 1002.822)
        assert(packEfficiency.draw_power(1000).imag == 0)
    with mock.patch('PackEfficiency.get_pack_ocv', return_value=105.0):
        assert(round(packEfficiency.draw_power(1000).real, 3) == 1005.039)
        assert(packEfficiency.draw_power(1000).imag == 0)

def test_draw_power_imaginary_root():
    with mock.patch('PackEfficiency.get_pack_ocv', return_value=140.0):
        # power loss expected to be (14000/11 - 1000sqrt(2)/11 i)^2 * 0.055
        # 90000 + 970000/11 - 140000sqrt(2)/11 i
        assert(round(packEfficiency.draw_power(90000).real, 3) == 178181.818)
        assert(round(packEfficiency.draw_power(90000).imag, 3) == -17999.082)
    with mock.patch('PackEfficiency.get_pack_ocv', return_value=105.0):
        # power loss expected to be (10500/11 - 100sqrt(195)/11 i)^2 * 0.055
        # 51000 + 541500/11 - 10500sqrt(195)/11 i
        assert(round(packEfficiency.draw_power(51000).real, 3) == 100227.273)
        assert(round(packEfficiency.draw_power(51000).imag, 3) == -13329.502)
