import sys
import os.path
sys.path.append(os.path.dirname(__file__))
import requests
import csv
import collections


from config import WEATHER_API_KEY
from heartland_coordinates import longtitude, latitude
import pandas as pd

one_call_base = 'https://api.openweathermap.org/data/2.5/onecall?'
path = os.path.join(os.path.dirname(__file__), '..', 'routes\ASC2021\ASC2021_draft.csv')

location = []
with open(path, 'r') as longtitude, latitude:
    for line in longtitude, latitude:
        # read a set of latitude and longitude points
        row = line.split(',')
        lat = row[0].strip()
        lon = row[1].strip()

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
            location.append(current_temperature)
            # TODO: we'll want to look at more fields, and save into a CSV
            print(current_temperature)

        # TODO: make requests for every line (ie. for every set of latitude and longitude points)

with open('new_get_weather.csv', 'w') as f:
    data = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for row in location:   
        data.writerow([row])
