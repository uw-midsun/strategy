import matplotlib.pyplot as plt
import numpy as np
import cmath

import sys
import os.path
sys.path.append(os.path.dirname(__file__))
from SoC_OCV import SoC_OCV

class PackEfficiency:
	'''
	resistance of the pack in ohms
	cell IR = 50mOhm
	36 cells in parallel = 50mOhm / 36 = 1.389mOhm
	36 modules in series = 1.389mOhm * 36 = 50mOhm
	Contactor x4 = 0.8mOhm
	Copper busbars, cables, and connections ~= 1mOhm
	Fuse Resistance ~= 1mOhm
	Connector resistance ~= 1mOhm
	Total = ~55mOhm
	
	assume this is constant for now, implement changes for temp, SoC variations later
	power loss in a pack is due primarily to ohmic heating
	'''
	
	def __init__(self):
		self.pack_resistance = 0.055
		
		#initialize SoC-OCV model curve
		self.soc_ocv_curve = SoC_OCV()
	
	#if we want say 1000W at the motors, we will need to draw more power (1050W) from the cells
	def draw_power(self, power_outside_pack_W, soc, max = 100): #max is the maximum value for 100% SoC
		if power_outside_pack_W == 0:
			return (0, 1)
		
		#pack_ocv = 36*4 #from SoC-OCV curve or telemetry, assume cells are balanced
		pack_ocv = self.soc_ocv_curve.get_cell_ocv(soc, max) * 36
		print("Pack OCV: {}".format(pack_ocv))
		
		#solve quadratic equation to find current
		#I^2Ri - IVo + Po = 0
		current_draw = (pack_ocv - cmath.sqrt((pack_ocv ** 2) - 
			(4 * self.pack_resistance * power_outside_pack_W))) \
			/ (2 * self.pack_resistance)
		print("Current Draw: {}".format(current_draw))
		
		#this power loss is wasted as heat through the resistive elements
		power_loss = (current_draw**2)*self.pack_resistance
		
		#the power drawn from the cell itself (before resistive losses from internal resistance), the actual power draw for SoC estimation
		power_inside_pack = power_outside_pack_W + power_loss
		
		#1 = 100% efficiency
		#discharging efficiency - useable energy / given energy
		if power_outside_pack_W > 0:
			efficiency = (power_inside_pack - power_loss) / power_inside_pack
		#charging efficiency - power loss will be negative in this case - useable energy / given energy
		else:
			efficiency = (power_inside_pack) / power_outside_pack_W
			
		return (power_inside_pack, efficiency)
		
		
#Make sure we get values that make sense
class Test_Pack_Efficiency:
	def __init__(self):
		self.packEfficiency = PackEfficiency()
	def test(self):
		power, efficiency = self.packEfficiency.draw_power(100, 100)
		print("100W Test: {} Eff: {}".format(power, efficiency))
		power, efficiency = self.packEfficiency.draw_power(500, 90)
		print("500W Test: {} Eff: {}".format(power, efficiency))
		power, efficiency = self.packEfficiency.draw_power(5000, 80)
		print("5000W Test: {} Eff: {}".format(power, efficiency))
		power, efficiency = self.packEfficiency.draw_power(20000, 10)
		print("20000W Test: {} Eff: {}".format(power, efficiency))
		power, efficiency = self.packEfficiency.draw_power(0, 10)
		print("0W Test: {} Eff: {}".format(power, efficiency))
		power, efficiency = self.packEfficiency.draw_power(-500, 50)
		print("-500W Test: {} Eff: {}".format(power, efficiency))
		power, efficiency = self.packEfficiency.draw_power(-5000, 80)
		print("-5000W Test: {} Eff: {}".format(power, efficiency))
		
		power, efficiency = self.packEfficiency.draw_power(20000, 100)
		print("\n\n20000W  100% Test: {} Eff: {}".format(power, efficiency))
		power, efficiency = self.packEfficiency.draw_power(20000, 50)
		print("20000W 50% Test: {} Eff: {}".format(power, efficiency))
		power, efficiency = self.packEfficiency.draw_power(20000, 0)
		print("20000W 0% Test: {} Eff: {}".format(power, efficiency))


'''
#Testing Code	
print ("Testing Started")
pe = Test_Pack_Efficiency()
pe.test()
'''

if __name__ == "__main__":
	#plot efficiency and power loss vs power draw
	#make sure we get reasonable values

	pet = Test_Pack_Efficiency()
	pet.test()

	pe = PackEfficiency()

	p_array = []
	e_array = []
	w_array = []

	for i in range(0, 20000, 1000):
		power, efficiency = pe.draw_power(i, 60)
		p_array.append(power)
		e_array.append(efficiency)
		w_array.append(power - i)
		
	print(p_array)
	print(e_array)
		
	fig, ax = plt.subplots()
	ax.plot(p_array, e_array, 'b-',label = '%e')
	plt.ylabel('Efficiency')
	plt.xlabel('Power Draw')
	
	ax2 = ax.twinx()
	ax2.set_ylabel('Power Loss')
	ax2.plot(p_array, w_array)
	
	plt.show()
	