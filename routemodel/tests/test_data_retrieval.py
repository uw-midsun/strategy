import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))
import json
from data_retrieval.get_navigation import NavigationDataRetrieval
from data_retrieval.get_elevations import ElevationDataRetrieval

class MockResponse:
    def __init__(self):
        self.json_data = json.dumps({})
        self.status_code = 400
    
    
    def good_navi_response(self):
        self.json_data = json.dumps({'resourceSets': [{'resources': \
                        [{'routeLegs': [{'itineraryItems': \
                        [{'travelDistance': 2, 'compassDirection': 'N',\
                        'maneuverPoint': {'coordinates': [5, 10]}, \
                        'details': [{'names':['Main Street']}],
                        'instruction': {'text': 'Keep swimming'}}]}]}]}]}, \
                         sort_keys = True)
        self.status_code = 200
        return True
    
    def good_elev_response(self):
        self.json_data = json.dumps({'resourceSets': [{'resources': \
                         [{'elevations':[1, 2]}]}]}, sort_keys = True)
        self.status_code = 200
        return True
        

def test_navigation_parse_bad_response():
    navi_data = NavigationDataRetrieval([], [])
    response = MockResponse()
    assert(navi_data.parse_navigation_data(response.json_data) == False)
    assert(response.status_code == 400)

def test_navigation_parse_good_response():
    navi_data = NavigationDataRetrieval([], [])
    response = MockResponse()
    response.good_navi_response()
    parsed = navi_data.parse_navigation_data(response.json_data)
    assert(parsed == True)
    assert(response.status_code == 200)
    filepath = '../optimization/navigation.csv'
    assert(os.path.isfile(filepath) == True)
    os.remove(filepath)
    
def test_navigation_getter_good_inputs():
    waypoints = [{"45": "-74"}, {"46": "-75"}]
    viawaypoints = [[{"45.5": "-74.5"}]]
    navi = NavigationDataRetrieval(waypoints, viawaypoints)
    response = navi.get_navigation_data()
    assert(response.status_code == 200)

def test_navigation_getter_bad_inputs():
    waypoints = [{}, {}]
    viawaypoints = [[{}]]
    navi = NavigationDataRetrieval(waypoints, viawaypoints)
    response = navi.get_navigation_data()
    assert(response.status_code == 400)  
    
def test_elevation_parse_bad_response():
    elev_data = ElevationDataRetrieval([], [])
    response = MockResponse()
    assert(elev_data.parse_elevation_data(response.json_data) == False)
    
def test_elevation_parse_good_response():
    elev_data = ElevationDataRetrieval([], [])
    response = MockResponse()
    response.good_elev_response()
    parsed = elev_data.parse_elevation_data(response.json_data)
    assert(parsed == True)
    assert(response.status_code == 200)
    filepath = '../optimization/elevations.csv'
    assert(os.path.isfile(filepath) == True)
    os.remove(filepath)

def test_elevation_getter_good_inputs():
    waypoints = [{"45": "-74"}, {"46": "-75"}]
    viawaypoints = [[{"45.5": "-74.5"}]]
    elev = ElevationDataRetrieval(waypoints, viawaypoints)
    response = elev.get_elevation_data()
    assert(response.status_code == 200)

def test_elevation_getter_bad_inputs():
    waypoints = [{}, {}]
    viawaypoints = [[{}]]
    elev = ElevationDataRetrieval(waypoints, viawaypoints)
    response = elev.get_elevation_data()
    assert(response.status_code == 500) 