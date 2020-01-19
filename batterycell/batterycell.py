import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText

# No such file exists for 958
# No such file exists for 998


def main(filein, fileout):
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


if __name__ == '__main__':
    for x in range(1, 1380):
        try:
            filename = "%s-DcLinearSweepScenario.csv" % x
            main("/Volumes/LACIE DRIVE/Midnight Sun/Battery Cell Data/Results-Single-File/%s" % filename, filename[:-4])
        except:
            print("No such file exists for %s" % x)
