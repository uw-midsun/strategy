import pandas as pd
from haversine import haversine, Unit
from numpy import arctan, geomspace, linspace
from math import sin, cos, sqrt, ceil
import matplotlib.pyplot as plt
from statistics import mean
import argparse 

def angle_to_rad(angle):
    rad = angle / 57.2958
    return rad

def rad_to_angle(rad):
    angle = rad * 57.2958
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
        # The we generate the top half
        efficiencies = geomspace(self.peak_efficiency, 0.8, 1000)
        torques = linspace(self.torque, 100,  1000)
        for point in range(len(torques)):
            self.curve.append((torques[point], efficiencies[point]))
            self.torque_list.append(torques[point])



class Car:
    
    gravity = 9.81
    rho = 1.225
    wheel_radius = 0.26
    battery_size = 3.888 * 10 ** 7 # Car energy capacity in Joules
    def __init__(self, mass, CdA, Crr):
        self.mass = mass # in kg
        self.CdA = CdA # drag area
        self.Crr = Crr # rolling resistance

    def force(self, angle, velocity, timestep=30):
        Fg = self.mass * self.gravity * sin(angle_to_rad(angle))
        Ff = self.mass * self.gravity * self.Crr * cos(angle_to_rad(angle))
        Fdrag = 0.5 * velocity ** 2 * self.CdA * self.rho
        Faccel = self.mass * (velocity / timestep) # force required to accelerate
        Ft = Fg + Ff + Fdrag + Faccel
        return Ft

    def energy_use(self, distance, angle, velocity, timestep=30):
        Ft = self.force(angle, velocity, timestep)
        E = Ft * distance
        return E

    def torque_req(self, angle, velocity, timestep=30):
        """
        returns the torque required per wheel
        """
        torque_per_wheel = self.force(angle, velocity, timestep) * self.wheel_radius / 2
        return torque_per_wheel

    def speed_req(self, angle, torque):
        """
        returns the speed traveled given a certain torque
        F = tau * 2 / wheel_radius
        F = mgsin(theta) + mgCrrcos(theta) + 0.5v^2CdArho
        sqrt((F - mgsin(theta) - mgCrrCos(theta))/(0.5CdArho)) = v
        """
        velocitysquared= ((torque * 2 / self.wheel_radius) - (self.mass * self.gravity * sin(angle_to_rad(angle))) - (self.mass * self.gravity * self.Crr * cos(angle_to_rad(angle))))/(0.5 * self.CdA * self.rho)
        return velocitysquared
    
    def speed_torque_calculator(self, angle, given_speed, min_speed, torque):
        if self.torque_req(angle, given_speed) <= torque:
            return given_speed, self.torque_req(angle, given_speed)
        elif self.speed_req(angle, torque) >= min_speed ** 2 and given_speed > self.speed_req(angle, torque):
            return self.speed_req(angle, torque), torque
        elif self.speed_req(angle, torque) >= min_speed ** 2 and given_speed < self.speed_req(angle, torque):
            return given_speed, torque
        else:
            required_torque = self.torque_req(angle, min_speed)
            return min_speed, required_torque

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Choose a map')
    parser.add_argument('--map', help='Map to pick to race on', default='ASC')
    parser.add_argument('--solar', help='Energy we receive from the solar panel', default=0, type=float)
    parser.add_argument('--weight', help='Weight of the car in kg', default=720, type=float)
    parser.add_argument('--dir', help='Location where your strategy directory is located', type=str)
    args = parser.parse_args()
    car = Car(args.weight, 0.15, 0.0015)
    min_speed = 7 # minimum allowable speed
    if args.map == 'WSC':
        try:
            csv_file = pd.read_csv(args.dir + '/routemodel/routes/wsc_elevation.csv')
        except:
            raise('You must pass in your strategy directory location')
        lon = csv_file.Longitude.to_list()
        lat = csv_file.Latitude.to_list()
        alt = csv_file['Elevation (m)'].to_list()
        speed_req = 22.2 # 80kph in m/s
    elif args.map == 'ASC':
        try:
            csv_file = pd.read_csv(args.dir + '/routemodel/routes/ASC2018.csv')
        except:
            raise('You must pass in your strategy directory location')
        lon = csv_file.lon.to_list()
        lat = csv_file.lat.to_list()
        alt = csv_file.alt.to_list()
        speed_req = 16.6 # 60 kph in m/s
    dist = [0]
    dalt = [0]
    climb = [0]
    angles = [0]
    for i in range(len(alt) - 1):
        dist.append(haversine((lat[i], lon[i]), (lat[i+1], lon[i+1]), unit = Unit.METERS) + dist[i])
        dalt = alt[i+1] - alt[i]
        angle = dalt / (dist[i+1] - dist[i])
        angles.append(angle)
        climb.append(57.2958 * arctan(angle))
    avg = mean(x for x in climb if x > -57.2958 * 0.0085035)
    #print(car.torque_req(avg, speed_req))
    torques = []
    breakpoint = []
    for angle in climb:
        torques.append(car.torque_req(angle, speed_req))
    torques = linspace(5, 30, 20)
    baseline = -1 * ceil(args.solar)
    wattages = linspace(baseline, baseline + 500, 50)
    total_energies = []
    for i in range(50):
        
        set_torque = 14 # Nm of torque we want from the motor
        torque_obj = TorqueCurve(set_torque)
        wattage = wattages[i]
        torque_obj.generate_curve()
        efficiencies = torque_obj.curve 
        torquess = []
        eff = []
        for j in range(len(efficiencies)):
            torquess.append(efficiencies[j][0])
            eff.append(efficiencies[j][1])

        data = [(0,0)]
        for point in range(len(dist)):
            data.append(car.speed_torque_calculator(climb[point], speed_req, min_speed, set_torque))
        total_energy = 0
        full_length = True
        for point in range(2, len(data)):
            pre_eff_energy = car.energy_use(dist[point - 1] - dist[point - 2], climb[point - 1], data[point][0])
            
            if above(torque_obj.torque_list, data[point][1]) != -1:
                efficiency = efficiencies[above(torque_obj.torque_list, data[point][1])][1] 
            else:
                efficiency = 0 
            total_energy += pre_eff_energy + wattage * (dist[point - 1] - dist[point - 2]) / data[point][0]
            if total_energy > Car.battery_size:
                breakpoint.append(dist[point - 1])
                full_length = False
                break
        total_energies.append(total_energy)
        if full_length:
            breakpoint.append(dist[-1])
    break_in_km = [x / 1000 for x in breakpoint]
    normalized_wattages = [x - baseline for x in wattages]
    plt.xlabel('Added Energy Use (W)')
    plt.ylabel('Range (km)')
    plt.title(args.map)
    plt.plot(normalized_wattages, break_in_km)
    plt.show()
