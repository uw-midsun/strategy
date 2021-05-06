import pandas as pd
import sys
import os.path
sys.path.append(os.path.dirname(__file__))
from datetime import datetime, timedelta

def build_routes_points(waypoints: list, viawaypoints: list):
    """
    @param waypoints: List of dictionaries of waypoints.
        Each dictionary can only have 1 waypoint.
        Up to 25 dictionaries/elements in full list.
        Format as: [{lat1: long1}, {lat2: long2},... {latN: longN}]
    @param viawaypoints: List of dictionaries of viawaypoints. 
        Each dictionary can have 0 to 10 viawaypoints.
        Full list must be one element shorter than list of waypoints,
        to a maximum of 24 elements.
        Format as: [{lat1: long1,... latN: longN},...{},...
                    {lat1: long1,... latN: longN}]
    @return: a string of points for sending to API
    """
    counter = 0
    params = str()
    for index, waypoint in enumerate(waypoints):
        for key, value in waypoint.items():
            params += 'wp.{}={},{}&'.format(counter, 
                                            key,
                                            value)
            counter += 1
        if index < len(waypoints) - 1:
            for key, value in viawaypoints[index].items():
                    params += 'vwp.{}={},{}&'.format(counter, 
                                                     key, 
                                                     value)
                    counter += 1
         
    return params

def format_routes_query(points: str, route_attrs = 'routePath', dist_unit = 'km'):
    """
    Getting navigation data response from Bing Maps API.
    @param points: string of points formatted for requesting from Bing Maps API.
        Use points_query_builder method to build string correctly.
    @param dist_unit: Either 'km' or 'mi,' default to km since
        we're Canadian, eh. (optional)
    @param route_attrs: type of request to make (optional)
        - routePath: gives detailed list of maneuvers/directions and coordinates
        - excludeItinerary: no list of maneuvers
        - transitStops: for public transit
        - regionTravelSummary: no coordinates, maneuvers, only a summary of 
                               time and distance; can be asked for along with 
                               other options above
        - routeSummariesOnly: only a summary, other options cannot be selected
                              in conjunction
        Default is routePath. May want regionTravelSummary in conjunction.
        Format as "option1, option2" or "option1."
    @return: a string of formatted parameters to query from API
    """
    # adjust url for Route API request
    query = 'Routes?'

    # add coordinates, route attribute option, distance unit, and API key
    # to url to be requested
    query += '{}routeAttributes={}&distanceUnit={}'.format(points, 
                                                           route_attrs,
                                                           dist_unit)
    
    return query  

def parse_routing_data(response: dict):
    """
    Parsing through Routes API call response.
    @param response: Requests.response object from API call
    @return: Pandas DataFrame with columns of:
        - Latitude
        - Longitude
        - Maneuver Instruction
        - Distance to Maneuver
        - Direction
        - Street
    """
    route = response    # headers are for csv, create DataFrame to write data into
    headers = ['Latitude', 'Longitude', 'Maneuver Instruction', 'Distance to Maneuver', 'Direction', 'Street']
    route_df = pd.DataFrame(columns=headers)

    # parse through each route leg returned in response, append to dataframe
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
                    if len(item['details']) > 1:
                        street = item['details'][1].get('names')[0]
                    else:
                        street = item['details'][0].get('names')[0]
                    
                    # append data into dataframe
                    route_df = route_df.append({'Latitude': lat, 
                                                'Longitude': longit, 
                                                'Maneuver Instruction': instruction, 
                                                'Distance to Maneuver': dist, 
                                                'Direction': direction, 
                                                'Street': street}, 
                                                ignore_index = True)
    except Exception as error:
        print(f'An error occurred: {error}')
        sys.exit()
    return route_df

def time_to(speeds: list, route_df: pd.DataFrame, start_time: datetime):
    '''
    @param speeds: list of speeds car travels at. Accepts length 1 or same as number of df rows. 
        Expected to be in equivalent unit as dist_unit in `format_routes_query`
    @param route_df: Pandas Dataframe object. Expects column of 'Distance to Maneuver'
    @param start_time: DateTime object, expressing the first row's start time

    @return Pandas Dataframe object passed in, with added columns of:
        'Speed': Speed at which car travels in segment
        'Elapsed Time': Time (in hours) needed to travel segment based on given speed
        'Start Timestamp': Expected start time of segment based on speed and distance to travel
    '''

    if len(speeds) == 1:
        route_df['Speed'] = speeds[0]
    elif len(speeds) == len(route_df.index):
        route_df['Speed'] = pd.Series(speeds)
    else:
        raise ValueError("Incorrect speeds list length")

    route_df['Elapsed Time'] = route_df['Distance to Maneuver'] / route_df['Speed']
    
    timestamps = [start_time]
    timestamps.extend([timestamps[-1] + timedelta(hours=time) \
        for time in route_df['Elapsed Time'][:-1]])
    route_df['Start Timestamp'] = pd.Series(timestamps) 

    return route_df
