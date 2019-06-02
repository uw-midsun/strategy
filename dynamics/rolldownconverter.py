import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from parserdcsv import clean
from scipy import interpolate
# Test data
def generate_test_data():
    global m, Crr, g, rho, CdA, vinit, t, dt, v
    m = 640 # kg
    Crr = 0.0015
    g = 9.81
    rho = 1.225 
    CdA = 0.15
    vinit = 25
    t = np.linspace(0,800,10000)
    dt = t[1] - t[0]
    v = []
    v.append(vinit)
    i = 0
    while v[i] >= 0.5:
        v.append(v[i] - ((Crr * m * g + CdA * rho * v[i] ** 2 / 2) * dt / m))
        i += 1
    t = t[0:len(v)]
generate_test_data()
data = clean("~/midsun/dynamics/rolldowndata/RollDown2019-06-02-8.csv")
x = data['time']
y = data['average_velocity']
fuzz = 5
f = interpolate.interp1d(x[0::fuzz], y[0::fuzz], kind = 'cubic')
t = np.linspace(x.iloc[1], x.iloc[-fuzz], 10000)
v = f(t)
polyv = np.polyfit(t,v,3)
vsmooth = polyv[-4] * t ** 3 + polyv[-3] * t ** 2 + polyv[-2] * t + polyv[-1]
polya = np.polyder(polyv)
a = polya[-3] * t ** 2 + polya[-2] * t + polya[-1]
poly = np.polyfit(vsmooth, a, 2)
plt.plot(t,v)
plt.show()

CdAcalc = -poly[0] * 2 * m / rho
Crrcalc = -poly[2] /  g
print("Your calculated CdA is {0:.5f} and your calculated Crr is {1:.5f}".format(CdAcalc, Crrcalc))
