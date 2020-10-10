import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import argparse

class LOCoilCurve:

    # from datasheets
    # removed first (0, 0) and replaced with (0.001, 0.001)
    # (because log)
    efficiency = np.array([0.001, 50.1, 81.8, 87.9, 90.4, 91.9, 92.3, 
        92.3, 92.4, 92.4, 92.5, 92.5, 91.5, 91.0, 89.5, 87.4])

    torque = np.array([0.001, 0.6, 3.2, 5.3, 7.3, 9.4, 11.4, 15.4, 19.6,
        23.8, 28.3, 32.6, 36.9, 41.2, 52.1, 62.6])

    def power_draw(self, torque_required_Nm, energy_draw_W, time_s):
        pass

    def log_func(self, x, a, b):
        return a + b * np.log(x)

    def linear_func(self, x, m, b):
        return m * x + b

    def __init__(self):
        # haven't used covariance
        self.start_pars, cov = curve_fit(f=self.log_func, xdata=self.torque[:6],
            ydata=self.efficiency[:6])
        self.res = self.efficiency[:6] - self.log_func(self.torque[:6], *self.start_pars)

        self.m = round((self.efficiency[-1] - self.efficiency[4]) \
            / (self.torque[-1] - self.torque[4]), 8)
        self.b = self.efficiency[-1] - self.m * self.torque[-1]

        np.append(self.res,
            [self.efficiency[point] 
            - self.linear_func(self.torque[point], self.m, self.b)
            for point in range(len(self.torque[6:]))])

    def graph(self):
        x_vals = np.linspace(0.001, self.torque[5], 100)
        y_vals = self.log_func(x_vals, *self.start_pars)
        plt.plot(x_vals, y_vals)

        x_vals_end = np.linspace(self.torque[5], self.torque[-1], 100)
        y_vals_end = self.linear_func(x_vals, self.m, self.b)
        plt.plot(x_vals_end, y_vals_end)

        plt.plot(self.torque, self.efficiency, 'r+')
        plt.title("LO Coil")
        plt.show()

class HICoilCurve:

    # from data sheets
    # removed inital point (0, 0) and replaced with (0.001, 0.001)
    # (because log)
    efficiency = np.array([0.001, 45.7, 78.3, 84.2, 87.2, 88.9, 89.9, 90.7, 
        91.3, 91.5, 91.8, 91.5, 91.4, 90.9, 89.7, 88.0])

    torque = np.array([0.001, 0.6, 2.7, 4.4, 6.0, 7.9, 9.6, 13.1, 16.7, 
        20.4, 24.2, 57.9, 31.7, 35.5, 44.9, 54.0])
        
    def power_draw(self, torque_required_Nm, energy_draw_W, time_s):
        pass

    def log_func(self, x, a, b):
        return a + b * np.log(x)

    def linear_func(self, x, m, b):
        return m * x + b

    def __init__(self):
        # not using covariance
        self.start_pars, cov = curve_fit(f=self.log_func, xdata=self.torque[:6],
            ydata=self.efficiency[:6])
        self.res = self.efficiency[:6] - self.log_func(self.torque[:6], *self.start_pars)

        self.m = round((self.efficiency[-1] - self.efficiency[4]) \
            / (self.torque[-1] - self.torque[4]), 8)
        self.b = self.efficiency[-1] - self.m * self.torque[-1]

        np.append(self.res,
            [self.efficiency[point] 
            - self.linear_func(self.torque[point], self.m, self.b)
            for point in range(len(self.torque[6:]))])

    def graph(self):
        x_vals = np.linspace(0.001, self.torque[5], 100)
        y_vals = self.log_func(x_vals, *self.start_pars)
        plt.plot(x_vals, y_vals)

        x_vals_end = np.linspace(self.torque[5], self.torque[-1], 100)
        y_vals_end = self.linear_func(x_vals_end, self.m, self.b)
        plt.plot(x_vals_end, y_vals_end)

        plt.plot(self.torque, self.efficiency, 'r+')
        plt.title("HI Coil")
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='See coil fit graphs')
    parser.add_argument('-c', '--coil', help='Select HI or LO coil', default="LO")
    args = parser.parse_args()

    if args.coil.upper() == "LO":
        lo_coil = LOCoilCurve()
        lo_coil.graph()
    elif args.coil.upper() == "HI":
        hi_coil = HICoilCurve()
        hi_coil.graph()
    else:
        print("Choose HI or LO please")
