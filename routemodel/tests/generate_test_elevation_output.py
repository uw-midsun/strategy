# script to generate test data
import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import pandas as pd
import data_retrieval.elevations as elevs
import csv
import data_retrieval.common as commons

data_file = os.path.join(os.path.dirname(__file__), '..', 'routes', 'ASC2021','ASC2021_elevations_draft.csv')
output_file  = os.path.join(os.path.dirname(__file__), 'test_elevation_output.csv')

def test_elevations_points_builder_and_query(points: list):
    points_encoded = elevs.build_elevations_points(points)
    #query = elevs.format_elevations_query(points_encoded)
    query_polyline = elevs.format_elevations_query(points_encoded, 'polyline', 50)
    #query_ellipsoid = elevs.format_elevations_query(points_encoded, heights='ellipsoid')
    
    response_polyline = commons.get_API_data(query_polyline)
    parsed_response_polyline = elevs.parse_elevations_data(response_polyline, points, method='polyline')
    print(parsed_response_polyline)
            
    elevations_data = [parsed_response_polyline]
    write_csv_file(elevations_data)

def write_csv_file(elevations_data: list):
    with open(output_file, mode='a', newline='') as write_file:
        file_writer = csv.writer(write_file, delimiter=",")
        file_writer.writerow(elevations_data)

def reset_csv_file():
    with open('test_elevation_output.csv', mode='w', newline='') as clear_file:
        clear_file.truncate()
        file_writer = csv.writer(clear_file, delimiter=",")

with open(data_file, "r") as file:
    reader = csv.reader(file)
    points = []
    count = 0
    reset_csv_file()
    for row in reader:
        if (count == 0):
            continue
        points.append({row[1]:row[2]})
        count += 1
    test_elevations_points_builder_and_query(points)
