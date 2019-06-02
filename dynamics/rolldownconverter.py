import numpy as np
import matplotlib.pyplot as plt
# TODO: add data loading for actual data
# Test data
m = 640 # kg
Crr = 0.0015
g = 9.81
rho = 1.225 
CdA = 0.15
vinit = 20
t = np.linspace(0,800,10000)
def power(lst, power):
    # take a list and raise every element to a power
    return [ x ** power for x in lst]
# Assuming the data is evenly spaced
dt = t[1] - t[0]
v = []
v.append(vinit)
i = 0
while v[i] >= 0.5:
    v.append(v[i] - ((Crr * m * g + CdA * rho * v[i] ** 2 / 2) * dt / m))
    i += 1
t = t[0:len(v)]
# The numpy function gradient gives a second order approximation of the derivative of the velocity
a = np.gradient(v,dt)
# We now want to find the relationship between force and velocity
# Given that F = ma = Crr * m * g + 1/2 * rho * CdA * v^2
# We can fit a quadratic curve to our F vs v plot to find CdA and Crr

A = np.array([[sum(power(v,4)), sum(power(v,3)), sum(power(v,2))],
              [sum(power(v,3)), sum(power(v,2)), sum(v)],
              [sum(power(v,2)), sum(v), len(v)]])

b = [0,0,0]
for point in range(len(v)):
    b[0] += v[point] ** 2 * m * a[point]
    b[1] += v[point] * m * a[point]
    b[2] += a[point] * m

B = np.array(b)
x = np.linalg.solve(A,B)
CdAcalc = -x[0] * 2 / rho
Crrcalc = -x[2] / (m * g)
print(CdAcalc, Crrcalc)
