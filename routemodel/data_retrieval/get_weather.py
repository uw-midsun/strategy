import sys
import os.path
import requests
import pandas as pd
from config import WEATHER_API_KEY

sys.path.append(os.path.dirname(__file__))
ONE_CALL_BASE = 'https://api.openweathermap.org/data/2.5/onecall?'
PATH = os.path.join(os.path.dirname(__file__), '..', 'routes/ASC2021/ASC2021_draft.csv')


def get_weather(lat, long):
    """
    Calls OpenWeather API to get wind data and returns data in a dict
    @param lat: string containing latitude value
    @param long: string containing longitude value
    @return: dict containing the weather data

    """
    units = "metric"
    exclude = "minutely,hourly,daily,alerts"  # To exclude certain weather reports, right now just using current
    url = ONE_CALL_BASE + \
        "lat={}&lon={}&exclude={}&units={}&appid={}".format(lat, long, exclude, units, WEATHER_API_KEY)

    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()

        precipitation = 0 if "rain" not in weather_data["current"]["weather"][0] else \
            weather_data["current"]["weather"][0]["rain"]

        weather_dict = {
            'Latitude': lat,
            'Longitude': long,
            'Temperature (C)': weather_data["current"]["temp"],
            'Wind Speed (m/s)': weather_data["current"]["wind_speed"],
            'Wind Direction': weather_data["current"]["wind_deg"],
            'Weather': weather_data["current"]["weather"][0]["main"],
            'Weather Description': weather_data["current"]["weather"][0]["description"],
            'Pressure (hPa)': weather_data["current"]["pressure"],
            'Precipitation (mm)': precipitation
        }
        return weather_dict

    print("An error occurred: ", response.json())
    sys.exit()


if __name__ == '__main__':
    # Initialize dataframe and populate with headers
    headers = ['Latitude', 'Longitude', 'Temperature (C)', 'Wind Speed (m/s)', 'Wind Direction', 'Weather',
               'Weather Description', 'Pressure (hPa)', 'Precipitation (mm)']
    weather_df = pd.DataFrame(columns=headers)

    try:
        with open(PATH, 'r') as wea_2021:
            for line in wea_2021:
                row = line.split(',')
                lat = row[0]
                long = row[1].strip()

                # Get wind data for each coordinate point
                weather_df = weather_df.append(get_weather(lat, long), ignore_index=True)

        # Save to CSV
        weather_df.to_csv('get_weather_data.csv', index=False)
    except FileNotFoundError as err:
        print("An error occurred:", err)
        sys.exit()
