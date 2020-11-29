import matplotlib.pyplot as plt
import numpy as np
import itertools
from sklearn import datasets, linear_model, metrics
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# fName = "D:\Documents\MSXIV\MSXIV\Strategy\CellDataFileTestMJ1.txt"
# fName = r"C:\Users\micke\Documents\MSXIV\Strategy\CellDataFileTestMJ1.txt"

import sys
import os.path
sys.path.append(os.path.dirname(__file__))
fName = 'CellDataFileTestMJ1.txt'

class BatTestPlot:
	def __init__(self):
		#includes 0.050 cell and 0.035 cable, from tests done on single cell
		self.IR = 0.085
		
	def plot_SoCOCV(self):
		print ("plotting SoC OCV")
		
		x = np.arange(0,10,0.2)
		y = np.sin(x)
		
		socfig, ax = plt.subplots()
		ax.plot(x,y)
		plt.title('MJ1 SoC OCV @3.5A')
		plt.show()
		
	def read_data(self, filename):
		#voltage, capacity = np.loadtxt(filename, delimiter = '\t', skiprows = 1, usecols = (1,7), unpack = True)
		with open(filename) as f_in:
			voltage, current, soc = np.loadtxt(itertools.islice(f_in, 1, None, 2), delimiter = '\t', usecols = (1,3,9), unpack = True)

		v_ocv = voltage + self.IR * current
		
		fig, ax = plt.subplots()
		
		ax.plot(soc, voltage, 'bo',label = 'v')
		ax.plot(soc, v_ocv, 'm-', label = 'ocv')
		
		soc = soc.reshape(-1,1)
		voltage = voltage.reshape(-1,1)
		
		#model = linear_model.LinearRegression()
		#model.fit(soc, voltage)
		
		#voltage_test = model.predict(soc)
		
		#ax.plot(soc, voltage_test, 'r-')
		
		#print('Coefficients: \n', model.coef_)
		#print('Variance Score: %.2f' % metrics.r2_score(voltage, voltage_test))
		
		poly_model = make_pipeline(PolynomialFeatures(5), linear_model.Ridge())
		poly_model.fit(soc, v_ocv)
		
		print("coefficients:")
		print(poly_model[1].coef_)
		print("Intercept:")
		print(poly_model[1].intercept_)
		
		poly_voltage_plot = poly_model.predict(soc)
		ax.plot(soc, poly_voltage_plot, 'g-', label = 'v_prediction', linewidth = 6)
		
		plt.title('Soc vs Voltage LG MJ1 @3A DSC')
		plt.legend(loc = 'lower right')
		plt.grid(True)
		plt.show()
		
	
print ("Started")

test = BatTestPlot()
test.read_data(fName)
#test.plot_SoCOCV()
