import matplotlib.pyplot as plt
import numpy as np
import itertools
import math

from sklearn import datasets, linear_model, metrics
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

#To fix - still energy left at 0% - 2.85V at end due to IR voltage drop
#This requires a more precise cell cycling profile generated with a SMU
#0% SoC is defined as when the cell drops below 2.5V under a 3A load.

import sys
import os.path
from numpy.core.overrides import verify_matching_signatures

from numpy.lib.shape_base import _make_along_axis_idx
sys.path.append(os.path.join(os.path.dirname(__file__)))
fName = "CellDataFileTestMJ1.txt"

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
	
	def get_cell_ocv(self, soc: float or int):
		if (soc > self.soc[-1] or soc < self.soc[0]):
			raise Exception("The soc value if out of predicted range")
		
		max_soc = len(self.soc) - 1
		min_soc = 0

		while (min_soc <= max_soc):
			mid_soc = math.floor((max_soc + min_soc) / 2)
			if (self.soc[mid_soc] < soc):
				min_soc = mid_soc + 1
			elif (self.soc[mid_soc] > soc):
				max_soc = mid_soc - 1
			else:
				return self.v_ocv[mid_soc]
		
		min_soc = max_soc - 10
		return self.__find_not_in_search__(soc, min_soc)
	
	def __find_not_in_search__(self, soc: int, min_soc: int):
		ocv0 = 0
		ocv1 = 0
		soc0 = 0
		soc1 = 0
		for index in range(min_soc, len(self.soc)):
			if (self.soc[index] < soc):
				soc0 = self.soc[index]
				ocv0 = self.v_ocv[index]
			elif ((self.soc[index] > soc)):
				soc1 = self.soc[index]	
				ocv1 = self.v_ocv[index]
				break
		ocv = round(((soc - soc0)*(ocv1 - ocv0) / (soc1 - soc0)) + ocv0, 6)
		return ocv
	
	def plot_graph(self):
		plt.plot(self.soc, self.v_ocv, c = 'r')
		plt.title("SOC vs. OCV values based on test data")
		plt.xlabel("State of Charge (SOC)")
		plt.ylabel("Open Circuit Voltage (OCV)")
		plt.grid(True)
		plt.show()

class test_SoC_OCV:
	def __init__(self):
		self.SoCOCV = SoC_OCV()
	
	def test(self):
		#print("Open Circuit Voltage for {} State of Charge is ".format(value) + str(self.SoCOCV.get_cell_ocv(value)))
		print("Linear Version:")
		print(f"regular 100: {self.SoCOCV.get_cell_ocv(100)}")
		print(f"binary 100: {self.SoCOCV.get_binary_sort(100)}")
		print(f"regular 75: {self.SoCOCV.get_cell_ocv(75)}")
		print(f"binary 75: {self.SoCOCV.get_binary_sort(75)}")
		print(f"regular 25: {self.SoCOCV.get_cell_ocv(25)}")
		print(f"binary 25: {self.SoCOCV.get_binary_sort(25)}")
		print(f"regular 0: {self.SoCOCV.get_cell_ocv(0)}")
		print(f"binary 0: {self.SoCOCV.get_binary_sort(0)}")
	
	def test_plot_graph(self):
		self.SoCOCV.plot_graph()

testing = test_SoC_OCV()
testing.test()