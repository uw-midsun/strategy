import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import argparse


def generate_csv():
    """ Clean Cell Weight Measurements and Output Results as CSV

    Iterate through each file
    Extract weight from file
    Drop negative weights
    Create 10 evenly spaced histogram bins for the data
    Drop the lowest bin (aka the near zero value)
    Select the weight data from the bin with the greatest occurrence
    Remove outliers from the weigh data (> or < 2 std from the mean)
    Calculate the mean and the standard deviation of the weight
    Output the

    :return: True
    """
    output = pd.DataFrame(columns=['Cell Number', 'Average Cell Weight (g)', 'Standard Deviation (g)'])
    for i in range(1, 1380):
        try:
            # FileIO Parameters
            filename = "%s-weight.csv" % i
            filein = file_location + "/" + filename

            # Open Weight File
            df = pd.read_csv(filein)

            # Extract data
            weight = df["weight(g)"]

            # Use data with weights > 0 grams
            weight = weight[weight > 0]

            # Statistically bin the data
            bin_means, bin_edges, bin_number = stats.binned_statistic(weight, weight, statistic='mean', range=(min(weight), max(weight)))

            # Drop lowest bin (close to zero value) then get most common bin occurrence as label
            counts = np.bincount(bin_number[bin_number > 1])
            bin_label = np.argmax(counts)

            # Set the weight where the bin number is equal to the most common bin
            weight = weight[bin_number == bin_label]

            # Remove outliers further than 2 standard deviations from the mean
            mean = np.mean(weight)
            std = np.std(weight)
            weight = weight[weight >= mean - (2*std)]
            weight = weight[weight <= mean + (2*std)]

            # Append data to data frame
            output = output.append({'Cell Number': i, 'Average Cell Weight (g)': np.mean(weight), 'Standard Deviation (g)': np.std(weight)}, ignore_index=True)
        except Exception as e:
            print(e)
    # Output complete results as csv
    output.to_csv("cell_weight_results.csv", index=False)
    return True


def generate_graph():
    """ Generate graph of the cell weight results

    :return: True
    """
    # Open CSV file
    df = pd.read_csv("./cell_weight_results.csv")

    # Extract information
    num = df["Cell Number"]
    avg = df["Average Cell Weight (g)"]
    std = df["Standard Deviation (g)"]

    # Plot
    f, ax = plt.subplots(1, 1)
    ax.grid(color="blue")
    plt.title("Average Cell Weight Measurements")
    plt.xlabel("Cell Number")
    plt.ylabel("Average Cell Weight (g)")

    # Plot Raw Data
    ax.scatter(num, avg, c=std, cmap="Spectral")

    # Save and Close Plot
    plt.savefig("./cell_weight_results.png")
    plt.close(f)
    return True


if __name__ == '__main__':
    # Parse Data Folder as command line argument
    parser = argparse.ArgumentParser()
    parser.add_argument("fileLocation", help="folder location of the cell data files")
    args = parser.parse_args()
    file_location = args.fileLocation

    generate_csv()
    generate_graph()
    print("Done!")
