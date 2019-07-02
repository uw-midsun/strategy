"""
Given:
 - Weight (kg)
 - Car's velocity (m/s)
 - Wind speed (m/s + direction)
 - Car's rolling resistance (Crr)
 - Car's coefficient of aerodynamic drag (CdA)
 - Pitch of the ground (angle, theta)
 - Density of air (rho, kg/m^3)
Need to do:
 - Take these values, and calculate the energy consumption of the car speeding up and maintaing a velocity
Want:
 - We want to know the instantaneous energy consumption of the car

Car: 
 - Friction
 - Aero drag
 - Gravity 
 - Motors (forward) 

To travel a constant velocity, we know sum (a) = 0
To accelerate, a = adesired

F = ma

if a = 0, 
  sum(F) must also be zero

Forward on the left, dragging on the right

Fmotor = Ffric + Fdrag + Fg
Ffric = Fn * Crr
Fn = m * g * cos(theta) 
Fdrag = 1/2 * rho * CdA * v^2
Fg = m * g * sin(theta)
Fmotor = m * g * cos(theta) * Crr + 1/2 * rho * CdA * v^2 + m * g * sin(theta)
Fmotor + ma = m * g * cos(theta) * Crr + 1/2 * rho * CdA * (v+vwind)^2 + m * g * sin(theta)

So if we know all these things, we know exaclty how much energy we require from the motor at any given velocity

What we want is an easy to calculate that!

Given our state inputs, we get our the amount of force the motor needs to apply

Our energy consumption for a given distance d is given by E = Fmotor * distance

Given a velocity profile, give me both the instantaneous force requirement, and the total energy usage
"""

import math
class energyConsumption():
    def __init__(self,m,theta,Crr,rho,CdA,v,vbefore,vwind,distance):
        self.m = m
        self.theta = theta
        self.Crr = Crr
        self.rho = rho
        self.CdA = CdA
        self.v = v
        self.vbefore = vbefore
        self.vwind = vwind
        self.d = distance
        self.drag = 0.5*self.rho*self.CdA*(self.v+self.vwind)*(self.v+self.vwind)
        self.fric = self.m*9.8*self.Crr*math.cos(self.theta)
        self.grav = self.m*9.8*(math.sin(self.theta))

    def instForce(self):
        self.a = (self.v - self.vbefore) / (self.d / ((self.v + self.vbefore) / 2))
        if self.a < 0:
            self.a = 0.05 * self.a
        Fmotor = self.m*9.8*self.Crr*math.cos(self.theta)+0.5*self.rho*self.CdA*(self.v+self.vwind)*(self.v+self.vwind)+self.m*9.8*(math.sin(self.theta))+ self.a
        return Fmotor

    def energyUsed(self):
        Fmotor = self.instForce()
        energy = self.d*Fmotor
        return energy

