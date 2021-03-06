import sys
import os.path
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from BatteryPower import BatteryPower

@pytest.fixture
def battery():
    battery = BatteryPower()
    return battery

#testing using sample data under the title BATTERY_AGGREGATE_VC from can_messages.csv
def test_battery_aggregate_vc(battery):
    assert(battery.calc_power(2339805638, 171683203) == 401705326329298514)
    assert(battery.calc_power(2662553934, 3548668148) == 9448520337917894232)
    assert(battery.calc_power(2436208041, 681804358) == 1661017259348442678)
    assert(battery.calc_power(629290808, 6734528) == 4237976566618624)
    assert(battery.calc_power(2003252338, 2003252338) == 4013019929702466244)
    assert(battery.calc_power(3013540249, 2307234718) == 6952944686583164782)
    assert(battery.calc_power(270409647, 133771994) == 36173237676026118)
    assert(battery.calc_power(2565162974, 2361918908) == 6058706930392112392)
    assert(battery.calc_power(171683203, 2339805638) == 401705326329298514)
    assert(battery.calc_power(875251415, 3832059876) == 3354015828833724540)