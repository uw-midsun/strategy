# script to generate test data
import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import pandas as pd
import data_retrieval.elevations as elevs
import csv

data_file = os.path.join(os.path.dirname(__file__), '..', 'routes', 'ASC2018.csv')

def test_elevations_points_builder_and_query(points: list):
    points_encoded = elevs.build_elevations_points(points)
    query = elevs.format_elevations_query(points_encoded)
    query_polyline = elevs.format_elevations_query(points_encoded, 'polyline', 10)
    query_ellipsoid = elevs.format_elevations_query(points_encoded, heights='ellipsoid')

with open(data_file, "r") as file:
    reader = csv.reader(file)
    points = []
    count = 0
    for row in reader:
        if (row[1] == 'lon'):
            continue
        points.append({row[1]:row[2]})
        count += 1
        if (count==10):
            break
    print(points)
    test_elevations_points_builder_and_query(points)
    