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

Our energy consumption for a given time t is given by E = Fmotor * t

Given a velocity profile, give me both the instantaneous force requirement, and the total energy usage
"""

import math
class energyConsumption():
    def __init__(self,m,theta,Crr,rho,CdA,v,vwind,a,d,t):
        self.m = m #mass of car
        self.theta = theta #angle of car
        self.Crr = Crr  #angle of elevation, in radians
        self.rho = rho
        self.CdA = CdA
        self.v = v #velocity of car
        self.vwind = vwind #velocity of wind
        self.a = a #acceleration of car
        self.d = d #distance traveled (put in an array of 0 if calculate energy with time. Assuming distance to be distance travelled between since previous point, not culmulative )
        self.t = t #total duration for total energy (put in an array of 0 if calculate energy with distance)

    def instForce(self,thisMoment):
        if self.v[thisMoment]<0:
            raise Exception('velocity should not be negative.') #reject negative velocities
        else:
            Fn = self.m * 9.81 * (math.cos(self.theta[thisMoment])) #normal force
        
            Ffric = Fn * self.Crr #frictional force
            allVel = self.v[thisMoment] + self.vwind[thisMoment] #overall velocity of vehicle
            Fdrag = 0.5 * self.rho * self.CdA * (allVel) * (allVel) #aero drag force
            Fg = self.m * 9.81 * (math.sin(self.theta[thisMoment])) #gravity
            ma = self.a[thisMoment] * self.m #acceleration
            Fmotor = (Ffric + Fdrag + Fg) - ma #force of motor
            return Fmotor

    def energyUsedWithTime(self):
        energy = 0 #initially energy used is 0
        time = self.t # time variable from input
        for i in range(time): #loop through each second
            forceAtTime = self.instForce(i) #calculate the force at this second
            energy = energy + forceAtTime #total energy is the previous energy plus the energy used at this second
        return energy
# Test:
# newInfo = energyConsumption(5,6,3,5,2,[3,10,5],[1,8,2],3)
# print(newInfo.energyUsed())

    def energyUsedWithDistance(self):
        energy = 0 #initialize energy variable
        for i in range(len(self.d)): #loop through each distance point
            forceAtMoment = self.instForce(i) #force at this point
            work = forceAtMoment * self.d[i] #energy at this point is force * distance travelled
            energy = work + energy #sums up energy
        return energy
    
