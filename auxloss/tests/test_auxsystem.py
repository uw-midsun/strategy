import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))
from auxsystem import AuxSystem


def test_no_time():
    TestSystem = AuxSystem(10, 6)
    assert(TestSystem.energy_consumed(0, 10, 6) == 0)


def test_no_current():
    TestSystem = AuxSystem(0, 2)
    assert(TestSystem.energy_consumed(1, 0, 2) == 0)


def test_no_voltage():
    TestSystem = AuxSystem(2, 0)
    assert(TestSystem.energy_consumed(1, 2, 0) == 0)


def test_negative_time():
    TestSystem = AuxSystem(10, 6)
    assert(TestSystem.energy_consumed(-1, 10, 6) == 0)


def test_negative_voltage():
    # will assume new voltage is 0
    TestSystem = AuxSystem(10, 6)
    assert(TestSystem.energy_consumed(1, 10, -1) == 60)


def test_negative_current():
    # will assume new current is 0
    TestSystem = AuxSystem(10, 0)
    assert(TestSystem.energy_consumed(2, -1, 2) == 20)


def test_positive_attributes():
    TestSystem = AuxSystem(1, 1)
    assert(TestSystem.energy_consumed(1, 1, 1) == 1)


def test_attributes_initialized_negative():
    TestSystem = AuxSystem(-1, -1)
    assert(TestSystem.voltage == 0)
    assert(TestSystem.voltage_old == 0)
    assert(TestSystem.current == 0)
    assert(TestSystem.current_old == 0)
