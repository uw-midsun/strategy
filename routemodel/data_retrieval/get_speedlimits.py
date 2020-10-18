import requests
import json
import pandas as pd
import sys
import os.path
sys.path.append(os.path.dirname(__file__))
from config import API_KEY
BASE_URL = "https://dev.virtualearth.net/REST/v1/Routes/"

class SpeedLimitDataRetrieval: 
    def __init__(self, pts: list, sp_unit="KPH"):
        """
        Initialize SpeedLimitDataRetrieval
        @param pts: list containing latitude and longitude pairs of points along route
        @param sp_unit: speed unit response data option. Only other option is MPH afaik
        """
        
        self.points = pts
        self.speed_unit = sp_unit  
    
    def get_speedlimit_data(self):
        """
        Getting speed limit response from Bing Maps API.
        @return: Requests.response object from API call
        """
        # adjust url for speed limit API request
        url = BASE_URL + "SnapToRoad?"
        query_params = ""

        # loop through points
        # store into points string

        for index, point in enumerate(self.points):
            for key in point.keys():
                query_params += "{},{}".format(key, point[key])
                # prevents a semicolon from being appended to the last set of points
                # because that results in an error :P
                if index < len(self.points)-1: 
                    query_params += ";" 

        # add coordinates, route attribute option, distance unit, and API key
        # to url to be requested
        url += 'includeSpeedLimit=true&travelMode=driving&points={}&speedUnit={}&key={}'.format(query_params, \
            self.speed_unit, API_KEY)
        print(url)
        
        # get and return response
        response = requests.get(url)
        return response

    def parse_speedlimit_data(self, response): 
        """
        Parsing through Routes API call response.
        @param response: Requests.response object from API call
        @return: boolean
        """
        pass
