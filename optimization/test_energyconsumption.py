import pytest
from energyconsumption import *
 
def test_energyconsumptionTime():
   calcEnergyWithTime = energyConsumption(2,[2,5,3],3,5,2,[3,10,5],[1,8,2],[0.2,4,1],[4,2,3],3).energyUsedWithTime()
   assert calcEnergyWithTime
   print(calcEnergyWithTime)

   calcEnergyWithTime = energyConsumption(9,[0.2,0.3,0.8],4,5,12,[4,39,5],[2,8,10],[9,2,14],[9,19,4],3).energyUsedWithTime()
   assert calcEnergyWithTime
   print(calcEnergyWithTime)

   calcEnergyWithTime = energyConsumption(12,[0.2,0.3,0.8,0.6],4,5,12,[4,39,5,14],[2,8,10,29],[9,2,14,41],[9,19,4,34],4).energyUsedWithTime()
   assert calcEnergyWithTime
   print(calcEnergyWithTime)

def test_energyconsumptionDistance():
   calcEnergyWithDistance = energyConsumption(2,[2,5,3],3,5,2,[3,10,5],[1,8,2],[0.2,4,1],[4,2,3],3).energyUsedWithDistance()
   assert calcEnergyWithDistance
   print(calcEnergyWithDistance)

   calcEnergyWithDistance = energyConsumption(9,[0.2,0.3,0.8],4,5,12,[4,39,5],[2,8,10],[9,2,14],[9,19,4],3).energyUsedWithDistance()
   assert calcEnergyWithDistance
   print(calcEnergyWithDistance)

   calcEnergyWithDistance = energyConsumption(12,[0.2,0.3,0.8,0.6],4,5,12,[4,39,5,14],[2,8,10,29],[9,2,14,41],[9,19,4,34],4).energyUsedWithDistance()
   assert calcEnergyWithDistance
   print(calcEnergyWithDistance)

