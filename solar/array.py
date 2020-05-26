from math import pi
from solar import SolarDay
import csv
import os

str = ('python3.7 calculation-angles-cell.py')
filename = 'MSXIV-Strategy-Cell-Angles.csv'
#os.system(str)

# To do:
# Create 3D surface as a combination of all cells:
# Takes the average energy from all cells
# Input values into the module_angle to account for total energy
# In series/parallel configuration


def to_rad(angle):
    rad = angle * 2 * pi / 360
    return rad


def integrate(x, y):
    # Given an X and Y data set, numerically integrate
    integral = 0
    for i in range(len(x) - 1):
        integral += (x[i + 1] - x[i]) * (y[i + 1] + y[i]) / 2
    return integral


class SolarArray:
    def data(self):
        array = []
        with open(filename, mode='r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                cell = {"Cell_ID": row[0], "Angle": row[4]}
                array.append(cell)
        # print(array)
        return(array)

    def __init__(self, day, latitude, longitude, timezone, cloudiness):
        self.day = day
        self.lat = latitude
        self.long = longitude
        self.cloud = cloudiness
        self.points = []
        self.time = timezone

    # calculate and store total energy values
    def totalEnergy(self):
        total_energy = 0
        array = self.data()
        for i in range(1, len(self.data())):
            module_angle = float(array[i]['Angle'])
            d = SolarDay(self.day, self.lat, self.long,
                         self.time, self.cloud, module_angle)
            insol = integrate(d.energy_received()[1], d.energy_received()[0])
            energy = insol * 5 * 0.17
            total_energy = total_energy + energy

        return(total_energy)


if __name__ == '__main__':
    test = SolarArray(182, 30.28, 97.73, 8, 0.5)
    print(test.totalEnergy())
