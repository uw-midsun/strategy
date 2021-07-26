import sys
import os.path
import requests
import xml.etree.ElementTree  as ElementTree

OSM_URL = 'https://api.openstreetmap.org/api/0.6'
OSRM_URL = 'http://router.project-osrm.org'

""" 
Method 1: 
    For each coordinate passed in, get its node ID from OSM API.
    Once all coordinates' node ID's are collected, query again to get its information,
        and flag the nodes with a traffic signal/stop tag.
"""

def get_node_ids(lat: str, long: str):
    """
    @param lat: string representing latitude
    @param long: string representing longitude
    @return: OSM node ids corresponding to the coordinates
    """

    query = OSRM_URL + '/nearest/v1/driving/{},{}'.format(long,lat)
    response = requests.get(query)
    node_list = response.json()['waypoints'][0]['nodes']
    node_str = str()
    for node in node_list:
        if (node is not 0):
            node_str += '{},'.format(node)
    return node_str

def get_stop_query(coordinates: list):
    """
    @param coordinates: list of dictionaries for coordinates.
        Format as: [{lat1: long1}, {lat2: long2},... {latN: longN}]
    @return: API response for node descriptions of all the coordinates
    """

    query = OSM_URL + '/nodes/?nodes='
    for index, point in enumerate(coordinates):
        for key, value in point.items():
            node_ids = get_node_ids(key, value)
            query += str(node_ids)
    print(query)
    return requests.get(query)

def parse_stop_data(response):
    """
    @param response: response xml from Open Street Map query, containing
        information of nodes (coordinates)
    @return: list of coordinates representing stop sign/signal locations
    """

    stop_coords = []
    try:
        tree = ElementTree.fromstring(response.content)
        for element in tree.iterfind('node'):
            for child in list(element):
                if (child.attrib['v'] == 'stop' or child.attrib['v'] == 'traffic_signals'):
                    stop_coords.append({element.attrib['lat']: element.attrib['lon']})
                    break
    except:
        print("Returned an invalid response")
    return stop_coords


""" 
Method 2: 
    Pass all coordinates as points of a path, and retrieve all node ids along the path.
    Then, send a query for the information of all these node ids, 
        and flag the nodes with a traffic signal/stop tag.
"""

def get_path_nodes (waypoints: list):
    """
    @param coordinates: list of dictionaries for coordinates.
        Format as: [{lat1: long1}, {lat2: long2},... {latN: longN}]
    @return: API response for node descriptions of all the coordinates
    """

    query = OSRM_URL + '/route/v1/driving/'
    params = '?overview=false&annotations=true'
    for index, waypoint in enumerate(waypoints):
        for key, value in waypoint.items():
            query += '{},{};'.format(value, key)
    query = query[:-1] + params
    return requests.get(query).json()

def get_path_stop_query (response):
    """
    @param response: API response for node descriptions of all the coordinates.
        It should be in json format
    @return: list of coordinates that represent a stop sign/signal location.
    """

    query = OSM_URL + '/nodes/?nodes='
    stop_coords = []
    route_data = response
    for leg in route_data["routes"][0]["legs"]:
        query_new = query + str(leg["annotation"]["nodes"])[1:-1]
        res = requests.get(query_new, headers={"Accept": "application/json"})
        if res.status_code == 200:
            for element in res.json()["elements"]:
                if "tags" in element and "highway" in element["tags"] and (element["tags"]["highway"] == "stops" or element["tags"]["highway"] == "traffic_signals"):
                    stop_coords.append({element["lat"]:element["lon"]})
    return stop_coords
