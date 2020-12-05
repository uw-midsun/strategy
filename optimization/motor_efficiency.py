import argparse
import math
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model

class MotorEfficiency:

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
    
    def graph_default(self):
        dataset = pd.read_csv(self.coil + 'Data.csv')
        dataset['CalcEfficiency'] = dataset.apply(lambda x: self.calc_efficiency(x.Speed, x.Torque), axis=1)

        plt.scatter(dataset.index, dataset['Efficiency'], color='blue', label='True')
        plt.scatter(dataset.index, dataset['CalcEfficiency'], color='red', label='Calculated')
        plt.legend()
        plt.title("Efficiency Calculation Comparions (" + self.coil + " Coil)")
        plt.xlabel("Datapoint #")
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
        motor_efficiency_curve.graph_default()
        