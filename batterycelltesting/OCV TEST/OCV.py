import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import os
import argparse
import zipfile 

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
   filename = filename[0:len(filename)-4]
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
   plt.savefig('OCVGraphs/'+ (filename) + '.png', bbox_inches='tight') ##Creating a new file each
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
       
   weighted_sum_voltage = 0
   for i in range(0, len(valid_voltage)):
      weighted_sum_voltage = weighted_sum_voltage + valid_voltage[i] * Weights[i]
      
   weight_avg_voltage = [weighted_sum_voltage / sum(Weights)] 
   return weight_avg_voltage
   print("Weighted Average for Filtered Voltages: %s"  % weight_avg_voltage)
   


parser = argparse.ArgumentParser(description='Makes weighted averages from OCV data')
parser.add_argument(
   '--file',
   '-f',
   default = 'empty', #Making two ways to run the script, with a file or zip.
   type=str,
   help='.csv file containing OCV Data. First column should be \'voltage\' and the second \'current\'')

parser.add_argument(
    '--zip',
    '-z',
    default = 'empty',
    help='.zip file with CSV files containing OCV Data. First column should be \'voltage\' and the second \'current\''
)
args = parser.parse_args()

# Checks to make sure only 1 arguement is used.
if args.file == 'empty' and args.zip == 'empty':
   parser.error("Please input at least one type of file.")
elif args.file != 'empty' and args.zip != 'empty':
   parser.error("Please input only one type of file.")
elif args.file != 'empty' and args.file[len(args.file)-4:len(args.file)] != ".csv":
   parser.error("Please input a .csv file")
elif args.zip != 'empty' and args.zip[len(args.zip)-4:len(args.zip)] != ".zip":
   parser.error("Please input a .zip file")
   
outputs = []


# Create target graphs folder if it doesn't already exist.
if not os.path.exists('OCVGraphs'):
    os.mkdir('OCVGraphs')
if not os.path.exists('OutputCSV'):
    os.mkdir('OutputCSV')
# Checks if the zip argument was not used. 
if args.zip == 'empty':
   df = pd.read_csv(args.file)

   
   voltage= (df['voltage']) 
   current= (df['current']).multiply(10000000000) 
      
   outputs.append(calculation())
   graphing(args.file)
   

# Otherwise, unzip the zip file into a new folder and iterate through them.
else:
   
    
   with zipfile.ZipFile(args.zip, 'r') as zip_ref:
    zip_ref.extractall('CSVFolder')
    
   for filename in os.listdir('CSVFolder'):
       if filename.endswith('.csv'):
         df = pd.read_csv('CSVFolder/' + filename) 

         voltage= (df['voltage']) 
         current= (df['current']).multiply(10000000000) 
         
         outputs.append(calculation())
         graphing(filename)
         

df = pd.DataFrame(outputs)
df.to_csv("OutputCSV/Outputs.csv")
