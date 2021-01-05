import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import pandas as pd
import data_retrieval.routes as rts

def test_routes_points_builder_wps_vwps_correct():
    waypoints = [{"45": "-74"}, {"46": "-75"}]
    viawaypoints = [{"45.5": "-74.5"}]
    points = rts.routes_points_builder(waypoints, viawaypoints)
    check = "wp.0=45,-74&vwp.1=45.5,-74.5&wp.2=46,-75&"
    assert(points == check)
    
def test_routes_points_builder_wps_correct_too_many_vwps():
    waypoints = [{"45": "-74"}, {"46": "-75"}]
    viawaypoints = [{"45.5": "-74.5"}, {"45.6": "-74.6"}]
    
    # should automatically disregard the extra viawaypoints dictionary
    points = rts.routes_points_builder(waypoints, viawaypoints)
    check = "wp.0=45,-74&vwp.1=45.5,-74.5&wp.2=46,-75&"
    assert(points == check)
    
def test_routes_points_builder_wps_no_vwps():
    waypoints = [{"45": "-74"}, {"46": "-75"}]
    viawaypoints = [{}]
    points = rts.routes_points_builder(waypoints, viawaypoints)
    check = "wp.0=45,-74&wp.1=46,-75&"
    assert(points == check)
        
def test_routes_points_builder_no_inputs():
    waypoints = [{}]
    viawaypoints = [{}]
    points = rts.routes_points_builder(waypoints, viawaypoints)
    check = ""
    assert(points == check)
    
def test_format_routes_query_valid_points_default_inputs():
    waypoints = [{"45": "-74"}, {"46": "-75"}]
    viawaypoints = [{"45.5": "-74.5"}]
    points = rts.routes_points_builder(waypoints, viawaypoints)
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
    points = rts.routes_points_builder(waypoints, viawaypoints)
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
    assert(isinstance(data, pd.DataFrame))
    # checking if columns as expected
    assert({'Latitude', 'Longitude', 'Maneuver Instruction', 
            'Distance to Maneuver', 'Direction', 'Street'}.issubset(data.columns))
    # code below checks if any non-null value is Main Street
    # should be true!
    assert(data.isin(['Main Street']).any().any())    
