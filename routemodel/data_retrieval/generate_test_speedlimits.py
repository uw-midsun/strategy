import pandas as pd
import sys
import os.path
import csv
import speedlimits as spdlts
import common

sys.path.append(os.path.dirname(__file__))
input_file = os.path.join(os.path.dirname(__file__), '..', 'routes', 'ASC2021','ASC2021_draft.csv')
output_file  = os.path.join(os.path.dirname(__file__), '..', 'routes', 'ASC2021', 'generated_speedlimits.csv')


def generate_speedlimits(points: list):
    pts = spdlts.build_speedlimits_points(points)
    query = spdlts.format_speedlimits_query(pts)
    response = common.get_API_data(query)
    parsed_df = spdlts.parse_speedlimits_data(response)
    
    return parsed_df


def read_csv(file_path):
    points = []
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            points.append({row[0]: row[1]})

    return points


def main():
    points = read_csv(input_file)
    parsed_df = generate_speedlimits(points)
    parsed_df.to_csv(output_file)


if __name__ == "__main__":
    main()
