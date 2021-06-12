import sys
import os.path
import requests
import xml.etree.ElementTree  as ElementTree

BASE_URL = 'http://overpass-api.de/api/xapi?*'

def build_bbox_query(coordinates: list, query_type: str):
    """
    @param coordinates: list of dictionaries for coordinates.
        Format as: [{lat1: long1}, {lat2: long2},... {latN: longN}]
    @param query_type: type of query to create
        'stop' for stop sign, 'traffic_signals' for traffic stops
    @return: completed query url string
    """
    min_lat = min_long = 180.0
    max_lat = max_long = -180.0 
    for index, point in enumerate(coordinates):
        for key in point.keys():
            key_float = float(key)
            value_float = float(point[key])

            if (key_float < min_lat):
                min_lat = key_float
            if (key_float > max_lat):
                max_lat = key_float
            if (value_float < min_long):
                min_long = value_float
            if (value_float > max_long):
                max_long = value_float

    query = BASE_URL + '[highway={}][bbox={},{},{},{}]'.format(query_type, min_long, min_lat, max_long, max_lat)
    return query

def get_stop_query (query: str):
    """
    @param query: openstreetmap url to send GET API request
    @return: list of dictionaries that are coordinates {lat:long}
    """
    stop_result = []
    try:
        response = requests.get(query)
        # OpenStreetMap API returns XML response to parse
        tree = ElementTree.fromstring(response.content)
        for element in tree.iterfind('node'):
            stop_result.append({element.attrib['lat']: element.attrib['lon']})
    except:
        print("Returned an invalid reponse")
    return stop_result
