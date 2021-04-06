import sys
import os.path
sys.path.append(os.path.dirname(__file__))
import requests
import json
import csv

from config import WEATHER_API_KEY
one_call_base = 'https://api.openweathermap.org/data/2.5/onecall?'
path = os.path.join(os.path.dirname(__file__), '..', 'routes/ASC2021/ASC2021_draft.csv')
location = [ ]
with open(path, 'r') as wea2021:
    for line in wea2021:
        # read a set of latitude and longitude points
        row = line.split(',')
            
        #for point #1
        lat = row[0]
        lon = row[1].strip()
        location.append([float(lat),float(lon)])
        print(location)
        
        # build query to make an API call
        query_url = one_call_base + 'lat=' + lat + '&lon=' + lon + '&exclude=hour,daily&units=metric&appid=' + WEATHER_API_KEY

        # this makes our request
        response = requests.get(query_url)
        # this will check if API call was successful
        if response.status_code == 200:
            # parse response from JSON format to a dictionary object in python
            weather_data = response.json()
            # look up specific field based on the JSON structure
            current_temperature = weather_data["current"]["temp"]
            # TODO: we'll want to look at more fields, and save into a CSV
            print(current_temperature)

        # TODO: make requests for every line (ie. for every set of latitude and longitude points)
