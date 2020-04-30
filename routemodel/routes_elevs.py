import requests
import pandas as pd

BASE_URL = 'https://dev.virtualearth.net/REST/v1/'
API_KEY = 'An7vG9z_4w8X-6EM5WtJpP7dnIxDrZ97wLR5Ue0UAqq_aI4ZPJZPTrzNiEJj5buS'
ROUTES_FILE = '../optimization/route.csv'
ELEVATIONS_FILE = '../optimization/elevation.csv'


class MapData:
    def __init__(self, wps: list, vwps: list, route_attrs='routePath', dist_unit='km', ht='sealevel'):
        """
        Initialize MapData
        @param wps: dictionary of major waypoints inputted by user
        @param vwps: dictionary of minor waypoints inputted by user
        @param route_attrs: routes response data option
        @param dist_unit: routes response distance unit option
        @param ht: elevations response height model option
        """
        self.waypts = wps
        self.viawaypts = vwps
        self.route_attribute = route_attrs
        self.distance_unit = dist_unit
        self.heights = ht

    def get_route_data(self):
        """
        Getting route data response from Bing Maps API.
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

    def parse_route_data(self, response):
        """
        Parsing through Routes API call response.
        @param response: Requests.response object from API call
        @return: boolean
        """
        # convert response into dict
        route = response.json()

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
        route_df.to_csv(ROUTES_FILE)
        print(f'Routes data written to CSV file.')
        return True

    def parse_elevation_data(self, response):
        """
        Parsing through Elevations API call response.
        @param response: Requests.response object from API call
        @return: boolean
        """
        # convert response into dict
        elevations = response.json()
        # parse down to relevant information
        elevations = elevations['resourceSets'][0]['resources'][0]['elevations']

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
                                                    'Elevation': elevations[counter]}, ignore_index = True)
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


if __name__ == "__main__":
    waypoints = []
    via_waypoints = []
    distance_unit = 'km'
    route_attribute = 'routePath'
    heights = 'sealevel'

    print(f"Enter up to 25 waypoints.")
    waypoints_limit = 25 # limit specified by Routes API
    # note that the Elevations API only has a limit of ~1000 of any type of point
    try:
        for i in range(waypoints_limit):
            coordinate = {}
            latitude = float(input("Type in the latitude: "))
            longitude = float(input("Type in the longitude: "))
            coordinate[str(latitude)] = str(longitude)
            waypoints.append(coordinate)
    except ValueError:
        print(f"Waypoints input stopped. Moving on.")
        pass
    print(waypoints)

    print(f"Enter up to 10 minor / via waypoints for each waypoint.")
    via_waypoints_limit = 10 # limit specified by Routes API
    # note that the Elevations API only has a limit of 1024
    # and does not classify points into waypoints/viawaypoints
    for i in waypoints[:-1]:
        inner_list = []
        try:
            for j in range(via_waypoints_limit):
                coordinate = {}
                latitude = float(input("Type in the latitude: "))
                longitude = float(input("Type in the longitude: "))
                coordinate[str(latitude)] = str(longitude)
                inner_list.append(coordinate)
            via_waypoints.append(inner_list)
        except ValueError:
            print(f"Viawaypoints input stopped. Next waypoint.")
            via_waypoints.append(inner_list)
            pass

    print(via_waypoints)
    map_object = MapData(waypoints, via_waypoints, route_attribute, distance_unit, heights)
    routes_response = map_object.get_route_data()

    if routes_response.status_code == 200:
        map_object.parse_route_data(routes_response)
    else:
        print('No usable route data was returned.')

    elevs_response = map_object.get_elevation_data()

    if elevs_response.status_code == 200:
        map_object.parse_elevation_data(elevs_response)
    else:
        print('No usable elevation data was returned.')
