import matplotlib.pyplot as plt
import numpy as np
import itertools

#from sklearn import datasets, linear_model, metrics
#from sklearn.preprocessing import PolynomialFeatures
#from sklearn.pipeline import make_pipeline

#To fix - still energy left at 0% - 2.85V at end due to IR voltage drop
#This requires a more precise cell cycling profile generated with a SMU
#0% SoC is defined as when the cell drops below 2.5V under a 3A load.

import sys
import os.path
from numpy.core.overrides import verify_matching_signatures

from numpy.lib.shape_base import _make_along_axis_idx
sys.path.append(os.path.join(os.path.dirname(__file__)))
fName = "CellDataFileTestMJ1.txt"

# File Path for my desktop
# fName = "D:\Documents\MSXIV\MSXIV_2\Strategy\SoC_Algorithm_Round2\CellDataFileTestMJ1.txt"
# File Path for my laptop
# fName = r"C:\Users\micke\Documents\MSXIV\Strategy\SoC_Algorithm_Round2\CellDataFileTestMJ1.txt"

class SoC_OCV:
	def __init__(self):
		#includes 0.050 cell and 0.035 cable, from tests done on single cell
		#This is the Resistance present when the chg-discharge curve was done, not the pack resistance
		#Should be eplicitly tested on the setup. This is a rough estimate of what I expect it was, as we never measured it.
		IR = 0.085

		#read data from txt files generated during discharge test
		with open(fName) as f_in:
			#fill matrices with data from file (all are lists)
			self.voltage, self.current, self.soc = np.loadtxt(itertools.islice(f_in, 1, None, 2), delimiter = '\t', usecols = (1,3,9), unpack = True)
		
		#Estimate the ocv of the cell, only taking the internal resistance into account (assuming no voltage relaxation or recovery)
		self.v_ocv = self.voltage + IR * self.current

		self.soc = self.__selection_sort__([value for value in self.soc])
		self.v_ocv =  self.__selection_sort__([value for value in self.v_ocv])
		
		#generate model for SoC_OCV curve
		#for now, fitting a 5th degree polynomial, but should use splines with interpolation
		
		#self.voltage = self.voltage.reshape(-1,1)
		#poly_model = make_pipeline(PolynomialFeatures(5), linear_model.Ridge())
		#poly_model.fit(self.soc, self.v_ocv)
		
		#self.voltage_predict = poly_model.predict(self.soc)
	
	#similar to the map function in Arduino
	#def valmap(value, istart, istop, ostart, ostop):
	#	return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
	
	#SoC between 
	#def get_cell_ocv(self, soc, max = 100):
	#	loc = self.valmap(soc, 0, max, len(self.voltage_predict) - 1, 0)
	#	if loc > len(self.voltage_predict) - 1:
	#		loc = len(self.voltage_predict)-1
	#	if loc < 0:
	#		loc = 0
	#	return int(loc)
	#	return self.voltage_predict[int(loc)]
	
	def get_soc_and_v_ocv(self):
		return self.soc, self.v_ocv
	
	# 
	def check_in_graph(self, soc2):
		if (soc2 > self.soc[len(self.soc) - 1] or soc2 < self.soc[0]):
			return "Value is out of predicted range", "Value is out of predicted range"
		v_ocv1 = 0
		v_ocv2 = 0
		soc1 = 0
		soc3 = 0

		for index in range(len(self.soc)):
			if (self.soc[index] == soc2):
				return self.v_ocv[index]
			elif (self.soc[index] < soc2):
				soc1 = self.soc[index]
				v_ocv1 = self.v_ocv[index]
			elif ((self.soc[index] > soc2)):
				soc3 = self.soc[index]	
				v_ocv2 = self.v_ocv[index]
				break
		value = v_ocv2 - (((v_ocv2 - v_ocv1)*(soc3 - soc2)) / (soc3 - soc1))
		return value
	
	def __selection_sort__(self, lst):
		for i in range(len(lst) - 1):
			min = i
			for j in range(i + 1, len(lst)):
				if (lst[j] < lst[min]):
					min = j
			self.__swap__(lst, i, min)
		return lst

	def __swap__(self, a, i, min):
		temp = a[i]
		a[i] = a[min]
		a[min] = temp


class test_SoC_OCV:
	def __init__(self):
		self.SoCOCV = SoC_OCV()
	def test(self):
		print(self.SoCOCV.check_in_graph(100))
		print(self.SoCOCV.check_in_graph(75))
		print(self.SoCOCV.check_in_graph(25))
		print(self.SoCOCV.check_in_graph(0))
		
if __name__ == "__main__":
	#just print out to console and make sure that we get reasonable values
	testing_soc_ocv = test_SoC_OCV()
	testing_soc_ocv.test()

	ocd = SoC_OCV()
	x_soc, y_vocv = ocd.get_soc_and_v_ocv()
	#plt.plot(x_soc, y_vocv)
	#plt.show()