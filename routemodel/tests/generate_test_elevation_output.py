# script to generate test data
import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import pandas as pd
import data_retrieval.elevations as elevs
import csv
import data_retrieval.common as commons

data_file = os.path.join(os.path.dirname(__file__), '..', 'routes', 'ASC2021','ASC2021_elevations_draft.csv')
output_file  = os.path.join(os.path.dirname(__file__), '..', 'routes', 'ASC2021', 'test_elevation_output.csv')

def test_elevations_build_query(points: list):
    points_encoded = elevs.build_elevations_points(points)
    #query = elevs.format_elevations_query(points_encoded)
    query_polyline = elevs.format_elevations_query(points_encoded, 'polyline', 1000)
    #query_ellipsoid = elevs.format_elevations_query(points_encoded, heights='ellipsoid')
    
    response_polyline = commons.get_API_data(query_polyline)
    parsed_response_polyline = elevs.parse_elevations_data(response_polyline, points, method='polyline')
    return parsed_response_polyline

def read_csv_points(data):
    with open(data, "r") as file:
        reader = csv.reader(file)
        points = []
        count = 0
        for row in reader:
            if (count == 0):
                count += 1
                continue
            points.append({row[1]:row[2]})
            count += 1
    return points

if __name__ == "__main__":
    points = read_csv_points(data_file)
    apiResponse = test_elevations_build_query(points)
    apiResponse.to_csv(output_file)