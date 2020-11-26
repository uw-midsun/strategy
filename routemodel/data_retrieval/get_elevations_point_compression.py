import requests
import pandas as pd
import sys
import os.path
from csv import reader
from config import API_KEY
sys.path.append(os.path.dirname(sys.path[0]))
BASE_URL = 'https://dev.virtualearth.net/REST/v1/'
ELEVATIONS_FILE = os.path.join(sys.path[0], '../../routemodel/routes/heartland_elevations.csv')
COORDINATES_FILE = os.path.join(sys.path[0], '../../routemodel/routes/heartland_coordinates.csv')

class ElevationDataRetrieval:
    def __init__(self, wps: list, vwps: list, ht='sealevel'):
        """
        Initialize MapData
        @param wps: list of dictionaries of major waypoints inputted by user
        @param vwps: list of dictionaries of minor waypoints inputted by user
        @param ht: elevations response height model option
        """
        self.waypts = wps
        self.viawaypts = vwps
        self.heights = ht

    def point_compression(self):
        """
        Compresses point data to Base-64 string
        @return: String
        In Depth description of algorithim can be found @:
        https://docs.microsoft.com/en-us/bingmaps/rest-services/elevations/point-compression-algorithm
        """
        compressed_points = ""
        lat = 0
        long = 0
        # Dict to convert Base 10 to Bing's Base 64 compressed text
        encoder_dict = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H",
                        8: "I", 9: "J", 10: "K", 11: "L", 12: "M", 13: "N", 14: "O",
                        15: "P", 16: "Q", 17: "R", 18: "S", 19: "T", 20: "U", 21: "V",
                        22: "W", 23: "X", 24: "Y", 25: "Z", 26: "a", 27: "b", 28: "c",
                        29: "d", 30: "e", 31: "f", 32: "g", 33: "h", 34: "i", 35: "j",
                        36: "k", 37: "l", 38: "m", 39: "n", 40: "o", 41: "p", 42: "q",
                        43: "r", 44: "s", 45: "t", 46: "u", 47: "v", 48: "w", 49: "x",
                        50: "y", 51: "z", 52: "0", 53: "1", 54: "2", 55: "3", 56: "4",
                        57: "5", 58: "6", 59: "7", 60: "8", 61: "9", 62: "_", 63: "-"}
        # Step 1
        for index, waypoint in enumerate(self.waypts):
            for key in waypoint.keys():

                # Step 2
                new_lat = int(round(float(key) * 100000))
                new_long = int(round(float(waypoint[key]) * 100000))

                # Step 3
                dx = (new_lat - lat)
                dy = (new_long - long)
                lat = new_lat
                long = new_long

                # Step 4
                dy *= 2
                dx *= 2

                # Step 5
                if dx < 0:
                    dx = abs(dx) - 1
                if dy < 0:
                    dy = abs(dy) - 1

                # Step 6
                index = int(((dx + dy) * (dx + dy + 1) / 2) + dx)

                # Step 7
                rem = []
                while index > 0:
                    rem.append(int(index % 32))
                    index = int(index / 32)

                # Step 8
                for i in range(0, len(rem) - 1):
                    rem[i] += 32

                # Step 9
                for i in rem:
                    compressed_points += encoder_dict[i]

        return compressed_points

    def modified_get_elevation_data(self, points):
        """
        Modified getting elevation data response from Bing Maps API.
        @param points: Compressed base 64 string containing coordinates data
        @return: Requests.response object from API call
        """
        # Since we are passing in the compressed points, we need to build the request URL in a different way
        # append specified elevation URL details
        url = BASE_URL + 'Elevation/List?'

        # add parameters to URL
        url += 'points={}&heights={}&key={}'.format(points, self.heights, API_KEY)

        # request URL and return response
        response = requests.get(url)
        return response.json()

    def parse_elevation_data(self, response):
        """
        Parsing through Elevations API call response.
        @param response: Requests.response object from API call
        @return: boolean
        """
        # This line is modified from the original module as we already converted response to dict earlier
        elevations = response
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
        # needed as there are duplicate points in waypoints that are not returned in elevations
        index_check = 0

        for index, waypoint in enumerate(self.waypts):
            for key in waypoint.keys():
                # added to ensure that loop is broken when the index goes past the end of elevations
                # duplicate points caused self.waypts to have more points than returned elevations
                try:
                     indexCheck = elevations[counter]
                except:
                     break

                elevation_df = elevation_df.append({'Latitude': key,
                                                    'Longitude': waypoint[key],
                                                    'Elevation': elevations[counter]},
                                                     ignore_index = True)
                counter += 1
            try:
                # added because we did not use the minor waypoints parameter
                if self.viawaypts is None:
                    break

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

# method calls to generate the heartland elevations
if __name__ == '__main__':
    # This generates a list of dictionaries for the coordinates
    COORDINATES_LISTX = []
    COORDINATES_LISTY = []
    COORDINATES_LIST = []
    with open(COORDINATES_FILE, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            COORDINATES_LISTX.append(row[0])
            COORDINATES_LISTY.append(row[1])
        COORDINATES_LIST.append(dict(zip(COORDINATES_LISTX, COORDINATES_LISTY)))

    heartland_elevations = ElevationDataRetrieval(COORDINATES_LIST, None)
    api_response = heartland_elevations.modified_get_elevation_data(heartland_elevations.point_compression())
    heartland_elevations.parse_elevation_data(api_response)
