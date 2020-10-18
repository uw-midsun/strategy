from csv import reader, writer
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import argparse
import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

MESSY_DATA_FILE = os.path.join(sys.path[0], '..', '..', 'tests', 'data_smooth_testing', 'clean_RollDown.csv')
CLEAN_DATA_FILE = os.path.join(sys.path[0], '..', '..', 'tests', 'data_smooth_testing', 'cleanTestData.csv')

parser = argparse.ArgumentParser(description="Specify messy and clean file locations")
parser.add_argument("-m", "--messy", help="Enter messy data file path to read from", type=str)
parser.add_argument("-c", "--clean", help="Enter clean data file path to write to", type=str)
args = parser.parse_args()

if args.messy:
    MESSY_DATA_FILE = args.messy
if args.clean:
    CLEAN_DATA_FILE = args.clean

# TODO: need to somehow make sure it is odd number of data points
unfilteredVelocity = []
xValues = []
# stored but never used
deletedVelocityValues = []
deletedTimeValues = []

# max acceleration as determined by dynamics team - anything above this value must be a signal error as components cannot attain higher acceleration
MAX_ACCEL = 9.81

# read data into unfilitered array
with open(MESSY_DATA_FILE, "r") as messyData:
    csv_reader = reader(messyData, delimiter = ',')

    # skip first line (headers)
    next(csv_reader)

    for line in csv_reader:
        # line index values based on rollDown data from repository
        # making sure previous list value exists and that accel is less than max value
        # to filter for outliers

        # expect velocity in line[3] and time in line[0]

        if len(unfilteredVelocity) > 0 and abs(100 * (float(line[3]) - unfilteredVelocity[-1]) / 
            (float(line[0]) - xValues[-1])) > MAX_ACCEL:
            deletedVelocityValues.append(float(line[3]))  
            deletedTimeValues.append(float(line[0]))                  
        else:
            xValues.append(float(line[0]))
            unfilteredVelocity.append(float(line[3]))

# filter the array
filteredData = savgol_filter(unfilteredVelocity, 7, 4)

# write to CSV
with open(CLEAN_DATA_FILE, "w", newline='') as cleanData:
    csv_writer = writer(cleanData)

    csv_writer.writerow(['Time Offset [ms]', 'Velocity'])

    for index in range(len(xValues)):
        csv_writer.writerow([xValues[index], filteredData[index]])

unfiltered, = plt.plot(xValues, unfilteredVelocity, color = "r", label="Messy")
filtered, = plt.plot(xValues, filteredData, color = "g", label="Cleaned")
plt.title("Smoothed Velocity Profile")
plt.xlabel("Time Offset (ms)")
plt.ylabel("Velocity")
plt.legend(handles=[unfiltered, filtered])
plt.show()