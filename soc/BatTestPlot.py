import matplotlib.pyplot as plt
import numpy as np
import itertools
from SoC_OCV import SoC_OCV 
from sklearn import datasets, linear_model, metrics
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# fName = "D:\Documents\MSXIV\MSXIV\Strategy\CellDataFileTestMJ1.txt"
# fName = r"C:\Users\micke\Documents\MSXIV\Strategy\CellDataFileTestMJ1.txt"

import sys
import os.path
sys.path.append(os.path.dirname(__file__))
fName = 'test_data//CellDataFileTestMJ1.txt'

class BatTestPlot:
	def __init__(self):
		"""Initialize BatTestPlot class to test plotting as a fit or as a linear approximation. Includes 0.050 cell and 0.035 cable, from tests done on single cell
		"""

		self.IR = 0.085
		self.four_parallel_IR = ((self.IR - 0.035) / 4) + 0.035
		self.voltage = []
		self.current = []
		self.soc = []
		self.v_ocv = []
		
	def read_data(self, filename):
		"""Read data from passed test file. Function reads cell test data (voltage, current, soc)

		Args:
			filename: name and relative path of file in file structure 
		"""

		with open(filename) as f_in:
			self.voltage, self.current, self.soc = np.loadtxt(itertools.islice(f_in, 1, None, 2), delimiter = '\t', usecols = (1,3,9), unpack = True)

		self.v_ocv = self.voltage + self.IR * self.current

	def plot_SocOCV_linear(self):
		"""Graph data based on linear approximations. Uses Soc_OCV class to graph data
		"""

		soc_ocv = SoC_OCV()
		soc_ocv.plot_graph()

	def plot_SoCOCV_fit(self):
		"""Graph data based on fit. Uses Scikit-learn to fit data to data points
		"""
		
		fig, ax = plt.subplots()
		
		ax.plot(self.soc, self.voltage, 'bo',label = 'v')
		ax.plot(self.soc, self.v_ocv, 'm-', label = 'ocv')
		
		self.soc = self.soc.reshape(-1,1)
		self.voltage = self.voltage.reshape(-1,1)
		
		#model = linear_model.LinearRegression()
		#model.fit(soc, voltage)
		
		#voltage_test = model.predict(soc)
		
		#ax.plot(soc, voltage_test, 'r-')
		
		#print('Coefficients: \n', model.coef_)
		#print('Variance Score: %.2f' % metrics.r2_score(voltage, voltage_test))
		
		poly_model = make_pipeline(PolynomialFeatures(5), linear_model.Ridge())
		poly_model.fit(self.soc, self.v_ocv)
		
		print("coefficients:")
		print(poly_model[1].coef_)
		print("Intercept:")
		print(poly_model[1].intercept_)
		
		poly_voltage_plot = poly_model.predict(self.soc)
		ax.plot(self.soc, poly_voltage_plot, 'g-', label = 'v_prediction', linewidth = 6)
		
		plt.title('Soc vs Voltage LG MJ1 @3A DSC Fit')
		plt.legend(loc = 'lower right')
		plt.grid(True)
		plt.show()
		

if __name__ == '__main__':	
	print ("Started")
	test = BatTestPlot()
	test.read_data(fName)
	test.plot_SocOCV_linear()
	test.plot_SoCOCV_fit()

