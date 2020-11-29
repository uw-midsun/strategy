import matplotlib.pyplot as plt
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from optimization.car_model import Car
from soc.soc_deprecated.SoCEstimation import CoulombCounter

def calculate_SOC_values(v_profile, e_profile, distance, initial_soc, min_speed=None, max_speed=None):
    if min_speed is not None and max_speed is not None:
        car_model = Car(speed_min_ms=min_speed, speed_max_ms=max_speed)
    elif min_speed is not None:
        car_model = Car(speed_min_ms=min_speed)
    elif max_speed is not None:
        car_model = Car(speed_max_ms=max_speed)
    else:
        car_model = Car()

    soc_est = CoulombCounter()

    soc_intervals = [initial_soc]
    soc_est.set_SoC(initial_soc)

    for i in range(len(v_profile) - 1):
        energy_used = car_model.energy_used(v_profile[i: i + 2], e_profile[i: i + 2], distance[i: i + 1])
        #in SoC calculation, wanted units is W = Js^-1, cancelled out in function's conversion so using 1 
        soc_est.discharge(energy_used / 1, 1, True)
        soc_intervals.append(soc_est.get_soc())

    # last point: maintaining velocity for last given distance
    last_point_velocities = [v_profile[-1], v_profile[-1]]
    last_elevation = [e_profile[-1], e_profile[-1]]
    last_energy_used = car_model.energy_used(last_point_velocities, last_elevation, distance[-1])
    soc_est.discharge(last_energy_used / 1, 1, True)
    soc_intervals.append(soc_est.get_soc())

    return soc_intervals

def generate_SOC_graph(v_profile, e_profile, distance, initial_soc=1):
    x_axis = [0]
    for interval_distance in distance:
        x_axis.append(x_axis[len(x_axis) - 1] + interval_distance)

    soc_values = calculate_SOC_values(v_profile, e_profile, distance, initial_soc)
    soc_percentages = [soc * 100 for soc in soc_values]

    # for purpose of graphing velocities as step, start at 0
    v_profile.insert(0, 0)

    fig, ax1 = plt.subplots()
    
    color = 'tab:red'
    ax1.set_xlabel('Distance Travelled (m)')
    ax1.set_ylabel('Velocity (m/s)')
    ax1.yaxis.label.set_color(color)
    ax1.spines['left'].set_color(color)
    ax1.step(x_axis, v_profile, where='pre', color=color)

    ax2 = ax1.twinx()

    color = 'tab:blue'
    ax2.set_ylabel('State of Charge (%)')
    ax2.yaxis.label.set_color(color)
    ax2.spines['right'].set_color(color)
    ax2.plot(x_axis, soc_percentages, color=color)

    plt.title('State of Charge vs. Velocity Graph')
    fig.tight_layout()
    plt.show()