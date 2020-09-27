import requests
import json
import pandas as pd
import sys
import os.path
sys.path.append(os.path.dirname(__file__))
from config import API_KEY
BASE_URL = 'https://dev.virtualearth.net/REST/v1/'
ELEVATIONS_FILE = os.path.join(sys.path[0], '../../optimization/elevations.csv')

class ElevationDataRetrieval:
    def __init__(self, wps: list, vwps: list, ht='sealevel'):
        """
        Initialize MapData
        @param wps: dictionary of major waypoints inputted by user
        @param vwps: dictionary of minor waypoints inputted by user
        @param ht: elevations response height model option
        """
        self.waypts = wps
        self.viawaypts = vwps
        self.heights = ht
        
    def get_elevation_data(self):
        """
        Getting elevation data response from Bing Maps API.
        @return: Requests.response object from API call
        """
        # append specified elevation URL details
        url = BASE_URL + 'Elevation/List?'

        # points will capture all the waypoints and viawaypoints
        # in a string as the elevation API requires
        points = ''

        # build points string as a param
        for index, waypoint in enumerate(self.waypts):
            for key in waypoint.keys():
                points += '{},{},'.format(key, waypoint[key])
            try:
                for viawaypoints in self.viawaypts[index]:
                    for key in viawaypoints.keys():
                        points += '{},{},'.format(key, \
                               viawaypoints[key])
            # same as IndexError exception raised in Route data getter
            except IndexError:
                pass

        # add parameters to URL
        url += 'points={}&heights={}&key={}'.format(points[:-1], \
                       self.heights, API_KEY)
        
        # request URL and return response
        response = requests.get(url)
        return response
    
    def parse_elevation_data(self, response):
        """
        Parsing through Elevations API call response.
        @param response: Requests.response object from API call
        @return: boolean
        """
        # convert response into dict
        elevations = json.loads(response)
        # parse down to relevant information
        try:
            elevations = elevations['resourceSets'][0]['resources'][0]['elevations']
        except KeyError:
            return False

        # create DataFrame with headers
        headers = ['Latitude', 'Longitude', 'Elevation']
        elevation_df = pd.DataFrame(columns=headers)

        # loop through waypoints and viawaypoints
        # to write coordinates into DataFrame
        counter = 0
        for index, waypoint in enumerate(self.waypts):
            for key in waypoint.keys():
                elevation_df = elevation_df.append({'Latitude': key,
                                                    'Longitude': waypoint[key],
                                                    'Elevation': elevations[counter]},
                                                     ignore_index = True)
                counter += 1
            try:
                for viawaypoints in self.viawaypts[index]:
                    for key in viawaypoints.keys():
                        elevation_df = elevation_df.append({'Latitude': key,
                                                            'Longitude': viawaypoints[key],
                                                            'Elevation': elevations[counter]}, ignore_index = True)
                    counter += 1
            except IndexError:
                pass


        # write dataframe into csv and return true
        elevation_df.to_csv(ELEVATIONS_FILE)
        print(f'Elevations written to CSV file.')
        return True
