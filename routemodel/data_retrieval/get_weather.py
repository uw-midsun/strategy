import sys
import os.path
sys.path.append(os.path.dirname(__file__))

from config import WEATHER_API_KEY

one_call = 'https://api.openweathermap.org/data/2.5/onecall?lat=35.6870&lon=-105.9378&exclude=hour,daily&units=metric'
headers = {'Content-Type': }
path = '/Users/anhmai/Desktop/weather\ api '
with open(path, 'r') as wea2021:
    x = next(wea2021)
    for line in wea2021:
        row = line.split(',')
        # assign lon and lat
        lon = float(row[1])
        lat = float(row[2])
        # make call
        params = {'key': api_key, 'lat': lat, 'lon': lon}
        response = requests.get(one_call, headers=headers, params=params)
        # output weather data
        