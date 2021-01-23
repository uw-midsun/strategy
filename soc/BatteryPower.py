import pandas as pd
import sys
import os.path

class BatteryPower:
    def __init__(self): 
        self.resistance = 0.055

    #based on BATTERY_AGGREGATE_VC data which has voltage + current out of battery pack
    #unsure how to include the BATTERY_VT, which includes voltage + temperature out of one module?
    def calc_power(self, current, voltage):
        power = voltage * current
        return power

class TestBatteryPower:   
    #testing using sample data from can_messages.csv
    def test(self):
        battery_test = BatteryPower()
        #ask about units??
        print(battery_test.calc_power(2339805638, 171683203))
        print(battery_test.calc_power(2662553934, 3548668148))
