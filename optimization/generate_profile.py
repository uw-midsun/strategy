# This file will deal with implementing the velocity profile creation using a genetic generation algorithm
from random import randrange
from math import ceil, floor, sqrt
from statistics import mean
from energyconsumption import energyConsumption
import matplotlib.pyplot as plt
import numpy
global m, Crr, rho, CdA, vwind
m = 660
Crr = 0.07
rho = 1.125
CdA = 0.59
vwind = 0
def get_torque(velocity = 'arbitrary', air_gap = 'arbitrary'):
    # TODO: Add Connor's torque calculations
    accel = 0.95
    return accel

def max_accel(velocity, gradient):
    accel = get_torque()
    state = energyConsumption(m, gradient, Crr, rho, CdA, velocity, velocity, vwind, 30)
    decel = -1 * (state.drag + state.fric) / state.m
    if state.grav > 0:
        decel = decel - (state.grav / state.m)
    else:
        accel = accel - (state.grav / state.m)
    accel = accel + decel
    return [floor(decel * 1000), ceil(accel * 1000)]
def v_over_d_to_a(v1, a, d):
    v2squared = (v1 ** 2 + 2 * a * d)
    if v2squared > 0:
        v2 = sqrt(v1 ** 2 + 2 * a * d)
    else:
        v2 = 0.1
    return v2
def generate_profile(time, distance, max_velocity = 20, precision = 30):
    """
    :param time (int) Maximum allowable time to cover a distance in seconds
    :param distance (int) Distance to be covered in meters
    :param max_velocity (int) Maximum allowable velocity in meters per second
    :param init_pops (int) Number of initial populations generated
    :param variance (float) How heavily we wish to vary our initial guesses
    :param precision (int) meters between measured points
    """
    pops = []
    avg_velocity = distance / time
    initial_profile = []
    for point in range(distance // precision):
        initial_profile.append(avg_velocity)
    # Here we generate the naive solution of traveling at the average velocity required
    return initial_profile
  

def calculate_fit(velocity_profile, elevation_profile, max_time = 450, max_a = 20, precision = 30):
    """
    :param velocity_profile (list) a precision by precision list of velocities
    :param elevation_profile (list) a precision by precision list of gradients in radians
    :param max_time (int) the maximum allowable time to travel a distance in seconds
    :param max_a (int) the maximum allowable acceleration in the velocity profile
    :param precision (int) distance in meters between points
    """
    energy = []
    for point in range(1, len(velocity_profile)):
        #TODO: Change the energyConsumption method to take in a list instaed of individual velocity/elevations
        force_point = energyConsumption(m, elevation_profile[point - 1], Crr, rho, CdA, velocity_profile[point],velocity_profile[point - 1], vwind, 30) 
        energy_point = force_point.energyUsed()
        energy.append(energy_point)
    fit = sum(energy)
    times = [force_point.d / v for v in velocity_profile[1:]]
    has_negative = any(v < 0 for v in velocity_profile)
    if sum(times) > max_time or has_negative:
        fit = -1
    return fit

def generation_forward(profile, elev_profile, cut_percentage = 0.8, max_velocity = 30, decel = -0.5, accel = 0.6):
    """
    :param pops (list) a list of velocity profiles
    :param fitnesses (list) a list of pops evaluated by some valuation function
    :param cut_percentage (float, 0 to 1) proportion of population that "dies"
    :param mutation (float, 0 to 1) likeliness of a newly generated pop being "mutated"
    :param variance (float) gives the variance scale of mutation (as a proportion of max_velocity) * 0.1
    :param max_velocity (float) maximum allowable velocity
    """
    new_profile = []
    new_profile.append(21)
    for point in range(len(profile) - 1):
        decel = ceil(max_accel(new_profile[point], elev_profile[point])[0])
        accel = ceil(max_accel(new_profile[point], elev_profile[point])[1])
        if accel < 0:
            a = randrange(decel, accel) * 0.001
        else:
            a = randrange(decel, accel * 50) * (0.001 / 20)
            if a < 0:
                a = a * 50
        v_next = v_over_d_to_a(new_profile[point], a, 30)        
        if v_next < 1:
            v_next = 1
        if v_next > max_velocity:
            v_next = max_velocity
        new_profile.append(v_next)
    print(new_profile)
    return new_profile

if __name__ == '__main__':
    # Load in the COTAelevation map
    with open('COTAelevation.txt', 'r') as file:
        line = file.readline()
        count = 1
        data = []
        while line and count < 3:
            count += 1
            line = file.readline()
        while line:
            line = file.readline()
            data.append(line)
        clean_data = []
        for row in data:
            row = row.replace('\n', '').split(',')
            if row != '':
                clean_data.append(row)
    # Create the elevation profile
    elev_profile = []
    for i in range(len(clean_data) - 1):
        pitch = numpy.arctan(float(clean_data[i][1]) / 10)
        elev_profile.append(pitch)
    # Load in the distance and necessary time for a lap
    distance = 5490
    time = 420
    iterations = 5000 # Number of iterations to use
    # Generate a population setup
    profile = generate_profile(time, distance)
    values = []
    # Calculate the fitness of each population:
    values.append(calculate_fit(profile, elev_profile))
    min_value = 1000000
    for i in range(iterations):
        new_profile = generation_forward(profile, elev_profile)
        value = calculate_fit(new_profile, elev_profile)
        print(value, min_value)
        if min_value > value and value > 0:
            profile = new_profile
            min_value = value
            values.append(value)
            print(value)
    # Show a plot of those means to see the differences
    plt.plot(values)
    plt.show()
    # Show the optimal path
    print(profile)
