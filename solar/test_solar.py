import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

from solar import SolarDay
from solar import integrate
global SolarDay

#day - base case
solarDayBase = SolarDay(350, 0.23, 90.23, 1, 0.5, -90)
#day - change moduleangle1
solarDayMod1 = SolarDay(350, 0.23, 90.23, 1, 0.5, -45)
#day - change moduleangle2
solarDayMod2 = SolarDay(350, 0.23, 90.23, 1, 0.5, 0)
#day - change moduleangle3
solarDayMod3 = SolarDay(350, 0.23, 90.23, 1, 0.5, 45)
#day - change moduleangle4
solarDayMod4 = SolarDay(350, 0.23, 90.23, 1, 0.5, 90)
#day - change day1
solarDayDay1 = SolarDay(81, 0.23, 90.23, 1, 0.5, -45)
#day - change day2
solarDayDay2 = SolarDay(126, 0.23, 90.23, 1, 0.5, -45)
#day - change location1 (equator - quito)
solarDayLoc1 = SolarDay(350, -0.18, -78.47, 5, 0.5, -45)
#day - change location2 (random, paris)
solarDayLoc2 = SolarDay(350, 48.86, 2.29, 1, 0.5, -45)
#day - change location3 (south pole)
solarDayLoc3 = SolarDay(350, 89.01, 45.41, 0, 0.5, -45)
#day - change cloud1
solarDayCloud1 = SolarDay(350, 89.01, 45.41, 0, 0, -45)
#day - change cloud2
solarDayCloud2 = SolarDay(350, 89.01, 45.41, 0, 0.25, -45)
#day - change cloud3
solarDayCloud3 = SolarDay(350, 89.01, 45.41, 0, 0.5, -45)
#day - change cloud4
solarDayCloud4 = SolarDay(350, 89.01, 45.41, 0, 0.75, -45)
#day - change cloud5
solarDayCloud5 = SolarDay(350, 89.01, 45.41, 0, 1, -45)


# solstice, location - south pole, cloud - 0
#solarDayDay1 = SolarDay(350, 0.23, 90.23, 1, 1, 20) 
#day  - equinox, location - equator (Quito), cloud - 0.5
#solarDayDay2 = SolarDay(81.25, -0.18, -78.47, 5, 0.5, 40) 
#day - random, location - random, cloud - 0
#solarDayDay3 = SolarDay(126, 48.86, 2.29, 1, 0, 60)


def test_energy_received():
    solarDayBaseR = 5 * 0.17 * integrate(solarDayBase.energy_received()[1], solarDayBase.energy_received()[0])
    assert(solarDayBaseR == 0)

    solarDayMod1R = 5 * 0.17 * integrate(solarDayMod1.energy_received()[1], solarDayMod1.energy_received()[0])
    assert(solarDayMod1R == 0)

    solarDayMod2R = 5 * 0.17 * integrate(solarDayMod2.energy_received()[1], solarDayMod2.energy_received()[0])
    assert(solarDayMod2R == 0)

    solarDayMod3R = 5 * 0.17 * integrate(solarDayMod3.energy_received()[1], solarDayMod3.energy_received()[0])
    assert(solarDayMod3R == 0)

    solarDayMod4R = 5 * 0.17 * integrate(solarDayMod4.energy_received()[1], solarDayMod4.energy_received()[0])
    assert(solarDayMod4R == 0)

    solarDayDay1R = 5 * 0.17 * integrate(solarDayDay1.energy_received()[1], solarDayDay1.energy_received()[0])
    assert(solarDayDay1R == 0)

    solarDayDay2R = 5 * 0.17 * integrate(solarDayDay2.energy_received()[1], solarDayDay2.energy_received()[0])
    assert(solarDayDay2R == 0)

    solarDayLoc1R = 5 * 0.17 * integrate(solarDayLoc1.energy_received()[1], solarDayLoc1.energy_received()[0])
    assert(solarDayLoc1R == 0)

    solarDayLoc2R = 5 * 0.17 * integrate(solarDayLoc2.energy_received()[1], solarDayLoc2.energy_received()[0])
    assert(solarDayLoc2R == 0)

    solarDayLoc3R = 5 * 0.17 * integrate(solarDayLoc3.energy_received()[1], solarDayLoc3.energy_received()[0])
    assert(solarDayLoc3R == 0)

    solarDayCloud1R = 5 * 0.17 * integrate(solarDayCloud1.energy_received()[1], solarDayCloud1.energy_received()[0])
    assert(solarDayCloud1R == 0)

    solarDayCloud2R = 5 * 0.17 * integrate(solarDayCloud2.energy_received()[1], solarDayCloud2.energy_received()[0])
    assert(solarDayCloud2R == 0)

    solarDayCloud3R = 5 * 0.17 * integrate(solarDayCloud3.energy_received()[1], solarDayCloud3.energy_received()[0])
    assert(solarDayCloud3R == 0)

    solarDayCloud4R = 5 * 0.17 * integrate(solarDayCloud4.energy_received()[1], solarDayCloud4.energy_received()[0])
    assert(solarDayCloud4R == 0)

    solarDayCloud5R = 5 * 0.17 * integrate(solarDayCloud5.energy_received()[1], solarDayCloud5.energy_received()[0])
    assert(solarDayCloud5R == 0)


