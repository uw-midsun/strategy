import requests
import json
import pandas as pd
import sys
import os.path
sys.path.append(os.path.dirname(__file__))
from config import API_KEY
BASE_URL = "https://dev.virtualearth.net/REST/v1/Routes/"

# TEMPORARY FOR TESTING TWO HARD-CODED POINTS
query_params = "SnapToRoad?points=35.686916,-105.938140;35.686272,-105.938292&includeTruckSpeedLimit=true&IncludeSpeedLimit=true&speedUnit=MPH&travelMode=driving&key=AqeZ3SYMvzGA-9SGT-IEQ9eD9QkENVFwmiiZTL69S2vXCy4oc2sI-xxSupiL0UsP"
url = BASE_URL + query_params
response = requests.get(url)
print(response.json())

class SpeedlimitDataRetrieval: 
    def __init__(self, pt1_lat: float, pt1_long: float, pt2_lat: float, pt2_long: float, sp_unit="KPH"):
        """
        Initialize SpeedlimitDataRetrieval
        @param pt1_lat: latitude of first point (floating point)
        @param pt1_long: longitude of first point (floating point)
        @param pt2_lat: latitude of second point (floating point) 
        @param pt2_long: longitude of second point (floating point)
        @param sp_unit: speed unit response data option
        """

        # This can probably be updated to take a list containing multiple points
        # (later)
        # self.points = pts (where pts is a list)
        self.point1 = pt1_lat + "," + pt1_long
        self.point2 = pt2_lat + "," + pt2_lat
        self.include_speed_limit = include_sp_lim
        self.speed_unit = sp_unit  
    
    def get_speedlimit_data(self):
        """
        Getting speed limit response from Bing Maps API.
        @return: Requests.response object from API call
        """
        # adjust url for speed limit API request
        url = BASE_URL + "SnapToRoad?"

        # store into points string
        points = "{};{}".format(self.point1, self.point2)

        # add coordinates, route attribute option, distance unit, and API key
        # to url to be requested
        url += 'includeSpeedLimit=true&travelMode=driving&points={}&speedUnit={}&key={}'.format(points, \
            self.speed_unit, API_KEY)
        
        # get and return response
        response = requests.get(url)
        return response

    def parse_speedlimit_data(self, response): 
        """
        Parsing through Routes API call response.
        @param response: Requests.response object from API call
        @return: boolean
        """
        # WIP
        # convert response into dict
        route = json.loads(response)


