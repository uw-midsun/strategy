# This file will deal with implementing the velocity profile creation
from random import uniform
from math import ceil, floor, sqrt
from car_model import Car
import matplotlib.pyplot as plt
import numpy
import argparse

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
    # We ignore the first point since v is 0 at the start
    time = [dist_step / v for v in v_profile[1:]]
    fit = energy
    return [fit, sum(time)]


def generate_new_profile(v_profile, e_profile, dist_step=30, min_v=5):
    """
    :param v_profile: a step by step list of velocities in m/s
    :param e_profile: a step by step list of gradients in rad
    :param dist_step: distance between points
    :param min_v: the slowest we are allowed to go
    """
    new_profile = []
    new_profile.append(v_profile[0])  # start at the same speed
    for point in range(len(v_profile) - 1):
        timestep = dist_step / v_profile[point]
        max_v = car.max_velocity(
            v_profile[point], theta=e_profile[point], timestep=timestep)
        if max_v > min_v:
            new_v = uniform(min_v, max_v)  # Generate a random number between
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
        pass

    return elev_profile


parser = argparse.ArgumentParser(description="Add parameters to model")
parser.add_argument("-d", "--distance", type=int, required=True, help="Distance to travel (m)")
parser.add_argument("-t", "--time", type=int, required=True, help="Maximum allowable time (s)")
parser.add_argument("-i", "--iterations", type=int, required=True, help="Number of iterations to run")
parser.add_argument("-v", "--min_velocity", type=int, required=True, help="Minimum allowable velocity (m/s)")
args = parser.parse_args()

if __name__ == '__main__':
    elev_profile = load_course_map()
    # Load in the distance and necessary time for a lap
    distance = args.distance
    time = args.time  # max allowable time in s
    iterations = args.iterations  # Number of iterations to use
    min_velocity = args.min_velocity

    init_profile = generate_initial_profile(time, distance, elev_profile)
    v_profile = init_profile
    last_real_solution = v_profile
    values = []
    # Calculate the fitness of each population:
    values.append(calculate_fit(init_profile, elev_profile))
    min_value = 1000000
    min_time = 1000000

    for i in range(iterations):
        new_profile = generate_new_profile(v_profile, elev_profile, min_v=min_velocity)
        value = calculate_fit(new_profile, elev_profile, max_time=time)
        if min_value > value[0]:
            if time > value[1]:  # perfect solution
                v_profile = new_profile
                last_real_solution = v_profile
                min_value = value[0]
                min_time = value[1]
                values.append(value)
            elif abs(time - value[1]) < abs(time - min_time):
                # if this time is closer to max race time than before
                v_profile = new_profile
                min_value = value[0]
                min_time = value[1]
                values.append(value)
        elif time < value[1] and value[1] < min_time and (min_time - time) / time > 0.05:
            # if used more energy than prev, time above race time but faster than prev, and if previous optimal
            # solution is reasonably far from the max race time
            # TODO: handling if solutions are all too far from max race time due to min_velocity being too high
            v_profile = new_profile
            min_value = value[0]
            min_time = value[1]
            values.append(value)

    # Show a plot of those means to see the differences
    value_energies = [i[0] for i in values]
    value_times = [i[1] for i in values]
    fig, axs = plt.subplots(2)
    axs[0].plot(value_energies)
    axs[0].set_title("Energy")
    axs[1].plot(value_times)
    axs[1].set_title("Time")
    plt.show()
    # Show the optimal path
    print(last_real_solution)
