"""
formula given:
S = (D / E) * C * T * P
optimize for S

do i want to update everything on "get" -> ie. when we run optimization, or before?
if we're running multiple possibilities does this change anything

let's initially approach this as a prediction _only_ thing
"""
import csv

class ASC_Race:

    # Car information
    PASSENGERS = 4
    BATTERY_CAPACITY_kWH = 20

    distance_travelled_segments = []
    passengers = []
    time_elapsed_mins = 0

    def __init__(self, race_data_csv):
        # TODO: determine format of data passing and interacts
        # TODO: how to change route? update during race?
        with open(race_data_csv, 'r') as f:
            route = csv.reader(f)

            start = next(route)

            for row in route:
                # find distance -> hopefully a parameter; append to list
                # if passengers not flagged
                self.passengers.append(4)

    @property
    def D(self):
        '''
        Person-Mile Distance
        '''
        d = 0
        for seg, passenger in zip(self.distance_travelled_segments, self.passengers):
            d += seg * passenger
    
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

    def get_S(self, velocity_profile):
        self.update_variables(velocity_profile)
        return self.D / self.E * self.C * self.T * self.P

'''
initial guess = all even, get S
next guess = all even, except when limited by speed limit, get S

push in one direction (manage each segment?)

'''


'''
what is the trial run going to send in - where are we sending velocity into it
calculate best velocities -> then find minutes?

lat, lon, city name, city Id, time, temperature, efficiency correction,
wind speed, wind direction, precipitation, energy solar, energy corrected

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


some guess of S with a general profile of velocities
change velocities -> see how it affects S
'''
