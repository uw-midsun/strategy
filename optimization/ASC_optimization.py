"""
do i want to update everything on "get" -> ie. when we run optimization, or before?
if we're running multiple possibilities does this change anything

let's initially approach this as a prediction _only_ thing
"""
import csv
import pandas as pd

import sys
import os.path
sys.path.append(os.path.dirname(__file__), '..')

from dynamics.motor_efficiency.motor_efficiency import MotorEfficiency
from dynamics.car_model import Car

RACE_FILE = os.path.join(os.path.dirname(__file__), '../routemodel/data_retrieval/new_get_weather.csv')

class ASC_Race:

    # Car information
    PASSENGERS = 4
    BATTERY_CAPACITY_kWH = 20

    distance_travelled_segments = []
    # passengers = []
    time_elapsed_mins = 0

    def __init__(self, race_data_csv):
        # TODO: determine format of data passing and interacts
        # TODO: how to change route? update during race?
        self.route_df = pd.read_csv(race_data_csv, delimiter=',')

        # find distance -> hopefully a parameter; append to list
        # if passengers not flagged
        # self.passengers.append(4)

    @property
    def D(self):
        '''
        Person-Mile Distance
        '''
        d = 0
        # for seg, passenger in zip(self.distance_travelled_segments, self.passengers):
            # d += seg * passenger

        for seg in self.distance_travelled_segments:
            d += seg
    
        return d
    
    @property
    def E(self):
        '''
        External Energy Usage
        (n + 1) * Q * M
        '''
        nights = 4
        charging_per_night = 100
        return nights * charging_per_night

    @property
    def C(self):
        '''
        Completion Factor
        '''
        return 1

    @property
    def T(self):
        '''
        Target Speed Derate
        '''
        d = 0
        for seg in self.distance_travelled_segments:
            d += seg
    
        return d / self.time_elapsed_mins / 60

    @property
    def P(self):
        '''
        Practicality Score
        '''
        return 1
    
    def update_variables(self, velocity_profile):
        pass

    def get_score(self, velocity_profile):
        self.update_variables(velocity_profile)
        return self.D / self.E * self.C * self.T * self.P

def energy_needed():
    # between two points, how much energy do we draw?
    # ok so 
    # minus: 
    #   energy needed to travel this distance * -> energy_used, but only between two points? 
    car_model = Car() # can add speed limit?
    energy_needed = car_model.energy_used()

    #   efficiency of motors * (draw more energy than necessary) -> motor eff curves
    low_curve = MotorEfficiency("LO")
    high_curve = MotorEfficiency("HI")
    # TODO what the fuck is this
    # so we have speed, it will guess our torque based on test data
    power_needed = low_curve.power_draw_needed(energy_needed, speed, torque)

    #   efficiency of soc (how much energy is actually taken from batteries) -> soc 
    power_loss = power_needed * 0.5

    # auxloss to consider
    power_loss += 0.5

    # plus: energy gained from solar -> from solar

    power_loss -= 0.5

    return power_loss

    # takeaway from this exercise is that carmodel, lowhigh, and our soc and solar objects can be fairly static? we will need to change the speed limit on the car as we go, which we can do hopefully
    # how do we want this to happen wiht df -> either make calls per row, or just change the methods so they accept dfs

if __name__ == '__main__':
    race = ASC_Race(RACE_FILE)

'''

lat, lon, city name, city Id, time, temperature, efficiency correction,
wind speed, wind direction, precipitation, energy solar, energy corrected
+ mark stops (checkpoints) somehow

routemodel
speed limits, lat, lon, elevations
wind
weather??

solar


soc
??
auxloss

motor torque

dynamics

'''


'''
also, comparison of fmin
+ https://www.mathworks.com/help/optim/ug/fmincon.html
+ https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html


Parameters
fun(x, *args) -> float ==> get_score()  
initial guess ==> even within speed limits?
bounds (for each in x) ==> speed limits

'''