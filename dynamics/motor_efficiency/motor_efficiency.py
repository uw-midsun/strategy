import argparse
import math
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model
from scipy.optimize import curve_fit
import numpy as np

def log_func(self, x, a, b):
    return a + b * np.log(x)

def linear_func(self, x, a, b):
    return a + b * x

def exp_func(self, x, a, b, c):
    return a * np.exp(b * x) + c

class MotorEfficiency:

    speed_torque_func = log_func

    def __init__(self, coil):
        self.coil = coil
        self.dataset = pd.read_csv(coil + 'Data.csv')

        if coil == "HI":
            # remove outlier that exists in hi coil data 
            self.dataset.drop(axis=0, index=11, inplace=True)

        # let us determine relationship between speed and torque with voltage*current
        # we will use this predicted value in place of actual current and voltage
        x = self.dataset[['Speed', 'Torque']]
        y = self.dataset['Voltage'] * self.dataset['Current']
        regr = linear_model.LinearRegression()
        regr.fit(x, y)

        self.speed_k = regr.coef_[0]
        self.torque_k = regr.coef_[1]
        self.c = regr.intercept_

        # generate fit of speed and torque points to generate data
        # see speed_torque_func for function used
        self.rotational_speed = self.dataset['Speed'].values
        self.torque = self.dataset['Torque'].values

        self.start_pars, cov = curve_fit(f=self.speed_torque_func, xdata=self.rotational_speed, ydata=self.torque)

    def calc_efficiency(self, rotational_speed, torque):
        # formula: efficiency (%)
        # = power from torque and rotational_speed / power from bus voltage and current
        # = [pi / 30 * rotational_speed * torque] / [voltage * current] * 100
        return (math.pi / 30 * rotational_speed * torque) / (self.speed_k * rotational_speed + self.torque_k * torque + self.c) * 100

    def power_draw_needed(self, car_speed, torque, required_power):
        # if pi / 30 * rotational_speed = car_speed, then rotational_speed = car_speed / pi * 30
        return required_power / (self.calc_efficiency(car_speed / math.pi * 30, torque) * 0.01)

    def graph_generated_points(self):
        generated_x = np.linspace(self.rotational_speed[0], self.rotational_speed[-1], 100)
        generated_y = self.speed_torque_func(generated_x, *self.start_pars)

        # If want to show speed vs. power:
        plt.plot(self.rotational_speed, math.pi / 30 * self.rotational_speed * self.torque, 'r+')
        plt.plot(generated_x, math.pi / 30 * generated_x * generated_y, 'green')
        plt.ylabel("Calculated Power (W)")
        
        # If want to show speed vs. torque: 
        # plt.plot(self.rotational_speed, self.torque, 'b+')
        # plt.plot(generated_x, generated_y, 'green')
        # plt.ylabel("Torque (Nm)")
        
        plt.xlabel("Rotational Speed (Nrpm)")
        plt.title("Generated Points")

    def graph_predicted_efficiency(self):
        self.dataset['CalcEfficiency'] = self.dataset.apply(lambda x: self.calc_efficiency(x.Speed, x.Torque), axis=1)
        # generate 100 points to demonstrate fit
        speed_values = np.linspace(self.rotational_speed[0], self.rotational_speed[-1], 100)
        torque_values = self.speed_torque_func(speed_values, *self.start_pars)

        # Eliminate torque values that aren't greater than 0 (which will be at start of array)
        # and corresponding values on the speed array
        torque_values = torque_values[torque_values > 0]
        speed_values = speed_values[len(speed_values) - len(torque_values):]

        pred_efficiency = np.array([self.calc_efficiency(speed, torque) for speed, torque in zip(speed_values, torque_values)])
        power_values = np.array([math.pi / 30 * speed * torque for speed, torque in zip(speed_values, torque_values)])

        plt.plot(power_values, pred_efficiency, color='green', label='Additional points')
        plt.plot(math.pi / 30 * self.rotational_speed * self.torque, self.dataset['CalcEfficiency'], 'b+', label='Predicted')
        plt.scatter(math.pi / 30 * self.rotational_speed * self.torque, self.dataset['Efficiency'], color='red', label='Actual')

        plt.legend()
        plt.title("Efficiency Calculation Comparions (" + self.coil + " Coil)")
        plt.xlabel("Power (W)")
        plt.ylabel("Efficiency (%)")

    def graph(self):
        plt.subplot(1, 2, 1)
        self.graph_generated_points()

        plt.subplot(1, 2, 2)
        self.graph_predicted_efficiency()
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="See coil fit graphs")
    parser.add_argument('-c', '--coil', help='Select HI or LO coil', default="LO")
    args = parser.parse_args()

    if args.coil.upper() == "LO":
        lo_motor_eff_curve = MotorEfficiency(args.coil.upper())
        lo_motor_eff_curve.graph()
    elif args.coil.upper() == "HI":
        hi_motor_eff_curve = MotorEfficiency(args.coil.upper())
        hi_motor_eff_curve.graph()
    else:
        print("Invalid argument, choose HI or LO please")
