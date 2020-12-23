import argparse
import math
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model
from scipy.optimize import curve_fit
import numpy as np

class MotorEfficiency:

    def log_func(self, x, a, b):
        return a + b * np.log(x)

    def linear_func(self, x, a, b):
        return a + b * x
    
    def exp_func(self, x, a, b, c):
        return a * np.exp(b * x) + c

    func_to_fit = log_func

    def create_points(self, coil):
        dataset = pd.read_csv(coil + 'Data.csv')

        self.speed = dataset['Speed'].values
        self.torque = dataset['Torque'].values

        self.start_pars, cov = curve_fit(f=self.func_to_fit, xdata=self.speed, ydata=self.torque)
        # print(cov)

    def graph(self):
        generated_x = np.linspace(self.speed[0], self.speed[-1], 100)
        generated_y = self.func_to_fit(generated_x, *self.start_pars)
        plt.plot(self.speed, self.torque, 'r+')
        plt.plot(generated_x, generated_y, 'g+')
        plt.xlabel("Speed")
        plt.ylabel("Torque")
        plt.show()

    def __init__(self, coil):
        self.coil = coil
        dataset = pd.read_csv(coil + 'Data.csv')

        # let us determine relationship between speed and torque with voltage*current
        # we will use this predicted value in place of actual current and voltage

        x = dataset[['Speed', 'Torque']]
        y = dataset['Voltage'] * dataset['Current']
        regr = linear_model.LinearRegression()
        regr.fit(x, y)

        self.speed_k = regr.coef_[0]
        self.torque_k = regr.coef_[1]
        self.c = regr.intercept_

    def calc_efficiency(self, speed, torque):
        # formula: efficiency (%) = [pi/30 * speed * torque] / [voltage * current] * 100
        return (math.pi/30 * speed * torque) / (self.speed_k * speed + self.torque_k * torque + self.c) * 100

    def power_draw_needed(self, speed, torque, expected_power):
        return expected_power / (self.calc_efficiency(speed, torque) * 0.01)
    
    def graph_default(self):
        dataset = pd.read_csv(self.coil + 'Data.csv')
        dataset['CalcEfficiency'] = dataset.apply(lambda x: self.calc_efficiency(x.Speed, x.Torque), axis=1)
        speed_values = np.linspace(self.speed[0], self.speed[-1], 100)
        torque_values = self.func_to_fit(speed_values, *self.start_pars)

        torque_values = torque_values[torque_values > 0]
        speed_values = speed_values[len(speed_values) - len(torque_values):]
        assert(len(torque_values) == len(speed_values))

        pred_efficiency = np.array([self.calc_efficiency(speed, torque) for speed, torque in zip(speed_values, torque_values)])
        power_values = np.array([math.pi / 30 * speed * torque for speed, torque in zip(speed_values, torque_values)])

        plt.plot(power_values, pred_efficiency, color='green', label='Additional points')
        plt.plot([math.pi / 30 * speed * torque for speed, torque in zip(dataset['Speed'], dataset['Torque'])], dataset['CalcEfficiency'], color='blue', label='Predicted')
        plt.scatter([math.pi / 30 * speed * torque for speed, torque in zip(dataset['Speed'], dataset['Torque'])], dataset['Efficiency'], color='red', label='Actual')
        # plt.scatter(dataset.index, dataset['Efficiency'], color='blue', label='True')
        # plt.scatter(dataset.index, dataset['CalcEfficiency'], color='red', label='Calculated')
        plt.legend()
        plt.title("Efficiency Calculation Comparions (" + self.coil + " Coil)")
        plt.xlabel("Power")
        plt.ylabel("Efficiency (%)")
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="See coil fit graphs")
    parser.add_argument('-c', '--coil', help='Select HI or LO coil', default="LO")
    args = parser.parse_args()

    if args.coil.upper() != "LO" and args.coil.upper() != "HI":
        print("Choose HI or LO please")
    else:
        motor_efficiency_curve = MotorEfficiency(args.coil.upper())
        # make sure we are creating the parameters for speed, torque values
        motor_efficiency_curve.create_points(args.coil.upper())
        motor_efficiency_curve.graph_default()
        # motor_efficiency_curve.graph()

        