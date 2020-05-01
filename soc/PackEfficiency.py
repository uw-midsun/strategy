#this is programmed in notepad++ and not tested.

import cmath

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
		self._pack_resistance = 0.055
	
	#if we want say 1000W at the motors, we will need to draw more power (1050W) from the cells
	def draw_power(self, power_outside_pack_W):
		pack_ocv = get_pack_ocv() #from SoC-OCV curve or telemetry, assume cells are balanced
		
		#solve quadratic equation to find current
		#I^2Ri - IVo + Po = 0
		current_draw = (pack_ocv - cmath.sqrt((pack_ocv ** 2) - (4 * self._pack_resistance * power_outside_pack_W))) / (2 * (self._pack_resistance))
		#this power loss is wasted as heat through the resistive elements
		power_loss = (current_draw ** 2) * self._pack_resistance
		
		#the power drawn from the cell itself (before resistive losses from internal resistance), the actual power draw for SoC estimation
		power_inside_pack = power_outside_pack_W + power_loss
		
		#1 = 100% efficiency
		efficiency = (power_inside_pack - power_loss) / power_inside_pack
		
		return power_inside_pack

def get_pack_ocv():
		return 0.0