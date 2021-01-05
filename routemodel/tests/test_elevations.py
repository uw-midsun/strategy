import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import pandas as pd
import data_retrieval.elevations as elevs

def test_elevations_points_builder_valid_points():
    points = [{"45": "-74"}, {"46": "-75"}]
    points_encoded = elevs.elevations_points_builder(points)
    check = "g-hk1l5yhIggo_lwqC"
    assert(points_encoded == check)
    
def test_elevations_points_builder_empty_points():
    points = [{}]
    points_encoded = elevs.elevations_points_builder(points)
    check = ""
    assert(points_encoded == check)
    
def test_format_elevations_query_valid_points_default_inputs():
    points = [{"45": "-74"}, {"46": "-75"}]
    points_encoded = elevs.elevations_points_builder(points)
    query = elevs.format_elevations_query(points_encoded)
    check = "Elevation/List?points=g-hk1l5yhIggo_lwqC&heights=sealevel"
    assert(query == check)
    
def test_format_elevations_query_valid_points_polyline_inputs():
    points = [{"45": "-74"}, {"46": "-75"}]
    points_encoded = elevs.elevations_points_builder(points)
    query = elevs.format_elevations_query(points_encoded, 'polyline', 10)
    check = "Elevation/Polyline?points=g-hk1l5yhIggo_lwqC&heights=sealevel&samples=10"
    assert(query == check)

def test_format_elevations_query_valid_points_ellipsoid_heights():
    points = [{"45": "-74"}, {"46": "-75"}]
    points_encoded = elevs.elevations_points_builder(points)
    query = elevs.format_elevations_query(points_encoded, heights='ellipsoid')
    check = "Elevation/List?points=g-hk1l5yhIggo_lwqC&heights=ellipsoid"
    assert(query == check)
    
def test_parse_elevations_data_default_get_successful_response():
    points = [{"45": "-74"}, {"46": "-75"}]
    response = {"authenticationResultCode": "ValidCredentials",
                           'resourceSets': 
                               [{'estimatedTotal': 1,
                                 'resources': 
                                     [{'__type': 'ElevationData:http://schemas.microsoft.com/search/local/ws/rest/v1',
                                       'elevations': [184, 299],
                                       'zoomLevel': 14}]}],
                                   'statusCode': 200,
                                   'statusDescription': 'OK'}
    data = elevs.parse_elevations_data(response, points)
    assert(isinstance(data, pd.DataFrame))
    
    # Checking if columns as expected
    assert({'Latitude', 'Longitude', 'Elevation'}.issubset(data.columns))
    
    # code below checks if any non-null value is 184
    # should be true!
    assert(data.isin([184]).any().any())

def test_parse_elevations_data_polyline_get_successful_response():
    points = [{"45": "-74"}, {"46": "-75"}]
    response = {"authenticationResultCode": "ValidCredentials",
                           "resourceSets":
                               [{"estimatedTotal":1,
                                 "resources":
                                     [{"elevations":
                                       [186,49,61,324,299],
                                       "zoomLevel":9}]}],
                                 "statusCode":200,
                                 "statusDescription":"OK"}
    data = elevs.parse_elevations_data(response, points)
    assert(isinstance(data, pd.DataFrame))
    
    # Checking if columns are as expected
    assert({'Elevation'}.issubset(data.columns))
    
    # code below checks if any non-null value is 49
    # should be true!
    assert(data.isin([49]).any().any())