import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dynamics.car_model import Car
import numpy
from scipy.optimize import minimize
import argparse


global car
car = Car()

parser = argparse.ArgumentParser(description="Add parameters to model")
parser.add_argument("-d", "--distance", type=int, default=5490,
                    help="Distance to travel (m)")
parser.add_argument("-t", "--time", type=int, default=450,
                    help="Maximum allowable time (s)")
parser.add_argument("-v", "--min_velocity", type=int, default=5,
                    help="Minimum allowable velocity (m/s)")
parser.add_argument("-s", "--step", type=int, default=30,
                    help="Distance between elevation profile measurements")
parser.add_argument("-st", "--stop_velocity", type=int, default=7,
                    help="Maximum velocity for stops/turns")
args = parser.parse_args()


def load_course_map(course_name="COTA"):
    """
    :param course_name: name of the course we are loading in
    :return elev_profile: map of the elevations on a course
    """
    if course_name == "COTA":
        with open('COTAelevation_var.txt', 'r') as file:
            line = file.readline()
            data = []
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
        stops = []
        total_dist = 0
        for i in range(len(clean_data) - 1):
            pitch = numpy.arctan(float(clean_data[i][1])
                                 / float(clean_data[i][2]))
            elev_profile.append((pitch, int(clean_data[i][2])))
            total_dist += int(clean_data[i][2])
            if len(clean_data[i]) > 3:
                stops.append(int(clean_data[i][0]))
    if course_name == "ASC":
        pass
    return (elev_profile, stops, total_dist)


def generate_initial_profile(time, distance, e_profile, min_velocity,
                             stop_profile, max_stop_velocity):
    """
    :param time: Maximum allowable time to cover a distance in seconds
    :param distance: Distance to be covered in meters
    :param e_profile: List of pitches the car must travel
    :param min_velocity: Minimum allowable velocity
    :param stop_profile: List of indices where car must stop
    """
    avg_velocity = distance / time
    initial_profile = [avg_velocity]
    for point in range(len(e_profile) - 1):  # We don't care about the endpoint
        pitch = e_profile[point][0]
        dist_step = e_profile[point][1]
        old_v = initial_profile[point - 1]
        timestep = dist_step / old_v
        max_v = car.max_velocity(old_v, theta=pitch, timestep=timestep)
        if stop_profile != [] and stop_profile[0] == point+1:
            initial_profile.append(min(max_v, max_stop_velocity))
            stop_profile.remove(stop_profile[0])
        else:
            if max_v >= avg_velocity:
                initial_profile.append(avg_velocity)
            elif max_v >= min_velocity:
                initial_profile.append(max_v)
            else:
                initial_profile.append(min_velocity)
    # Here we generate the naive solution
    # traveling at the average velocity required
    return initial_profile


if __name__ == "__main__":

    map_data = load_course_map()
    elev_profile = map_data[0]
    stop_profile = map_data[1]
    distance = map_data[2]

    # Load in the distance and necessary time for a lap
    dist_step = args.step
    time = args.time  # max allowable time in s
    min_velocity = args.min_velocity
    max_velocity = 25
    max_stop_velocity = args.stop_velocity
    init_profile = generate_initial_profile(time, distance, elev_profile,
                                            min_velocity, stop_profile.copy(),
                                            max_stop_velocity)

    def objective(v_profile):
        energy = car.energy_used(v_profile, elev_profile, distance=dist_step)
        return energy / 1000000

    def time_constraint(v_profile):
        time_used = [dist_step / v for v in v_profile[1:]]
        return time-sum(time_used)

    def speed_constraint(v_profile):
        error = 0
        for i in range(len(v_profile) - 1):
            timestep = distance / v_profile[i]
            max_velocity = car.max_velocity(v_profile[i], timestep=timestep)
            if v_profile[i] > max_velocity:
                error += max_velocity - v_profile[i]
        return error

    # initial guess
    v0 = numpy.asarray(init_profile)
    
    # bounds
    elements = len(v0)
    bounds = [(min_velocity, max_velocity)] * elements
    for stop in stop_profile:
        bounds[stop-1] = (2, max_stop_velocity)

    # constraints
    condition1 = {'type': 'ineq', 'fun': time_constraint}
    condition2 = {'type': 'ineq', 'fun': speed_constraint}
    conditions = ([condition1, condition2])
    solution = minimize(objective, v0, method='SLSQP',
                        bounds=bounds, constraints=conditions)

    v = solution.x
    print("pitch,velocity")
    for i in range(len(v)):
        print(f"{elev_profile[i][0]},{v[i]}")
    message = solution.message
    status = solution.status
