import sys
import os
sys.path.append(os.path.join(sys.path[0], '../../'))
import pytest
import mock
from displays.SOC_velocity_graph import calculate_SOC_values

def test_calculate_SOC_values_zero_values():
    velocities = [0, 0, 0]
    elevations = [(0, 0), (0, 0), (0, 0)]
    distances = [0, 0, 0]
    initial_soc = 0

    with pytest.raises(ZeroDivisionError):
        calculate_SOC_values(velocities, elevations, distances, initial_soc)

def test_calculate_SOC_values_nonzero_values():
    velocities = [5, 7, 9, 13, 9.5, 7.5, 5]
    elevations = [(-1, 100), (1, 100), (3, 100), (3, 100), (1, 100), (1, 100), (1.5, 100)]
    distances = [10000, 10000, 20000, 30000, 30000, 30000, 20000]
    initial_soc = 1

    expected_result = [1, 0.9999995851481777, 0.9999991160493323, 0.9999985299598554, 0.9999992236028236, 0.9999994058571505, 0.9999995157405268, 0.9999994937072884]

    assert(expected_result == calculate_SOC_values(velocities, elevations, distances, initial_soc, min_speed=0, max_speed=1000))

def test_calculate_SOC_values_initial_soc_non_1():
    velocities = [5, 7, 9, 13, 9.5, 7.5, 5]
    elevations = [(-1, 100), (1, 100), (3, 100), (3, 100), (1, 100), (1, 100), (1.5, 100)]
    distances = [10000, 10000, 20000, 30000, 30000, 30000, 20000]
    initial_soc = 0.9

    expected_result = [0.9, 0.8999995851481777, 0.8999991160493324, 0.8999985299598554, 0.8999992236028236, 0.8999994058571505, 0.8999995157405268, 0.8999994937072884]

    assert(expected_result == calculate_SOC_values(velocities, elevations, distances, initial_soc, min_speed=0, max_speed=1000))

def test_calculate_SOC_values_zero_length_inputs():
    with pytest.raises(IndexError):
        calculate_SOC_values([], [], [], 1)

def test_calculate_SOC_values_single_element_inputs():
    with mock.patch("soc.soc_deprecated.SoCEstimation.CoulombCounter.get_soc", return_value=0.9):
        expected_result = [1, 0.9]
        assert(expected_result == (calculate_SOC_values([1], [(1, 1)], [1], 1)))

def test_calculate_SOC_values_inconsistent_length_inputs():
    with pytest.raises(IndexError):
        calculate_SOC_values([1, 2, 3], [(1, 1)], [1], 1)
        calculate_SOC_values([1, 2], [(1, 2), (2, 2), (4, 5)], [1, 2], 1)