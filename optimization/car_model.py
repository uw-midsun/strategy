from math import sin, cos, sqrt
from numpy import arctan


class Car():

    g = 9.81  # Acceleration due to gravity in m/s^2
    rho = 1.225  # Density of air at room temperature

    def __init__(self, m=720, Crr=0.0015, CdA=0.15, max_force=100):
        self.m = m  # mass of car in kg
        self.Crr = Crr  # Rolling Resistance coefficient of the car
        self.CdA = CdA  # Drag coefficient of the car
        self.max_force = max_force  # Max force of motors in N (Note not real)

    def force_req(self, v, vwind=0, v_old=None, theta=0, timestep=30):
        """
        :param v: velocity of the car in m/s
        :param vwind: velocity of the wind relative to the car (+ve with car)
        :param v_old: speed of the car at the initial point
        :param theta: angle that must be climbed by the car in radians
        :param timestep: time in s between measurements
        :return force: force in N required to power the car
        """
        # If we don't set v_old, we assume v has not changed
        if v_old is None:
            v_old = v

        Ffric = self.m * self.g * cos(theta) * self.Crr
        Fdrag = 0.5 * self.rho * self.CdA * (v + vwind) ** 2
        Fg = self.m * self.g * sin(theta)
        Fa = self.m * (v - v_old) / timestep
        Fmotor = Fa + Ffric + Fdrag + Fg
        return Fmotor

    def max_velocity(self, v_old, vwind=0, theta=0, timestep=30):
        """
        :param v_old: speed of the car at the initial point
        :param vwind: velocity of the wind relative to the car (+ve with car)
        :param theta: angle that must be climbed by the car in radians
        :param timestep: time in s between measurement
        :return velocity: max velocity that the car can travel in m/s
        """
        max_v = v_old - self.force_req(v_old, vwind=vwind, theta=theta) + self.max_force * timestep
        return max_v

    def energy_used(self, v_profile, e_profile, distance=100, wind=0):
        """
        :param v_profile: a series of velocities in m/s separated by a distance
        :param e_profile: a series of elevations in m separated by a distance
        :param distance: distance between points in the profiles
        :return energy used: energy used in J for the path and velocity profile
        """
        # TODO: Add error handling for len(v_profile) != len(e_profile)
        energy = 0
        num_points = len(v_profile)
        # Note we will end 1 before because we don't care about the distance
        # that happens after the last point because it is the "finish line"
        for point in range(num_points - 1):
            v_new = v_profile[point + 1]
            v_old = v_profile[point]
            e_new = e_profile[point + 1][0]
            # pytest fails here because e_profile from
            # pytest does not use variable distances
            e_old = e_profile[point][0]
            e_gain = e_new - e_old
            dist = e_profile[point][1]
            theta = arctan(e_gain / dist)  # Calculate the angle of elev
            v_avg = (v_new + v_old) / 2
            timestep = dist / v_avg
            energy_used = self.force_req(v_new, wind, v_old,
                                         theta, timestep) * dist
            energy += energy_used
        return energy
