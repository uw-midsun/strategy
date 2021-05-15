def get_weather():
    
    import sys
    import os.path
    sys.path.append(os.path.dirname(__file__))
    import requests
    import csv
    import json

    from config import WEATHER_API_KEY

    one_call_base = 'https://api.openweathermap.org/data/2.5/onecall?'
    path = os.path.join(os.path.dirname(__file__), '..', 'routes\ASC2021\ASC2021_draft.csv')

    location = []
    with open(path, 'r') as wea_2021:
        for line in wea_2021:
            row = line.split(',')
            lat = row[0]
            lon = row[1].strip()

            query_url = one_call_base + 'lat=' + lat + '&lon=' + lon + '&exclude=hour,daily&units=metric&appid=' + WEATHER_API_KEY

            response = requests.get(query_url)
            if response.status_code == 200:
                weather_data = response.json()

                precipitation = 0 if "rain" not in weather_data["current"]["weather"][0] else weather_data["current"]["weather"][0]["rain"]

                location.append([
                    float(lat), float(lon), 
                    weather_data["current"]["temp"],
                    weather_data["current"]["wind_speed"],
                    weather_data["current"]["wind_deg"],
                    weather_data["current"]["weather"][0]["main"],
                    weather_data["current"]["weather"][0]["description"],
                    precipitation
                ])

    with open('new_get_weather.csv', 'w', newline='') as f:
        data = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        data.writerow(['Latitude', 'Longitude', 'Temperature (C)', 'Wind Speed (m/s)', 'Wind Direction', 'Weather', 'Weather Description', 'Precipitation (mm)'])

        for row in location:   
            data.writerow(row)
