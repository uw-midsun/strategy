import matplotlib.pyplot as plt
import numpy as np
import itertools
from sklearn import datasets, linear_model, metrics
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

#To fix - still energy left at 0% - 2.85V at end due to IR voltage drop
#This requires a more precise cell cycling profile generated with a SMU
#0% SoC is defined as when the cell drops below 2.5V under a 3A load.

import sys
import os.path
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
			#fill matrices with data from file
			voltage, current, soc = np.loadtxt(itertools.islice(f_in, 1, None, 2), delimiter = '\t', usecols = (1,3,9), unpack = True)
		
		#Estimate the ocv of the cell, only taking the internal resistance into account (assuming no voltage relaxation or recovery)
		v_ocv = voltage + IR * current
		
		#generate model for SoC_OCV curve
		#for now, fitting a 5th degree polynomial, but should use splines with interpolation
		soc = soc.reshape(-1,1)
		voltage = voltage.reshape(-1,1)
		poly_model = make_pipeline(PolynomialFeatures(5), linear_model.Ridge())
		poly_model.fit(soc, v_ocv)
		
		self.voltage_predict = poly_model.predict(soc)
	
	#similar to the map function in Arduino
	def valmap(self, value, istart, istop, ostart, ostop):
		return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
	
	#SoC between 
	def get_cell_ocv(self, soc, max = 100):
		loc = self.valmap(soc, 0, max, len(self.voltage_predict) - 1, 0)
		if loc > len(self.voltage_predict) - 1:
			loc = len(self.voltage_predict)-1
		if loc < 0:
			loc = 0
		#return int(loc)
		return self.voltage_predict[int(loc)]
		
class test_SoC_OCV:
	def __init__(self):
		self.SoCOCV = SoC_OCV()
	def test(self):
		print(self.SoCOCV.get_cell_ocv(100))
		print(self.SoCOCV.get_cell_ocv(75))
		print(self.SoCOCV.get_cell_ocv(25))
		print(self.SoCOCV.get_cell_ocv(0))
		
if __name__ == "__main__":
	#just print out to console and make sure that we get reasonable values
	testing_soc_ocv = test_SoC_OCV()
	testing_soc_ocv.test()
	