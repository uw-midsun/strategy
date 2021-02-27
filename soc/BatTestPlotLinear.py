import sys
import os.path
from matplotlib import pyplot as plt
import numpy as np
import itertools
from SoC_OCV import SoC_OCV
sys.path.append(os.path.dirname(__file__))
fName = 'CellDataFileTestMJ1.txt'

class BatTestPlotLinear:
    
    def __init__(self):
        # Includes 0.050 cell and 0.035 cable, from tests done on single cell
        self.IR = 0.085
        self.four_parallel_IR = ((self.IR - 0.035) / 4) + 0.035
    
    def plot_SOC_OCV(self):
        print ("plotting SoC OCV")
        soc_ocv = SoC_OCV()
        soc_ocv.plot_graph()

    def read_data(self, filename):
		#voltage, capacity = np.loadtxt(filename, delimiter = '\t', skiprows = 1, usecols = (1,7), unpack = True)
        with open(filename) as f_in:
            voltage, current, soc = np.loadtxt(itertools.islice(f_in, 1, None, 2), delimiter = '\t', usecols = (1,3,9), unpack = True)
        
        v_ocv = voltage + self.IR * current
        fig, ax = plt.subplots()
        ax.plot(soc, voltage, label = 'v')
        ax.plot(soc, v_ocv, 'm-', label = 'ocv')
        plt.title('Soc vs Voltage LG MJ1 @3A DSC')
        plt.legend(loc = 'lower right')
        plt.grid(True)
        plt.show()	
		
	
print ("Started")

test = BatTestPlotLinear()
test.read_data(fName)
