import sys
import os.path
import requests
import csv
import pandas as pd
import math
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(__file__))
from config import WEATHER_API_KEY


def get_wind_data(lat, long):
    """
    Calls OpenWeather API to get wind data and returns JSON response 
    @param lat: latitude coordinate  
    @param long: longitude coordinate
    @return: Requests.response.json() object from API call
    """

    # URL Example: api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
    url = "http://api.openweathermap.org/data/2.5/weather?"
    units = "metric"

    # Define all parameters to be inserted into the URL
    url += "lat={}&lon={}&appid={}&units={}".format(lat, long, WEATHER_API_KEY, units)

    # Call OpenWeather API and return response object
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

    print("An error occurred: ", response.json())
    sys.exit()


def parse_wind_data(response):
    """
    Parses the OpenWeather API call for relevant data
    @param response: Requests.response.json() object from API call
    @return: Dataframe containing relevant wind data
    """

    # Parse down to relevant information
    try:
        lat = response['coord']['lat']
        long = response['coord']['lon']
        wind_speed = response['wind']['speed']
        wind_deg = response['wind']['deg']
    except KeyError as err:
        print("Error with the following key: ", err)
        sys.exit()

    # Initialize dataframe and populate with wind data
    headers = ['Latitude', 'Longitude', 'Wind Speed (m/s)', 'Direction in Deg']
    wind_df = pd.DataFrame(columns=headers)
    wind_df = wind_df.append({'Latitude': lat,
                              'Longitude': long,
                              'Wind Speed (m/s)': wind_speed,
                              'Direction in Deg': wind_deg},
                             ignore_index=True)
    return wind_df


def gen_car_vector(points):
    """
    Generates a vector between adjacent coordinates, to model the car's direction of travel
    @param points: list of length 2 containing tuples containing coordinates Ex: [(lat1, long1), (lat2, long2)]
    @return: tuple containing a vector modelling the car
    """

    # Create a vector between the first and second tuple
    car_vector = (points[1][0] - points[0][0], points[1][1] - points[0][1])

    # Convert to unit vector
    magnitude_car_vector = math.sqrt(car_vector[0] * car_vector[0] + car_vector[1] * car_vector[1])
    unit_car_vector = (car_vector[0] / magnitude_car_vector, car_vector[1] / magnitude_car_vector)

    return unit_car_vector


def gen_wind_vector(wind_speed, wind_dir):
    """
    Generates a vector to model wind direction and speed
    @param wind_speed: wind speed in m/s
    @param wind_dir: angle of wind in degrees (on a wind direction compass)
    @return: tuple containing a vector modelling the wind
    """

    # Convert the wind angle to a polar angle
    polar_theta = 90 - wind_dir
    if polar_theta < 0:
        polar_theta += 360

    polar_theta = math.radians(polar_theta)

    # Convert from polar coordinates to rectangular coordinates
    x_component = wind_speed * math.cos(polar_theta)
    y_component = wind_speed * math.sin(polar_theta)

    # Resolve rounding error
    if abs(x_component) < 0.0001:
        x_component = 0
    if abs(y_component) < 0.0001:
        y_component = 0

    # Create tuple for wind vector
    wind_vector = (x_component, y_component)

    return wind_vector


def get_wind_component(wind_vector, car_vector):
    """
    Projects wind vector onto car vector to get the wind vector component
    @param wind_vector: tuple containing a vector modelling the wind
    @param car_vector: tuple containing a vector modelling the car
    @return: tuple containing vector modelling the component of wind that is in the direction of the car's motion
    """

    # Solving for the component of wind vector that's parallel to the car vector i.e project wind vect onto car vect
    projection = ((wind_vector[0] * car_vector[0] + wind_vector[1] * car_vector[1]) * car_vector[0],
                  (wind_vector[0] * car_vector[0] + wind_vector[1] * car_vector[1]) * car_vector[1])
    parallel_wind_component = projection

    return parallel_wind_component


def visualize_vectors(wind_vector, unit_car_vector):
    """
    Plots the wind vector, car vector and projected wind vector for visualization, not critical to model functionality
    @param wind_vector: tuple containing a vector modelling the wind
    @param unit_car_vector: tuple containing a vector modelling the car

    """

    # Initialize origin
    x = [0]
    y = [0]

    # Create unit wind vector
    wind_vector_magnitude = math.sqrt(wind_vector[0] * wind_vector[0] + wind_vector[1] * wind_vector[1])
    unit_wind_vector = (wind_vector[0] / wind_vector_magnitude, wind_vector[1] / wind_vector_magnitude)

    projection = (
        (unit_wind_vector[0] * unit_car_vector[0] + unit_wind_vector[1] * unit_car_vector[1]) * unit_car_vector[0],
        (unit_wind_vector[0] * unit_car_vector[0] + unit_wind_vector[1] * unit_car_vector[1]) * unit_car_vector[1]
                )
    unit_parallel_wind_component = projection

    print("Unit Wind Vector:", unit_wind_vector)
    print("Unit Car Vector:", unit_car_vector)
    print("Unit Proj Vector:", unit_parallel_wind_component)
    plt.quiver(x, y, unit_wind_vector[0], unit_wind_vector[1], color='b', units='xy', scale=1, label="Wind Direction")
    plt.quiver(x, y, unit_car_vector[0], unit_car_vector[1], color='r', units='xy', scale=1, label="Car Direction")
    plt.quiver(x, y, unit_parallel_wind_component[0], unit_parallel_wind_component[1], color='g', units='xy', scale=1,
               label="Projected Wind")
    plt.title('Vector Plot')

    # set the x-limits and y-limits
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)

    # Show plot
    plt.legend(loc="upper left")
    plt.grid()
    plt.show()


def wind_model_main(coordinates_list):
    """
    Calculates the drag of the car for a series of two points, drag is calculated based on wind data at 2nd point
    @param coordinates_list: list of length 2 containing tuples containing coordinates Ex: [(lat1, long1), (lat2, long2)]
    @return: Drag force in N

    """
    # Generate vector modelling car's direction of travel
    car_vector = gen_car_vector(coordinates_list)

    # Get wind data from API for a given coordinate point
    current_point = coordinates_list[1]
    response = get_wind_data(current_point[0], current_point[1])

    # Parse API response to get relevant data
    wind_df = parse_wind_data(response)
    wind_speed = wind_df.iloc[0]['Wind Speed (m/s)']
    wind_direction = wind_df.iloc[0]['Direction in Deg']

    # Generate a wind vector and solve for component of wind parallel to car's direction of travel
    wind_vector = gen_wind_vector(wind_speed, wind_direction)
    parallel_wind_component = get_wind_component(wind_vector, car_vector)
    parallel_wind_component_magnitude = math.sqrt(parallel_wind_component[0] * parallel_wind_component[0] +
                                                  parallel_wind_component[1] * parallel_wind_component[1])

    # If wind component is in same direction of car, must subtract wind component from car speed
    if ((parallel_wind_component[0] * car_vector[0]) >= 0) or ((parallel_wind_component[1] * car_vector[0]) >= 1):
        parallel_wind_component_magnitude = parallel_wind_component_magnitude * -1

    # Set variables for the drag force equation
    fluid_density = 1.225  # TODO calculate based on the a coordinate
    car_velocity = 15  # Temp value,  change once measured in reality
    car_frontal_area = 2.8  # Temp value, change once measured in reality
    drag_coefficient = 0.201  # Temp value, once measured in reality
    relative_velocity = car_velocity + parallel_wind_component_magnitude

    # Calculate Drag force
    drag_force = 1/2 * (fluid_density * relative_velocity * relative_velocity * drag_coefficient * car_frontal_area)

    return drag_force


if __name__ == '__main__':
    COORDINATES_FILE = ""  # Fill in the CSV of a route for which you want drag data
    coordinates_list = []
    headers = ['Point 1', 'Point 2', 'Drag Force (N)']
    drag_df = pd.DataFrame(columns=headers)
    with open(COORDINATES_FILE, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)

        # Iterate over each row in the csv using reader object
        i = 1
        for row in csv_reader:
            if len(row) == 0:
                continue

            # Create a tuple for each coordinate in the form (lat, long)
            x_val = float(row[0])
            y_val = float(row[1])
            coordinate = (float(row[0]), float(row[1]))
            coordinates_list.append(coordinate)

            # Run the wind model for two points at a time
            if i % 2 == 0:
                drag = wind_model_main(coordinates_list)

                # Initialize dataframe and populate with drag data
                drag_df = drag_df.append({'Point 1': coordinates_list[0],
                                          'Point 2': coordinates_list[1],
                                          'Drag Force (N)': drag},
                                         ignore_index=True)
                coordinates_list = []
            i += 1

    print(drag_df)
