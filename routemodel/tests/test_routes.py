import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import pandas as pd
import data_retrieval.routes as rts
from datetime import datetime, timedelta

import pytest

def test_routes_points_builder_wps_vwps_correct():
    waypoints = [{"45": "-74"}, {"46": "-75"}]
    viawaypoints = [{"45.5": "-74.5"}]
    points = rts.build_routes_points(waypoints, viawaypoints)
    check = "wp.0=45,-74&vwp.1=45.5,-74.5&wp.2=46,-75&"
    assert(points == check)
    
def test_routes_points_builder_wps_correct_too_many_vwps():
    waypoints = [{"45": "-74"}, {"46": "-75"}]
    viawaypoints = [{"45.5": "-74.5"}, {"45.6": "-74.6"}]
    
    # should automatically disregard the extra viawaypoints dictionary
    points = rts.build_routes_points(waypoints, viawaypoints)
    check = "wp.0=45,-74&vwp.1=45.5,-74.5&wp.2=46,-75&"
    assert(points == check)
    
def test_routes_points_builder_wps_no_vwps():
    waypoints = [{"45": "-74"}, {"46": "-75"}]
    viawaypoints = [{}]
    points = rts.build_routes_points(waypoints, viawaypoints)
    check = "wp.0=45,-74&wp.1=46,-75&"
    assert(points == check)
        
def test_routes_points_builder_no_inputs():
    waypoints = [{}]
    viawaypoints = [{}]
    points = rts.build_routes_points(waypoints, viawaypoints)
    check = ""
    assert(points == check)
    
def test_format_routes_query_valid_points_default_inputs():
    waypoints = [{"45": "-74"}, {"46": "-75"}]
    viawaypoints = [{"45.5": "-74.5"}]
    points = rts.build_routes_points(waypoints, viawaypoints)
    query = rts.format_routes_query(points)
    check = "Routes?wp.0=45,-74&vwp.1=45.5,-74.5&wp.2=46,-75&"+\
        "routeAttributes={}&distanceUnit={}".format("routePath",
                                                     "km")
    assert(query == check)
    
def test_format_routes_query_invalid_points_default_inputs():
    points = [{"45": "-74"}, {"46": "-75"}]
    try:
        # should throw a TypeError exception, test should pass if so
        query = rts.format_routes_query(points)
    except TypeError as err:
        assert(str(err) == 'can only concatenate str (not "dict") to str')
    
def test_format_routes_query_valid_points_other_valid_inputs():
    waypoints = [{"45": "-74"}, {"46": "-75"}]
    viawaypoints = [{"45.5": "-74.5"}]
    points = rts.build_routes_points(waypoints, viawaypoints)
    query = rts.format_routes_query(points, 
                                    "routePath,regionTravelSummary",
                                    "mi")
    check = "Routes?wp.0=45,-74&vwp.1=45.5,-74.5&wp.2=46,-75&" +\
        "routeAttributes={}&distanceUnit={}".format("routePath,regionTravelSummary",
                                                    "mi")
    assert(query == check)
    
def test_parse_routing_data_successful_response():
    response = {'resourceSets': 
                               [{'resources': 
                                 [{'routeLegs': 
                                   [{'itineraryItems':
                                     [{'travelDistance': 2, 
                                       'compassDirection': 'N',
                                       'maneuverPoint': 
                                           {'coordinates': [5, 10]},
                                       'details': 
                                           [{'names':['Main Street']}],
                                       'instruction': 
                                           {'text': 'Keep swimming'}}]}]}]}]}
    data = rts.parse_routing_data(response)
    data_check = {'Latitude':[5],
                  'Longitude':[10], 
                  'Maneuver Instruction':['Keep swimming'],
                  'Distance to Maneuver':[2],
                  'Direction':['N'],
                  'Street':['Main Street']}
    check = pd.DataFrame(data_check, columns = list(data_check.keys()))
    pd.testing.assert_frame_equal(data, check, check_dtype=False)

def test_time_to_speeds_equivalent_length():
    sample_data = {'Latitude':[5, 6],
                  'Longitude':[10, 16], 
                  'Maneuver Instruction':['Keep swimming', 'why'],
                  'Distance to Maneuver':[2, 1.5],
                  'Direction':['N', 'S'],
                  'Street':['Main Street', 'yes']}
    sample_data_df = pd.DataFrame(sample_data, columns = list(sample_data.keys()))

    speeds = [2, 3]
    sample_data['Speed'] = speeds
    sample_data['Elapsed Time'] = [1, 0.5]
    start_time = datetime(2020, 12, 8, 1, 2, 3)
    sample_data['Start Timestamp'] = [start_time, start_time + timedelta(hours=1)]
    result_df = pd.DataFrame(sample_data, columns=list(sample_data.keys()))

    pd.testing.assert_frame_equal(
        rts.time_to(speeds, sample_data_df, start_time), 
        result_df
    )

def test_time_to_single_speed():
    sample_data = {'Latitude':[5, 6],
                  'Longitude':[10, 16], 
                  'Maneuver Instruction':['Keep swimming', 'why'],
                  'Distance to Maneuver':[2, 1.5],
                  'Direction':['N', 'S'],
                  'Street':['Main Street', 'yes']}
    sample_data_df = pd.DataFrame(sample_data, columns = list(sample_data.keys()))

    speeds = [2]
    sample_data['Speed'] = [2] * 2
    sample_data['Elapsed Time'] = [1, 0.75]
    start_time = datetime(2020, 12, 8, 1, 2, 3)
    sample_data['Start Timestamp'] = [start_time, start_time + timedelta(hours=1)]
    result_df = pd.DataFrame(sample_data, columns=list(sample_data.keys()))

    pd.testing.assert_frame_equal(
        rts.time_to(speeds, sample_data_df, start_time), 
        result_df
    )

def test_time_to_unexpected_length_speeds():
    sample_data = {'Latitude':[5, 6],
                  'Longitude':[10, 16], 
                  'Maneuver Instruction':['Keep swimming', 'why'],
                  'Distance to Maneuver':[2, 1.5],
                  'Direction':['N', 'S'],
                  'Street':['Main Street', 'yes']}
    sample_data_df = pd.DataFrame(sample_data, columns = list(sample_data.keys()))

    speeds = [2, 1, 1]
    start_time = datetime(2020, 12, 8, 1, 2, 3)

    with pytest.raises(ValueError):
        rts.time_to(speeds, sample_data_df, start_time)
