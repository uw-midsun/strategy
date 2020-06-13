import requests
import json
import pandas as pd
import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

BASE_URL = 'https://dev.virtualearth.net/REST/v1/'
API_KEY = 'An7vG9z_4w8X-6EM5WtJpP7dnIxDrZ97wLR5Ue0UAqq_aI4ZPJZPTrzNiEJj5buS'
NAVIGATION_FILE = os.path.join(sys.path[0], '..', '..', 'optimization', 'navigation.csv')

class NavigationDataRetrieval:
    def __init__(self, wps: list, vwps: list, route_attrs='routePath', dist_unit='km'):
        """
        Initialize NavigationDataRetrieval
        @param wps: dictionary of major waypoints inputted by user
        @param vwps: dictionary of minor waypoints inputted by user
        @param route_attrs: routes response data option
        @param dist_unit: routes response distance unit option
        """
        self.waypts = wps
        self.viawaypts = vwps
        self.route_attribute = route_attrs
        self.distance_unit = dist_unit

    def get_navigation_data(self):
        """
        Getting navigation data response from Bing Maps API.
        @return: Requests.response object from API call
        """
        # adjust url for Route API request
        url = BASE_URL + 'Routes?'
        query_params = ''

        # loop through waypoints and viawaypoints
        # store into points string

        counter = 0
        for index, waypoint in enumerate(self.waypts):
            for key in waypoint.keys():
                query_params += 'wp.{}={},{}&'.format(counter, key, waypoint[key])
                counter += 1
            try:
                for viawaypoints in self.viawaypts[index]:
                    for key in viawaypoints.keys():
                        query_params += 'vwp.{}={},{}&'.format(counter, key, viawaypoints[key])
                        counter += 1
            # IndexError exception raised (and ignored) as viawaypoints list should 
            # have a length of one less than the waypoints list
            # there may be a more elegant way to do this
            except IndexError:
                pass

        # add coordinates, route attribute option, distance unit, and API key
        # to url to be requested
        url += '{}routeAttributes={}&distanceUnit={}&key={}'.format(query_params, \
               self.route_attribute, self.distance_unit, API_KEY)
        
        # get and return response
        response = requests.get(url)
        return response

    def parse_navigation_data(self, response):
        """
        Parsing through Routes API call response.
        @param response: Requests.response object from API call
        @return: boolean
        """
        # convert response into dict
        route = json.loads(response)

        # headers are for csv, create DataFrame to write data into
        headers = ['Latitude', 'Longitude', 'Maneuver Instruction', 'Distance to Maneuver', 'Direction', 'Street']
        route_df = pd.DataFrame(columns=headers)

        # parse through each route leg returned in response
        try:
            for route_leg in route['resourceSets'][0]['resources'][0]['routeLegs']:
                # parse through the items in each route leg
                for item in route_leg['itineraryItems']:
                        # relevant info parsed below
                        lat = item['maneuverPoint']['coordinates'][0]
                        longit = item['maneuverPoint']['coordinates'][1]
                        instruction = item['instruction']['text']
                        dist = item['travelDistance']
                        direction = item['compassDirection']
    
                        # ensure street name is found
                        try:
                            if len(item['details']) > 1:
                                street = item['details'][1]['names'][0]
                            else:
                                street = item['details'][0]['names'][0]
                        except KeyError as err:
                            print(f'KeyError occurred on', err)
                            print(f'If error is \'names\' then error is expected.')
                            print(f'Sometimes a maneuver does not have a street name (e.g. highway ramps).')
                            street = ''
                            pass
                        
                        # append data into dataframe
                        route_df = route_df.append({'Latitude': lat, 'Longitude': longit, 
                                                    'Maneuver Instruction': instruction, 'Distance to Maneuver': dist, 
                                                    'Direction': direction, 'Street': street}, ignore_index = True)
        except Exception as error:
            print(f'Error occurred:', error)
            print(f'Please try again')
            return False
    
        # write dataframe to csv
        route_df.to_csv(NAVIGATION_FILE)
        print(f'Routes data written to CSV file.')
        return True
