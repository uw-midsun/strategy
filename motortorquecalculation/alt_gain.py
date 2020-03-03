import pandas as pd
from haversine import haversine, Unit
from numpy import arctan, geomspace, linspace
from math import sin, cos, ceil, pi
import matplotlib.pyplot as plt
from statistics import mean
import argparse


def kph_to_ms(kph):
    return kph * 0.277778


def degree_to_rad(angle):
    rad = angle * (pi / 180)
    return rad


def rad_to_degree(rad):
    angle = rad * (180 / pi)
    return angle


def above(lst, item):
    for i in range(len(lst)):
        if item > lst[i]:
            index = i
            return index
        else:
            return -1


class TorqueCurve:
    peak_efficiency = 0.96

    def __init__(self, nominal_torque):
        """
        Container object.
        @param nominal_torque: TODO
        @type nominal_torque: float
        """
        self.torque = nominal_torque
        self.curve = []
        self.torque_list = []

    def generate_curve(self):
        # First we generate the bottom half
        efficiencies = geomspace(0.1, self.peak_efficiency, 1000)
        torques = linspace(0.5, self.torque, 1000)
        for point in range(len(torques)):
            self.curve.append((torques[point], efficiencies[point]))
            self.torque_list.append(torques[point])
        # Then we generate the top half
        efficiencies = geomspace(self.peak_efficiency, 0.8, 1000)
        torques = linspace(self.torque, 100, 1000)
        for point in range(len(torques)):
            self.curve.append((torques[point], efficiencies[point]))
            self.torque_list.append(torques[point])


class Car:
    gravity = 9.81
    rho = 1.225
    wheel_radius = 0.26

    def __init__(self, mass, CdA, Crr):
        """
        Model of the car as a function of five forces.
        @param mass: The mass of the car, in kg.
        @type mass: float
        @param CdA: CdA is the combined drag coefficient
        @type CdA: float
        @param Crr:  Crr is the coefficient of rolling resistance
        @type Crr: float
        """
        self.mass = mass  # in kg
        self.CdA = CdA
        self.Crr = Crr

    def force(self, angle, velocity):
        """
        Get the total force given the angle and velocity of the car model.
        @param angle: Angle in degrees.
        @type angle: float
        @param velocity: Velocity of the car in m/s
        @type velocity: float
        @return: Total force on the car
        @rtype: float
        """
        Fg = self.mass * self.gravity * sin(degree_to_rad(angle))
        Ff = self.mass * self.gravity * self.Crr * cos(degree_to_rad(angle))
        Fdrag = 0.5 * velocity ** 2 * self.CdA * self.rho
        Ft = Fg + Ff + Fdrag
        return Ft

    def energy_use(self, distance, angle, velocity):
        """
        Get the total energy used by the car given the angle and velocity.
        @param angle: Angle in degrees.
        @type angle: float
        @param velocity: Velocity of the car in m/s
        @type velocity: float
        @return: Energy used by the car
        @rtype: float
        """
        Ft = self.force(angle, velocity)
        E = Ft * distance
        return E

    def torque_req(self, angle, velocity):
        """
        Returns the torque required per wheel
        @param angle: Angle in degrees.
        @type angle: float
        @param velocity: Velocity of the car in m/s
        @type velocity: float
        @return: Energy used by the car
        @rtype: float
        """
        torque_per_wheel = self.force(angle, velocity) * self.wheel_radius / 2
        return torque_per_wheel

    def speed_req(self, angle, torque):
        """
        returns the speed traveled given a certain torque
        F = tau * 2 / wheel_radius
        F = mgsin(theta) + mgCrrcos(theta) + 0.5v^2CdArho
        sqrt((F - mgsin(theta) - mgCrrCos(theta))/(0.5CdArho)) = v
        @param angle: Angle in degrees.
        @type: float
        @param torque: torque in Nm
        @type float
        @return the speed traveled given a certain torque
        @rtype: float
        """
        velocitysquared = (
            (torque * 2 / self.wheel_radius)
            - (self.mass * self.gravity * sin(degree_to_rad(angle)))
            - (self.mass * self.gravity * self.Crr * cos(degree_to_rad(angle)))
        ) / (0.5 * self.CdA * self.rho)
        return velocitysquared

    def speed_torque_calculator(self, angle, given_speed, min_speed, torque):
        """
        TODO: @Clarke What does this do?
        @param angle: Angle in degrees
        @type angle: float
        @param given_speed:
        @type given_speed: float
        @param min_speed:
        @type min_speed: float
        @param torque:
        @type torque: float
        @return: Speed, torque
        @rtype: (float, float)
        """
        if self.torque_req(angle, given_speed) <= torque:
            return given_speed, self.torque_req(angle, given_speed)
        elif self.speed_req(
            angle, torque
        ) >= min_speed ** 2 and given_speed > self.speed_req(angle, torque):
            return self.speed_req(angle, torque), torque
        elif self.speed_req(
            angle, torque
        ) >= min_speed ** 2 and given_speed < self.speed_req(angle, torque):
            return given_speed, torque
        else:
            required_torque = self.torque_req(angle, min_speed)
            return min_speed, required_torque


def generate_parameters(alt, lat, lon):
    """
    Given the raw data, generate parameters (distances, delta altitude, angles and climb.
    @param alt: Altitude data (
    @type alt: List[float]
    @param lat: Latitude
    @type lat: List[float]
    @param lon: Longitudes
    @type lon: List[float]
    @return: Distances, delta in altitudes, angles and climb.
    @rtype:(List[float], List[float], List[float], List[float])
    """
    dist = [0]
    # TODO: Unused variable: dalt.
    dalt = [0]
    climb = [0]
    angles = [0]
    for i in range(len(alt) - 1):
        dist.append(
            haversine((lat[i], lon[i]), (lat[i + 1], lon[i + 1]), unit=Unit.METERS)
            + dist[i]
        )
        dalt = alt[i + 1] - alt[i]
        angle = dalt / (dist[i + 1] - dist[i])
        angles.append(angle)
        climb.append((180 / pi) * arctan(angle))
    return dist, dalt, climb, angles


def main():
    """
    Plots a graph detailing range (km) over added energy use (W).
    """
    parser = argparse.ArgumentParser(
        description="Choose a map",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--map", help="Required: Map to pick to race on: [WSC|ASC]", required=True
    )
    parser.add_argument(
        "--solar", help="Energy we receive from the solar panel", default=0, type=float
    )
    parser.add_argument(
        "--weight", help="Weight of the car in kg", default=720, type=float
    )
    args = parser.parse_args()

    if args.map == "WSC":
        csv_file = pd.read_csv("wsc_elevation.csv")
        lon = csv_file.Longitude.to_list()
        lat = csv_file.Latitude.to_list()
        alt = csv_file["Elevation (m)"].to_list()
        speed_req = kph_to_ms(80)
    elif args.map == "ASC":
        csv_file = pd.read_csv("ASC2018.csv")
        lon = csv_file.lon.to_list()
        lat = csv_file.lat.to_list()
        alt = csv_file.alt.to_list()
        speed_req = kph_to_ms(60)

    car = Car(args.weight, 0.15, 0.0015)

    dist, _, climb, angles = generate_parameters(alt, lat, lon)
    avg = mean(x for x in climb if x > -(180 / pi) * 0.0085035)
    print("Car torque required per wheel (Nm): ", car.torque_req(avg, speed_req))

    # TODO: Another unused variable: torques. It is overwritten to [] in the loop below right away.
    torques = []
    for angle in climb:
        torques.append(car.torque_req(angle, speed_req))
    torques = linspace(5, 30, 20)

    breakpoints = []
    baseline = -1 * ceil(args.solar)
    wattages = linspace(baseline, baseline + 500, 50)
    total_energies = []
    for i in range(50):
        set_torque = 14  # Nm of torque we want from the motor
        torque_obj = TorqueCurve(set_torque)
        wattage = wattages[i]
        torque_obj.generate_curve()
        efficiencies = torque_obj.curve
        torques = []
        eff = []
        for j in range(len(efficiencies)):
            torques.append(efficiencies[j][0])
            eff.append(efficiencies[j][1])

        data = [(0, 0)]
        min_speed = 7  # minimum allowable speed (m/s)
        for point in range(len(dist)):
            data.append(
                car.speed_torque_calculator(
                    climb[point], speed_req, min_speed, set_torque
                )
            )

        total_energy = 0
        full_length = True
        for point in range(2, len(data)):
            pre_eff_energy = car.energy_use(
                dist[point - 1] - dist[point - 2], climb[point - 1], data[point][0]
            )

            if above(torque_obj.torque_list, data[point][1]) != -1:
                # TODO: efficiency is unused, is it useful?
                efficiency = efficiencies[
                    above(torque_obj.torque_list, data[point][1])
                ][1]
            else:
                efficiency = 0
            total_energy += (
                pre_eff_energy
                + wattage * (dist[point - 1] - dist[point - 2]) / data[point][0]
            )
            if total_energy > 5.04 * 10 ** 7:
                breakpoints.append(dist[point - 1])
                full_length = False
                break
        total_energies.append(total_energy)
        if full_length:
            breakpoints.append(dist[-1])

    break_in_km = [x / 1000 for x in breakpoints]
    normalized_wattages = [x - baseline for x in wattages]
    plt.plot(normalized_wattages, break_in_km)
    plt.xlabel("Added Energy Use (W)")
    plt.ylabel("Range (km)")
    plt.savefig("plot.png")
    plt.show()


if __name__ == "__main__":
    main()
