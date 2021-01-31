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

        self.start_pars, _ = curve_fit(f=self.speed_torque_func, xdata=self.rotational_speed, ydata=self.torque)

    def calc_efficiency(self, rotational_speed, torque):
        # formula: efficiency (%)
        # = power from torque and rotational_speed / power from bus voltage and current
        # = [pi / 30 * rotational_speed * torque] / [voltage * current] * 100
        return (math.pi / 30 * rotational_speed * torque) / (self.speed_k * rotational_speed + self.torque_k * torque + self.c) * 100

    def power_draw_needed(self, car_speed, torque, required_power):
        # if pi / 30 * rotational_speed = car_speed, then rotational_speed = car_speed / pi * 30
        return required_power / (self.calc_efficiency(car_speed / math.pi * 30, torque) * 0.01)

    def graph_generated_points(self, ax, left_graph):
        generated_x = np.linspace(self.rotational_speed[0], self.rotational_speed[-1], 100)
        generated_y = self.speed_torque_func(generated_x, *self.start_pars)

        if left_graph == "TORQUE":
            # Speed vs. torque graph
            ax.plot(self.rotational_speed, self.torque, 'b+')
            ax.plot(generated_x, generated_y, 'green')
            ax.ylabel("Torque (Nm)")
        else:
            # Speed vs. power graph
            ax.plot(self.rotational_speed, math.pi / 30 * self.rotational_speed * self.torque, 'r+')
            ax.plot(generated_x, math.pi / 30 * generated_x * generated_y, 'green')
            ax.set_ylabel("Calculated Power (W)")
        
        ax.set_xlabel("Rotational Speed (Nrpm)")
        ax.set_title("Generated Points")

    def graph_predicted_efficiency(self, ax):
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

        ax.plot(power_values, pred_efficiency, color='green', label='Additional points')
        ax.plot(math.pi / 30 * self.rotational_speed * self.torque, self.dataset['CalcEfficiency'], 'b+', label='Predicted')
        ax.scatter(math.pi / 30 * self.rotational_speed * self.torque, self.dataset['Efficiency'], color='red', label='Actual')

        ax.legend()
        ax.set_title("Efficiency Calculation Comparions (" + self.coil + " Coil)")
        ax.set_xlabel("Power (W)")
        ax.set_ylabel("Efficiency (%)")

    def graph(self, left_graph):
        '''
        Graphs information on the motor coil predictions and test data
        Left graph is speed vs. power or speed vs. torque fit
        Right graph is generated predictions, test predictions, and test points for the motor efficiency coil

        @param left_graph: changes left side plot, either "power" for speed vs. power or "torque" for speed vs. power
        '''
        _, (ax1, ax2) = plt.subplots(1, 2)
        self.graph_generated_points(ax1, left_graph)
        self.graph_predicted_efficiency(ax2)
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="See coil fit graphs")
    parser.add_argument('-c', '--coil', help='Select HI or LO coil', default="LO")
    parser.add_argument('-r', '--left', help='Show speed vs. power or speed vs. torque graphs', default="POWER")
    args = parser.parse_args()

    left_graph = args.left.upper() if args.left.upper() == "TORQUE" else "POWER"

    if args.coil.upper() == "LO":
        lo_motor_eff_curve = MotorEfficiency(args.coil.upper())
        lo_motor_eff_curve.graph(left_graph)
    elif args.coil.upper() == "HI":
        hi_motor_eff_curve = MotorEfficiency(args.coil.upper())
        hi_motor_eff_curve.graph(left_graph)
    else:
        print("Invalid argument, choose coil and left graph arguments")
