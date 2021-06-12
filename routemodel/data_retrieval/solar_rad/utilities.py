import json
import requests
import math

#constants
SPEED = 60.0
EARTH_RAD = 6371.0

#solcast api call
def get_radiation_data(longitude, latitude, api_key):
    base_url = 'https://api.solcast.com.au/'
    headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_key)}
    #creating dictionary of parameters (not sure if I should be creating this here or not)
    params = {
        'latitude': latitude,
        'longitude': longitude
    }
    api_url = base_url + '/world_radiation/forecasts'
    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

#takes two pairs of long, lat and calculates distance (km) between them (a1,b1 - lon, a2,b2 - lat)
def find_distance(a1, a2, b1, b2):
    #converting to radians
    diff1 = ((b2-a2) * math.pi) / 180.0
    diff2 = ((b1-a1) * math.pi) / 180.0
    a1_rad = (a2 * math.pi) / 180.0
    a2_rad = (b2 * math.pi) / 180.0
    #haversine formula to find distance
    t1 = math.pow(math.sin(diff1/2), 2)
    t2 = math.cos(a1_rad) * math.cos(a2_rad) * math.pow(math.sin(diff2/2), 2) 
    d = 2*EARTH_RAD*math.asin(math.sqrt(t1 + t2))
    return d

#time in hours
def get_time(distance):
    return distance/SPEED
    