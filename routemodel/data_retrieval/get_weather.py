import sys
import os.path
sys.path.append(os.path.dirname(__file__))
import requests
import csv

from config import WEATHER_API_KEY

ONE_CALL_BASE = 'https://api.openweathermap.org/data/2.5/onecall?'
PATH = os.path.join(os.path.dirname(__file__), '..', 'routes/ASC2021/ASC2021_draft.csv')


def get_weather(lat, long, weather_api_result):
    """
    Calls OpenWeather API to get wind data and returns data in a list
    @param lat: string containing latitude value
    @param long: string containing longitude value
    @param weather_api_result: list of lists containing weather data
    @return: list of lists containing weather data

    """
    query_url = ONE_CALL_BASE + 'lat=' + lat + '&lon=' + long + '&exclude=hour,daily&units=metric&appid=' + WEATHER_API_KEY

    response = requests.get(query_url)
    if response.status_code == 200:
        weather_data = response.json()

        precipitation = 0 if "rain" not in weather_data["current"]["weather"][0] else \
        weather_data["current"]["weather"][0]["rain"]

        weather_api_result.append([
            float(lat), float(long),
            weather_data["current"]["temp"],
            weather_data["current"]["wind_speed"],
            weather_data["current"]["wind_deg"],
            weather_data["current"]["weather"][0]["main"],
            weather_data["current"]["weather"][0]["description"],
            weather_data["current"]["pressure"],
            precipitation
        ])
        return weather_api_result

    print("An error occurred: ", response.json())
    sys.exit()


def save_weather_to_csv(weather_api_data):
    """
    Writes the weather data to a CSV file
    @param weather_api_result: list of lists containing weather data

    """
    with open('new_get_weather.csv', 'w', newline='') as f:
        data = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        data.writerow([
            'Latitude',
            'Longitude',
            'Temperature (C)',
            'Wind Speed (m/s)',
            'Wind Direction',
            'Weather',
            'Weather Description',
            'Pressure (hPa)',
            'Precipitation (mm)'
        ])

        for row in weather_api_data:
            data.writerow(row)


if __name__ == '__main__':
    weather_api_result = []
    try:
        with open(PATH, 'r') as wea_2021:
            for line in wea_2021:
                row = line.split(',')
                lat = row[0]
                long = row[1].strip()
                weather_data_list = get_weather(lat, long, weather_api_result)
        save_weather_to_csv(weather_data_list)
    except FileNotFoundError as err:
        print("An error occurred:", err)
        sys.exit()
