# script to generate test data
import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import pandas as pd
import data_retrieval.elevations as elevs
import csv

data_file = os.path.join(os.path.dirname(__file__), '..', 'routes', 'ASC2018.csv')
output_file  = os.path.join(os.path.dirname(__file__), 'test_elevation_output.csv')

def test_elevations_points_builder_and_query(points: list):
    points_encoded = elevs.build_elevations_points(points)
    query = elevs.format_elevations_query(points_encoded)
    query_polyline = elevs.format_elevations_query(points_encoded, 'polyline', 10)
    query_ellipsoid = elevs.format_elevations_query(points_encoded, heights='ellipsoid')
    elevations_data = [points_encoded, query, query_polyline, query_ellipsoid]
    write_csv_file(elevations_data)

def write_csv_file(elevations_data: list):
    with open(output_file, mode='a', newline='') as write_file:
        file_writer = csv.writer(write_file, delimiter=",")
        file_writer.writerow(elevations_data)

def reset_csv_file():
    with open('test_elevation_output.csv', mode='w', newline='') as clear_file:
        clear_file.truncate()
        file_writer = csv.writer(clear_file, delimiter=",")
        file_writer.writerow(['points_encoded', 'query', 'query_polyline', 'query_ellipsoid'])

with open(data_file, "r") as file:
    reader = csv.reader(file)
    points = []
    count = 0
    reset_csv_file()
    for row in reader:
        if (row[1] == 'lon'):
            continue
        points.append({row[1]:row[2]})
        count += 1
        if (count%10 == 0):
            test_elevations_points_builder_and_query(points)
            points.clear()
        if count == 100:
            break
