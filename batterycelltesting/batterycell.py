import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import argparse

# Pass Folder Location as a Command Line Argument
parser = argparse.ArgumentParser()
parser.add_argument("fileLocation", help="folder location of the cell data files", required=True)
args = parser.parse_args()
file_location = args.fileLocation


def generate_graphs():
    """Generate Graphs for all the Battery Cell Internal Resistance Data

    Iterate through each cell data file,
    Extract needed data from the file,
    Calculate a statistical linear regression through the data,
    Create and save the Plot of the data, including the linear regression and slope

    :return: True
    """
    for x in range(1, 2):
        try:
            # FileIO Parameters
            filename = "%s-DcLinearSweepScenario.csv" % x
            filein = file_location + "/" + filename
            fileout = filename[:-4]

            # Open DC Linear Sweep Scenario File
            df = pd.read_csv(filein)

            # Extract Data
            voltage = df["voltage"]
            current = df["current"]

            # Feature Engineering
            stats = linregress(current, voltage)

            # Plot
            f, ax = plt.subplots(1, 1)
            ax.grid(color="blue")
            plt.title("Voltage & Current Data from Cell %s" % fileout.split("-")[0])
            plt.xlabel("Current (A)")
            plt.ylabel("Voltage (V)")

            # Plot Raw Data
            ax.scatter(current, voltage, color="blue")

            # Plot Linear Regression Line
            ax.plot(current, current * stats.slope + stats.intercept, color="red")

            # Add Anchored Text
            at = AnchoredText("DC - IR = %f Ohm" % stats.slope, prop=dict(size=10), frameon=True, loc='upper left')
            at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
            ax.add_artist(at)

            # Save and Close Plot
            plt.savefig("./graphs/%s.png" % fileout)
            plt.close(f)
        except Exception as e:
            print(e)
    return True


def generate_csv():
    """Generate a CSV for all the Battery Internal Resistance Measurements

    Iterate through each file,
    Extract the Data from the file,
    Calculate a statistical linear regression of the data,
    Keep the slope of the linear regression,
    Output a CSV of the cell number and slope (Internal Resistance)

    :return: True
    """
    output = pd.DataFrame(columns=['Cell Number', 'Internal Resistance'])
    for i in range(1, 1380):
        try:
            # FileIO Parameter
            filename = "%s-DcLinearSweepScenario.csv" % i

            # Open DC Linear Sweep Scenario File
            df = pd.read_csv(file_location + "/" + filename)

            # Extract Data
            voltage = df["voltage"]
            current = df["current"]

            # Feature Engineering
            stats = linregress(current, voltage)
            output = output.append({'Cell Number': i, 'Internal Resistance': stats.slope}, ignore_index=True)
        except Exception as e:
            print(e)
    output.to_csv("cell_test_results.csv", index=False)
    return True


if __name__ == '__main__':
    generate_csv()
    generate_graphs()
    print("Done!")
