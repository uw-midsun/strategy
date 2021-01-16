import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import csv
import pytest
import mock

from aux_power_consumption import AuxPowerConsumption

budget_file = os.path.join(os.path.dirname(__file__), '..', 'MSXIV Power Budget.csv')

global auxpc
auxpc = AuxPowerConsumption(budget_file)

def test_expected_components_stored_as_keys():
    with open(budget_file, "r") as file:
        csv_file = csv.reader(file)

        column_names = []
        for row in csv_file:
            if row[0] == "Front Power Distribution Board" or row[0] == "Rear Power Distribution Board" or row[0] == "Component" or not row[0]:
                continue

            if row[0] == "AUX Current Draw and AUX Current Protection":
                break

            column_names.append(row[0])

    for component in column_names:
        assert(component in auxpc.power_consumptions)
    
    for key in auxpc.power_consumptions:
        assert(key in column_names)

def test_expected_headers_stored():
    for headers in auxpc.power_consumptions.values():
        assert("Max Power (W)" in headers and "Typical Power (W)" in headers)

def test_calculate_instantaneous_power_string_names_only():
    assert(auxpc.calculate_instantaneous_power({"components": ['Center Console']}) == 4.4)
    assert(auxpc.calculate_instantaneous_power({"components": ["Horn", "Motor Interface", "Solar Master"]}) == 0 + 2.4 + 4.0)

def test_calculate_instantaneous_power_tuples_only():
    assert(auxpc.calculate_instantaneous_power({"components": [("Horn", 10)]}) == round(62.1 * 0.1, 3))
    assert(auxpc.calculate_instantaneous_power({"components": [("Horn", 100), ("Fan", 50), ("Telemetry", 0)]}) == 62.1 + 3 * 0.5)

def test_calculate_instantaneous_power_strings_and_tuples():
    assert(auxpc.calculate_instantaneous_power({"components": [("Horn", 10), "Center Console"]}) == 6.21 + 4.4)
    assert(auxpc.calculate_instantaneous_power({"components": [("Horn", 100), ("Fan", 50), "Telemetry"]}) == 62.1 + 3 * 0.5 + 4.5)

def test_calculate_instantaneous_power_unexpected_input_format():
    with pytest.raises(TypeError):
        assert(auxpc.calculate_instantaneous_power("test"))
        assert(auxpc.calculate_instantaneous_power({"test2": ["hello"]}))

def test_calculate_instantaneous_power_ignores_unknown_components():
    assert(auxpc.calculate_instantaneous_power({"components": [("Horn", 10), "Center Console", "Some random unknown"]}) == 6.21 + 4.4)
    assert(auxpc.calculate_instantaneous_power({"components": [("Horn", 100), ("Fan", 50), "Telemetry", ("Unknowns", 200)]}) == 62.1 + 3 * 0.5 + 4.5)
    assert(auxpc.calculate_instantaneous_power({"components": [("Unknowns", 200), "Winnie the Pooh", ("Caillou", 2)]}) == 0)

def test_calculate_energy_usage_zero_power():
    with mock.patch('aux_power_consumption.AuxPowerConsumption.calculate_instantaneous_power', return_value=0):
        assert(auxpc.calculate_energy_usage({"components":[]}, 10) == 0)

def test_calculate_energy_usage_zero_time():
    with mock.patch('aux_power_consumption.AuxPowerConsumption.calculate_instantaneous_power', return_value=1.0):
        assert(auxpc.calculate_energy_usage("test", 0) == 0)

def test_calculate_energy_usage():
    with mock.patch('aux_power_consumption.AuxPowerConsumption.calculate_instantaneous_power', return_value=1.0):
        assert(auxpc.calculate_energy_usage("test", 100) == 100)
    with mock.patch('aux_power_consumption.AuxPowerConsumption.calculate_instantaneous_power', return_value=14.5):
        assert(round(auxpc.calculate_energy_usage("test", 87), 3) == round(87 * 14.5, 3))
