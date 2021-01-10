import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import pandas as pd
import json
import data_retrieval.speedlimits as spdlts

def test_speedlimits_points_builder_correct_inputs():
    list_of_points = [{"45": "-74"}, {"45.5": "-74.5"}, {"46": "-75"}]
    points = spdlts.build_speedlimits_points(list_of_points)
    check = "45,-74;45.5,-74.5;46,-75"
    assert(points == check)
        
def test_speedlimits_points_builder_no_inputs():
    list_of_points  = []
    points = spdlts.build_speedlimits_points(list_of_points)
    check = ""
    assert(points == check)
    
def test_format_speedlimits_query_valid_points_default_inputs():
    list_of_points = [{"45": "-74"}, {"45.5": "-74.5"}, {"46": "-75"}]
    points = spdlts.build_speedlimits_points(list_of_points)
    query = spdlts.format_speedlimits_query(points)
    check = "Routes/SnapToRoad?includeSpeedLimit=true&travelMode=driving&" + \
            "points={}&speedUnit={}".format(points, 'KPH')
    assert(query == check)
    
def test_format_speedlimits_query_invalid_points_default_inputs():
    points = [{"45": "-74"}, {"46": "-75"}]
    try:
        # should throw TypeError exception, test should pass if so
        query = spdlts.format_speedlimits_query(points)
    except Exception as err:
        assert(str(err) == 'can only concatenate str (not "dict") to str')
    
def test_format_speedlimits_query_valid_points_other_valid_inputs():
    list_of_points = [{"45": "-74"}, {"45.5": "-74.5"}, {"46": "-75"}]
    points = spdlts.build_speedlimits_points(list_of_points)
    query = spdlts.format_speedlimits_query(points, 
                                            "MPH")
    check = "Routes/SnapToRoad?includeSpeedLimit=true&travelMode=driving&" + \
            "points=45,-74;45.5,-74.5;46,-75&speedUnit={}".format('MPH')
    assert(query == check)
    
def test_parse_speedlimits_data_successful_response():
    response = {'authenticationResultCode': 'ValidCredentials',
                'resourceSets': [{'estimatedTotal': 1,
                                  'resources': [{'dataSourcesUsed': [5],
                                                  'snappedPoints':
                                                      [{"coordinate":{"latitude":43.774081204932955,"longitude":-79.5280152954904},"index":0,"name":"Steeles Ave W","speedLimit":50,"speedUnit":"KPH"},
                                                       {"coordinate":{"latitude":43.7638126,"longitude":-79.5771365},"index":1,"name":"Steeles Ave W","speedLimit":50,"speedUnit":"KPH"},
                                                       {"coordinate":{"latitude":43.757265798601146,"longitude":-79.606061880088319},"index":2,"name":"Steeles Ave W","speedLimit":60,"speedUnit":"KPH"},
                                                       {"coordinate":{"latitude":43.760031320790119,"longitude":-79.616949307985863},"index":3,"name":"ON-27 / Regional Rd-27 / Highway 27","speedLimit":70,"speedUnit":"KPH"}]}]}],
                'statusCode': 200,
                'statusDescription': 'OK',
                'traceId': 'af4be57884264def9cb3a8a4408699d7|BN000021D9|0.0.0.0|BN0000185A,BN00003128'}
    data = spdlts.parse_speedlimits_data(response)
    data_check = {'Latitude':[43.774081204932955, 43.7638126, 43.757265798601146, 43.760031320790119],
                  'Longitude':[-79.5280152954904, -79.5771365, -79.606061880088319, -79.616949307985863],
                  'Street':["Steeles Ave W", "Steeles Ave W", "Steeles Ave W", "ON-27 / Regional Rd-27 / Highway 27"],
                  'Speed Limit':[50, 50, 60, 70],
                  'Speed Unit':['KPH','KPH','KPH','KPH']}
    check = pd.DataFrame(data_check, columns = list(data_check.keys()))
    pd.util.testing.assert_frame_equal(data, check, check_dtype=False)