import matplotlib.pyplot as plt
import numpy as np
import itertools
import math

#To fix - still energy left at 0% - 2.85V at end due to IR voltage drop
#This requires a more precise cell cycling profile generated with a SMU
#0% SoC is defined as when the cell drops below 2.5V under a 3A load.

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__)))
fName = "Test//CellDataFileTestMJ1.txt"

class SoC_OCV:
	def __init__(self):
		#includes 0.050 cell and 0.035 cable, from tests done on single cell
		#This is the Resistance present when the chg-discharge curve was done, not the pack resistance
		#Should be eplicitly tested on the setup. This is a rough estimate of what I expect it was, as we never measured it.
		IR = 0.085 
		four_parallel_IR = ((IR - 0.035) / 4) + 0.035

		#read data from txt files generated during discharge test
		with open(fName) as f_in:
			#fill matrices with data from file (all are lists)
			voltage, current, soc = np.loadtxt(itertools.islice(f_in, 1, None, 2), delimiter = '\t', usecols = (1,3,9), unpack = True)
		
		#Estimate the ocv of the cell, only taking the internal resistance into account (assuming no voltage relaxation or recovery)
		v_ocv = voltage + IR * current

		# make points list with x - y pairs
		self.points = list(zip(soc, v_ocv))
		self.points.sort(key=lambda tup: tup[1]) 
		self.soc = [x for (x, y) in self.points]
		self.v_ocv =  [y for (x, y) in self.points]
		# Graph of the error of the SOC over the entire discharge (% error)
		
	def get_soc_and_v_ocv(self):
		return self.soc, self.v_ocv
	
	def get_points(self):
		return self.points
	
	def get_cell_ocv(self, soc: float or int) -> list:
		if (soc > self.soc[-1] or soc < self.soc[0]):
			raise Exception("The soc value is out of predicted range")
		
		max_soc = len(self.soc) - 1
		min_soc = 0

		while min_soc <= max_soc:
			mid_soc = math.floor((max_soc + min_soc) / 2)
			if self.soc[mid_soc] < soc:
				min_soc = mid_soc + 1
			elif self.soc[mid_soc] > soc:
				max_soc = mid_soc - 1
			else:
				return self.v_ocv[mid_soc]
		
		min_soc = max_soc - 1

		if min_soc >= 0:
			return self.__find_not_in_search__(soc, min_soc, True)
		else:
			min_soc = 0
			return self.__find_not_in_search__(soc, min_soc, True)
	
	def __find_not_in_search__(self, value_used_to_find: int, min: int, is_soc: bool) -> float or int:
		ocv0 = 0
		ocv1 = 0
		soc0 = 0
		soc1 = 0

		# Guess: Length of soc array is equal to the ocv array
		for index in range(min, len(self.soc)):
				if (self.soc[index] < value_used_to_find):
					soc0 = self.soc[index]
					ocv0 = self.v_ocv[index]
				elif ((self.soc[index] > value_used_to_find)):
					soc1 = self.soc[index]	
					ocv1 = self.v_ocv[index]
					break

		if is_soc:
			ocv = round(((value_used_to_find - soc0)*(ocv1 - ocv0) / (soc1 - soc0)) + ocv0, 6)
			return ocv
		else:
			soc = round(soc1 - ((ocv1 - value_used_to_find)*(soc1 - soc0) / (ocv1 - ocv0)), 6)
			return soc		
	
	def plot_graph(self):
		plt.plot(self.soc, self.v_ocv, c = 'r')
		plt.title("SOC vs. OCV values based on test data")
		plt.xlabel("State of Charge (SOC)")
		plt.ylabel("Open Circuit Voltage (OCV)")
		plt.grid(True)
		plt.show()
	

	def correct_soc(self, ocv: float or int, current: int or float) -> int or float:
		if current < 2:
			if (ocv > self.v_ocv[-1] or ocv < self.v_ocv[0]):
				raise Exception("The open circuit voltage value is out of predicted range")
			
			max_ocv = len(self.v_ocv) - 1
			min_ocv = 0

			while min_ocv <= max_ocv:
				mid_ocv = math.floor((max_ocv + min_ocv) / 2)
				if self.v_ocv[mid_ocv] < ocv:
					min_ocv = mid_ocv + 1
				elif self.v_ocv[mid_ocv] > ocv:
					max_ocv = mid_ocv - 1
				else:
					return self.soc[mid_ocv]
		
			min_ocv = max_ocv - 1

			if min_ocv >= 0:
				return self.__find_not_in_search__(ocv, min_ocv, False)
			else:
				min_ocv = 0
				return self.__find_not_in_search__(ocv, min_ocv, False)

		else:
			raise Exception('Current is too high')

class test_SoC_OCV:
	def __init__(self):
		self.SoCOCV = SoC_OCV()
	
	def test(self):
		test1 = self.SoCOCV.get_cell_ocv(100)
		test2 = self.SoCOCV.get_cell_ocv(75)
		test3 = self.SoCOCV.get_cell_ocv(25)
		test4 = self.SoCOCV.get_cell_ocv(0)
		print("Get OCV test:")
		print(f"regular 100: {test1}")
		print(f"regular 75: {test2}")
		print(f"regular 25: {test3}")
		print(f"regular 0: {test4}")
		print('')
		print("Correct SOC test:")
		print(f"regular 100: {self.SoCOCV.correct_soc(test1, 1)}")
		print(f"regular 75: {self.SoCOCV.correct_soc(test2, 1)}")
		print(f"regular 25: {self.SoCOCV.correct_soc(test3, 1)}")
		print(f"regular 0: {self.SoCOCV.correct_soc(test4, 1)}")

	def test_plot_graph(self):
		self.SoCOCV.plot_graph()

testing = test_SoC_OCV()
testing.test()