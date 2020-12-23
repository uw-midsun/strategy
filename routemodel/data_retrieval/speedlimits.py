import pandas as pd
import sys
import os.path

sys.path.append(os.path.dirname(__file__))

from config import API_KEY

def format_url_query(points, speed_unit = 'KPH'):
    """
    @param points: List of dictionaries of waypoints.
        Each dictionary can only have 1 point.
        Up to 100 dictionaries/elements in full list.
        Format as: [{lat1: long1}, {lat2: long2},... {latN: longN}]
    @return: a string of formatted parameters to query from API
    """
    # adjust url for speed limit API request
    url = "Routes/SnapToRoad?"
    query_params = ""

    # loop through points
    # store into points string
    for index, point in enumerate(points):
        for key in point.keys():
            query_params += "{},{}".format(key, point[key])
            # prevents a semicolon from being appended to the last set of points
            # because that results in an error :P
            if index < len(points)-1: 
                query_params += ";" 
    
    # add parameters to url to be requested
    url += 'includeSpeedLimit=true&travelMode=driving&points={}&speedUnit={}&key={}'\
        .format(query_params, speed_unit, API_KEY)
    return url

def parse_speedlimit_data(response): 
    """
    Parsing through Routes API call response.
    @param response: Requests.response object from API call
    @return: Pandas DataFrame with columns of:
        - Latitude
        - Longitude
        - Street
        - Speed Limit
        - Speed Unit
    """
    speedlimits = response
    headers = ['Latitude', 'Longitude', 'Street', 'Speed Limit', 'Speed Unit']
    speedlimits_df = pd.DataFrame(columns=headers)
    
    # parse through response and append to dataframe
    try:
        for data in speedlimits['resourceSets'][0]['resources'][0]['snappedPoints']:
            lat = data.get('coordinate').get('latitude')
            long = data.get('coordinate').get('longitude')
            street = data.get('name')
            speed_limit = data.get('speedLimit')
            speed_unit = data.get('speedUnit')
            speedlimits_df = speedlimits_df.append({'Latitude': lat, 
                                                    'Longitude': long, 
                                                    'Street': street,
                                                    'Speed Limit': speed_limit,
                                                    'Speed Unit': speed_unit}, 
                                                    ignore_index = True)
    # exception handling thingy
    except Exception as error:
        print(f'An error occurred: {error}')
        sys.exit()
    return speedlimits
