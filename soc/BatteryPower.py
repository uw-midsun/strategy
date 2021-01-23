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