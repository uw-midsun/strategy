import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))
import json
from data_retrieval.get_speedlimits import SpeedlimitDataRetrieval

class MockResponse:
    def __init__(self):
        self.json_data = json.dumps({})
        self.status_code = 400
    
    def good_speedlimit_response(self):
        self.json_data = json.dumps({"resourceSets": [{"resources": \
            [{"snappedPoints": [{ "coordinate": {"latitude": 35.686956, "longitude": -105.938072},\
			"index": 0, "name": "E San Francisco St","speedLimit": 0,"speedUnit": "KPH"},\
            {"coordinate": {"latitude": 35.686081507331807,"longitude": -105.93831770140044},\
            "index": 1,"name": "E Water St","speedLimit": 0,"speedUnit": "KPH"}]}]}]}\
        )
        self.status_code = 200
        return True

def test_speedlimit_getter_good_inputs():
    points = [{"35.686916": "-105.938140"}, {"35.686272": "-105.938292"}, {"35.685824": "-105.938451"}]
    speedlimit = SpeedlimitDataRetrieval(points)
    response = speedlimit.get_speedlimit_data()
    assert(response.status_code == 200)

def test_speedlimit_getter_bad_inputs():
    speedlimit = SpeedlimitDataRetrieval([])
    response = speedlimit.get_speedlimit_data()
    assert(response.status_code == 400)