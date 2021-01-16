import matplotlib.pyplot as plt
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from optimization.car_model import Car
from soc.soc_deprecated.SoCEstimation import CoulombCounter

def calculate_SOC_values(v_profile, e_profile, distances, initial_soc, min_speed=None, max_speed=None):
    """
    Calculates state of charge (SOC) array, representing SOC points during race specified by parameters

    :param v_profile: list of velocities that car travels (m/s)
    :param e_profile: list of elevations that car travels (m)
    :param distances: list of distances, specifying distance that 
        each speed in v_profile is travelled (m)
    :param initial_soc: float representing the initial battery state 
        (where 1 means fully charged, 0 is empty)
    :param min_speed: float representing minimum speed car must travel (m/s),
        defaults to None (no min)
    :param max_speed: float representing maximum speed car must travel (m/s), 
        defaults to None (no max)

    :return: list of state of charges, starting with initial_soc, 
        and SOC at the end of each interval of velocity.
    """

    if min_speed is not None and max_speed is not None:
        car_model = Car(speed_min_ms=min_speed, speed_max_ms=max_speed)
    elif min_speed is not None:
        car_model = Car(speed_min_ms=min_speed)
    elif max_speed is not None:
        car_model = Car(speed_max_ms=max_speed)
    else:
        car_model = Car()

    soc_est = CoulombCounter()

    soc_points = [initial_soc]
    soc_est.set_SoC(initial_soc)

    for i in range(len(v_profile) - 1):
        # Find energy used within each velocity/elevation interval
        energy_used = car_model.energy_used(v_profile[i: i + 2], e_profile[i: i + 2], distances[i: i + 1])
        # in `discharge`, method parameter units is W = Js^-1, but energy_used is in J
        # assume time span of 1s, conversion cancels out
        soc_est.discharge(power_W=energy_used / 1, time_S=1, dirOUT=True)
        soc_points.append(soc_est.get_soc())

    # last point: maintaining velocity for last given distance
    last_point_velocities = [v_profile[-1], v_profile[-1]]
    last_elevation = [e_profile[-1], e_profile[-1]]
    last_energy_used = car_model.energy_used(last_point_velocities, last_elevation, distances[-1])
    soc_est.discharge(last_energy_used / 1, 1, True)
    soc_points.append(soc_est.get_soc())

    return soc_points

def generate_SOC_graph(v_profile, e_profile, distances, initial_soc=1):
    """
    Graphs velocity and state of charge (SOC) vs. distance travelled for some race defined by parameters. 

    These parameters reflect those in energy_used from car_model.py
    :param v_profile: list of speeds that car travels (m/s)
    :param e_profile: list of elevations that car travels (m)
    :param distances: list of distances, specifying distance that 
        each speed in v_profile is travelled (m)
    :param initial_soc: float representing the initial battery state 
        (where 1 means fully charged, 0 is empty). Default is 1.
    """

    # start race at 0m travelled
    distance_travelled = [0]
    for interval_distance in distances:
        distance_travelled.append(distance_travelled[len(distance_travelled) - 1] + interval_distance)

    soc_values = calculate_SOC_values(v_profile, e_profile, distances, initial_soc)
    soc_percentages = [soc * 100 for soc in soc_values]

    # for purpose of graphing velocities as step, start at 0
    v_profile.insert(0, 0)

    fig, ax1 = plt.subplots()
    
    color = 'tab:red'
    ax1.set_xlabel('Distance Travelled (m)')
    ax1.set_ylabel('Velocity (m/s)')
    ax1.yaxis.label.set_color(color)
    ax1.spines['left'].set_color(color)
    ax1.step(distance_travelled, v_profile, where='pre', color=color)

    ax2 = ax1.twinx()

    color = 'tab:blue'
    ax2.set_ylabel('State of Charge (%)')
    ax2.yaxis.label.set_color(color)
    ax2.spines['right'].set_color(color)
    ax2.plot(distance_travelled, soc_percentages, color=color)

    plt.title('State of Charge vs. Velocity Graph')
    fig.tight_layout()
    plt.show()
