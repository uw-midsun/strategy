#Cell SOC Estimation class - Coulomb counting by pack data available
#Based off Karl's coulomb counting method
#https://uwmidsun.atlassian.net/wiki/spaces/~karlding/pages/620036100/BMS+SOC+Algorithm+v1.0.0+aka.+We+live+in+a+SOCiety


#This class operates on the assumptions that our pack is perfectly balanced, and there is no evident capacity fade
#SoC returned is between 0 (0%) and 1 (100%)

import sys
import os.path
sys.path.append(os.path.dirname(__file__))
from PackEfficiency import PackEfficiency

class CoulombCounter:
	'''
	36 cell parallel
	36 modules series
	~3.45 Ah per cell
	3.635V nominal
	'''
	def __init__(self):
		self.energy_available = 0
		self.pack_energy = 36 * 36 * 3.45 *3.635 #36S * 36P * 3.45Ah * 3.635V = 16 252.812 Wh
		self.SoC = self.energy_available / self.pack_energy
		self.maxSoC = 1 #the value of self.SoC when at 100% full
		self.PackEff = PackEfficiency()
		#cell ocv is available with PackEff.soc_ocv_curve.get_cell_ocv(self.SoC, max = 1)
		
	def set_SoC(self, soc):
		self.SoC = soc
		self.energy_available = soc * self.pack_energy
		
	def set_energy(self, energy):
		self.energy_available = energy
		self.SoC = self.energy_available / self.pack_energy
		
	def get_soc(self):
		return self.SoC
		
	def _print(self):
		print("SoC: {}  Energy Remaining: {}  Voltage: {}".format(self.SoC, self.energy_available, self.PackEff.soc_ocv_curve.get_cell_ocv(self.SoC, max = self.maxSoC)*36))
	
	#given telemetry updates, discharge the cells
	def telemetry_discharge(self, telemetry_pack_current, telemetry_pack_voltage, telemetry_interval_ms):
		self.discharge(self, telemetry_pack_current * telemetry_pack_voltage, telemetry_interval_ms*1000)
	
	#use a certain amount of power for a certain amount of time
	#dirOUT true for discharge, false for charge
	def discharge(self, power_W, time_S, dirOUT = True):
		if not dirOUT:
			power_W *= -1
		
		#power calculation taking the power loss into account
		power_total, efficiency = self.PackEff.draw_power(power_W, self.SoC, max = self.maxSoC)
		print(power_total)
		
		#total energy in Wh
		energy = power_total * time_S/3600
		
		#discharge
		self.energy_available -= energy
			
		#update SoC
		self.SoC = self.energy_available / self.pack_energy
		


class TestCoulombCounter:
	def __init__(self):
		self.CC = CoulombCounter()
		self.CC._print()
		
	def test(self):
		self.CC.set_SoC(1)
		self.CC._print()
		self.CC.set_SoC(0.75)
		self.CC._print()
	
	def test2(self):
		self.CC.set_SoC(0.9)
		self.CC._print()
		for x in range(4):
			self.CC._print()
			self.CC.discharge(20000, 500)
		self.CC._print()
		
		#expected without other power loss
		print("Expected without Power loss")
		print(0.9 * self.CC.pack_energy - 20000 * 500 / 3600 * 4)

#next step: plot this against another discharge curve
if __name__ == "__main__":
	#print out to console and make sure we get reasonable values
	print ("Starting")
	TCC = TestCoulombCounter()
	print("\n\n Test1: \n")
	TCC.test()
	print("\n\n Test 2: \n")
	TCC.test2()
