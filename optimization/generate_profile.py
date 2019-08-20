# This file will deal with implementing the velocity profile creation
from random import uniform
from math import ceil, floor, sqrt
from car_model import Car
import matplotlib.pyplot as plt
import numpy
global car

car = Car()
def v_over_d_to_a(v1, a, d):
    v2squared = (v1 ** 2 + 2 * a * d)
    if v2squared > 0:
        v2 = sqrt(v1 ** 2 + 2 * a * d)
    else:
        v2 = 0.1
    return v2


def generate_initial_profile(time, distance, e_profile):
    """
    :param time: Maximum allowable time to cover a distance in seconds
    :param distance: Distance to be covered in meters
    :param e_profile: List of pitches the car must travel
    """
    avg_velocity = distance / time
    dist_step = distance / len(e_profile)
    initial_profile = [avg_velocity]
    for point in range(len(e_profile) - 1):  # We don't care about the endpoint
        pitch = e_profile[point]
        old_v = initial_profile[point - 1]
        timestep = dist_step / old_v
        max_v = car.max_velocity(old_v, theta=pitch, timestep=timestep)
        if max_v >= avg_velocity:
            initial_profile.append(avg_velocity)
        elif max_v >= 5:
            initial_profile.append(max_v)
        else:
            initial_profile.append(5)
    # Here we generate the naive solution
    # traveling at the average velocity required
    return initial_profile


def calculate_fit(v_profile, e_profile, max_time=450, dist_step=30):
    """
    :param v_profile: a step by step list of velocities
    :param e_profile: a step by step list of gradients in rad
    :param max_time: the max allowable time to travel a distance in s
    :param dist_step: the distance between measured points
    """
    energy = car.energy_used(v_profile, e_profile, distance=dist_step)
    has_negative = any(v < 0 for v in v_profile)
    # We ignore the first point since v is 0 at the start
    time = [dist_step / v for v in v_profile[1:]]
    if sum(time) > max_time or has_negative:
        fit = -1
    else: 
        fit = energy
    return [fit, sum(time)]


def generate_new_profile(v_profile, e_profile, dist_step=30, min_v = 7):
    """
    :param v_profile: a step by step list of velocities in m/s
    :param e_profile: a step by step list of gradients in rad
    :param dist_step: distance between points
    :param min_v: the slowest we are allowed to go 
    """
    new_profile = []
    new_profile.append(v_profile[0]) # start at the same speed
    for point in range(len(v_profile) - 1):
        timestep = dist_step / v_profile[point]
        max_v = car.max_velocity(
                v_profile[point], theta=e_profile[point], timestep=timestep)
        if max_v > min_v:
            new_v = uniform(min_v, max_v)
        else:
            new_v = min_v
        new_profile.append(new_v)
    return new_profile

def load_course_map(course_name="COTA"):
    """
    :param course_name: name of the course we are loading in
    :return elev_profile: map of the elevations on a course
    """
    if course_name == "COTA":
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
    if course_name == "ASC":
        
    return elev_profile
 
if __name__ == '__main__':
    elev_profile = load_course_map()
    # Load in the distance and necessary time for a lap
    distance = 5490
    time = 420
    iterations = 50000  # Number of iterations to use
    init_profile = generate_initial_profile(time, distance, elev_profile)
    v_profile = init_profile
    values = []
    # Calculate the fitness of each population:
    values.append(calculate_fit(init_profile, elev_profile))
    min_value = 1000000
    min_time = 1000000
    for i in range(iterations):
        new_profile = generate_new_profile(v_profile, elev_profile)
        value = calculate_fit(new_profile, elev_profile, max_time=1000)
        if min_value > value[0] and value[0] > 0:
            v_profile = new_profile
            min_value = value[0]
            min_time = value[1]
            values.append(value)
        elif min_time > value[1] and value[0] < 0:
            v_profile = new_profile
            min_value = value[0]
            min_time = value[1]
            values.append(value)
            
    # Show a plot of those means to see the differences
    plt.plot(values)
    plt.show()
    # Show the optimal path
    print(v_profile)
