import matplotlib.pyplot as plt
import numpy as np
import itertools

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
		IR = 0.085 # For 4 parrelel ( (0.085 - 0.035) / 4) + 0.035

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
		# Create BatTestPlotLinear.py (for more accuracy)
		
	def get_soc_and_v_ocv(self):
		return self.soc, self.v_ocv

	# 
	def get_cell_ocv(self, soc2):
		if (soc2 > self.soc[-1] or soc2 < self.soc[0]):
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
		v_ocv3 = v_ocv2 - (((v_ocv2 - v_ocv1)*(soc3 - soc2)) / (soc3 - soc1))
		return v_ocv3

class test_SoC_OCV:

	def __init__(self, file_name):
		self.SoCOCV = SoC_OCV()
	
	def test(self):
		print(self.SoCOCV.get_cell_ocv(100))
		print(self.SoCOCV.get_cell_ocv(75))
		print(self.SoCOCV.get_cell_ocv(25))
		print(self.SoCOCV.get_cell_ocv(0))

if __name__ == "__main__":
	ocd = SoC_OCV()
	soc, vocv = ocd.get_soc_and_v_ocv()
	plt.plot(soc, vocv)
	plt.show()

