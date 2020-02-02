import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import os
def weighting (current, valid_current):
   low = min(valid_current)
   high = max(valid_current)
   if current >= 0:
      weight = 1 - current / high #Weights added based on closeness to 0A
   elif current <0:
      weight = 1 - current / low
   return weight

def graphing (filename):
   ax = plt.axes()
   plt.title(filename + " OCV Visualization")

   plt.xlim(min(current),max(current))
   plt.xlabel("Current(A)(X e10)")
   plt.xticks(np.arange(min(current),max(current), 0.25))##spacing
   ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.4f')) ##digits after decimal

   plt.ylim(min(voltage),max(voltage))
   plt.ylabel("Voltage(V)")
   plt.yticks(np.arange(min(voltage),max(voltage), 0.00005))
   ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.6f'))

   plt.scatter(current,voltage)
   plt.savefig((filename) + '.png', bbox_inches='tight') ##Creating a new file each
   plt.clf()
   
def calculation():
   stdV = np.std(voltage)
   avgV = np.mean(voltage)
   print("Average Voltages for all samples: %s" % avgV)
   valid_voltage = []
   valid_current = []
   Weights = []
   i = 0
   for v in voltage:
       if v < avgV + 3 * stdV and v > avgV - 3 * stdV:
           valid_voltage.append(voltage[i]) ##Filtering outlier Voltages out
           valid_current.append(current[i])
       i = i + 1


   for x in valid_current:
       Weights.append(weighting(x,valid_current)) #Adds a weighting based on current
       
   weightedsumV = 0
   for i in range(0, len(valid_voltage)):
      weightedsumV = weightedsumV + valid_voltage[i] * Weights[i]
      
   weightavgV = [weightedsumV / sum(Weights)] 
   return weightavgV
   print("Weighted Average for Filtered Voltages: %s"  % weightavgV)
   


outputs = []
for filename in os.listdir():
    if filename.endswith("OCVData.csv"):
      df = pd.read_csv(filename) #Reading the CSV File, 1000 entries

      voltage= (df['voltage']) #Storing each column into a DataFrame
      current= (df['current']).multiply(10000000000) #Multiplied by 10billion or e10
      
      outputs.append(calculation())
      graphing(filename)
      
df = pd.DataFrame(outputs)
df.to_csv("OutPuts.csv")
