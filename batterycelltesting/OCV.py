import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import os


def Weighting (Current,ValidCurrent):
   low = min(ValidCurrent)
   high = max(ValidCurrent)
   if Current >= 0:
      weight = 1 - Current/high #Weights added based on closeness to 0A
   elif Current <0:
      weight = 1 - Current/low
   return weight;

def Graphing (filename):
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
   plt.savefig('OCVDataGraph.png', bbox_inches='tight') ##Creating a new file each
   plt.clf()
   
def Calculation():
   stdV = np.std(voltage)
   avgV = np.mean(voltage)
   print("Average Voltages for all samples: %s" % avgV)
   ValidVoltage = []
   ValidCurrent = []
   Weights = []
   i = 0
   for v in voltage:
       if v < avgV+3*stdV and v > avgV-3*stdV:
           ValidVoltage.append(voltage[i]) ##Filtering outlier Voltages out
           ValidCurrent.append(current[i])
       i = i + 1


   for x in ValidCurrent:
       Weights.append(Weighting(x,ValidCurrent)) #Adds a weighting based on current
       
   weightedsumV = 0
   for i in range(0, len(ValidVoltage)):
      weightedsumV = weightedsumV + ValidVoltage[i]*Weights[i]
      
   weightavgV = [weightedsumV/sum(Weights)] #Divide by the sum of the weights,
   #not amount of elements, big issue I had.
   return weightavgV
   print("Weighted Average for Filtered Voltages: %s"  % weightavgV)
   
#print(Valids[0][0]) #First number is index, second is Voltage Or Current or Weight



outputs = []
for filename in os.listdir():
    if filenameendswith.("OCV.csv"):
      df = pd.read_csv(filename) #Reading the CSV File, 1000 entries

      voltage= (df['voltage']) #Storing each column into a DataFrame
      current= (df['current']).multiply(10000000000) #Multiplied by 10billion or e10
      
      outputs.append(Calculation())
      #Graphing(filename)
      
#df = pd.DataFrame(outputs)
#df.to_csv("OutPuts.csv")
