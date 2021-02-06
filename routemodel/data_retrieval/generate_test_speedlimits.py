import pandas as pd
import sys
import os.path
import csv
import speedlimits as spdlts

sys.path.append(os.path.dirname(__file__))
ASC2021_file = "../routes/ASC2021/ASC2021_draft.csv"


def generate_speedlimits(points: list):
    pts = spdlts.build_speedlimits_points(points)
    query = spdlts.format_speedlimits_query(pts)
    spdlts_data = [pts, query]

    return spdlts_data


def read_csv():
    points = []
    with open(ASC2021_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            points.append({row[0]: row[1]})

    return points


def write_to_csv(output_file, data: list):
    with open(output_file, mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(data)


def main():

    points = read_csv()
    data = generate_speedlimits(points)

    # Read ASC2021 CSV File
    # Take it as input into generate_speedlimits(points:list)
    # Need API token to make a get request to get speedlimits
    # Take the manipulated spdlts_data and write to a new csv file
    #   This CSV file would have the outputs that we want to analyze


if __name__ == "__main__":
    main()
