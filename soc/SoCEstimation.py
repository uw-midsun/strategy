#Cell SOC Estimation class - Coulomb counting by energy (Amp draw over telemetry)
#Based off Karl's coulomb counting method
#https://uwmidsun.atlassian.net/wiki/spaces/~karlding/pages/620036100/BMS+SOC+Algorithm+v1.0.0+aka.+We+live+in+a+SOCiety
#not really a coulomb counter, more of an energy meter.

#how is this being accessed, etc??
#Will it be different when used on telemetry data / modelling
#this is programmed in notepad++ and not tested.

class CoulombCounter:
	'''
	36 cell parallel
	36 modules series
	~3.45 Ah per cell
	3.635V nominal
	'''
	def __init__(self):
		self._energy_available = 0
		self._pack_energy = 36 * 36 * 3.45 * 3.635
		self._SoC = self._energy_available / self._pack_energy
		
	def set_SoC(self, soc):
		self._SoC = soc
		self._energy_available = soc * self._pack_energy
		
	def set_energy(self, energy):
		self._energy_available = energy
		self._SoC = self._energy_available / self._pack_energy
		
	def get_soc(self):
		return self._SoC
	
	#given telemetry updates, discharge the cells
	def telemetry_discharge(self, telemetry_pack_current, telemetry_pack_voltage, telemetry_interval_ms):
		self.discharge(self, telemetry_pack_current * telemetry_pack_voltage, telemetry_interval_ms*1000)
	
	#use a certain amount of power for a certain amount of time
	#dirOUT true for discharge, false for charge
	def discharge(self, power_W, time_S, dirOUT):
		#total energy in kWh
		energy = power_W * time_S / 3600 / 1000
		
		if dirOUT:
			#discharge
			self._energy_available -= energy
		else:
			#charge
			self._energy_available += energy
			
		#update SoC
		self._SoC = self._energy_available / self._pack_energy