import sys
import os.path
import csv
import pandas as pd
import math
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from routemodel.data_retrieval.get_weather import get_weather

R = 287.058  # Specific gas constant [J/(kg * K)]
CAR_VELOCITY = 15  # Temp value,  change once measured in reality
CAR_FRONTAL_AREA = 2.8  # Temp value, change once measured in reality
DRAG_COEFFICIENT = 0.201  # Temp value, once measured in reality


def gen_car_vector(points):
    """
    Generates a vector between adjacent coordinates, to model the car's direction of travel
    @param points: list of length 2 containing tuples containing coordinates Ex: [(lat1, long1), (lat2, long2)]
    @return: tuple containing a vector modelling the car
    """

    # Create a vector between the first and second tuple
    car_vector = (points[1][0] - points[0][0], points[1][1] - points[0][1])

    # Convert to unit vector
    unit_car_vector = get_unit_vector(car_vector)

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

    # Resolve rounding error (covers the "should be 0" case)
    if abs(x_component) < 0.0001:
        x_component = 0
    if abs(y_component) < 0.0001:
        y_component = 0

    # Create tuple for wind vector
    wind_vector = (x_component, y_component)

    return wind_vector


def get_projection(vector_a, vector_b):
    """
    Projects wind vector onto car vector to get the wind vector component
    @param vector_a: tuple containing the vector to be projected onto vector B
    @param vector_b: tuple containing the vector used for the basis of the projection
    @return: tuple containing the projection of vector A onto vector B
    """

    # Project vector A onto vector B
    projection = ((vector_a[0] * vector_b[0] + vector_a[1] * vector_b[1]) * vector_b[0],
                  (vector_a[0] * vector_b[0] + vector_a[1] * vector_b[1]) * vector_b[1])

    return projection


def get_unit_vector(vector):
    """
    Converts a vector into a unit vector
    @param vector: tuple containing the vector to be converted into a unit vector
    @return: tuple containing the unit vector of the inputted vector
    """

    # Converts vector into unit vector
    vector_magnitude = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    unit_vector = (vector[0] / vector_magnitude,
                   vector[1] / vector_magnitude)

    return unit_vector


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
    unit_wind_vector = get_unit_vector(wind_vector)

    # Project onto car vector
    unit_parallel_wind_component = get_projection(unit_wind_vector, unit_car_vector)

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

    # Initialize dataframe to hold weather data
    headers = ['Latitude', 'Longitude', 'Temperature (C)', 'Wind Speed (m/s)', 'Wind Direction', 'Weather',
               'Weather Description', 'Pressure (hPa)', 'Precipitation (mm)']
    weather_df = pd.DataFrame(columns=headers)

    # Get weather data and store into dataframe
    weather_df = weather_df.append(get_weather(current_point[0], current_point[1]), ignore_index=True)

    # Parse down to relevant data
    wind_speed = weather_df.iloc[0]['Wind Speed (m/s)']
    wind_direction = weather_df.iloc[0]['Wind Direction']
    pressure = weather_df.iloc[0]['Pressure (hPa)'] * 100  # Convert hPa to Pa
    temperature = weather_df.iloc[0]['Temperature (C)'] + 273  # Convert to absolute temperature

    # Generate a wind vector and solve for component of wind parallel to car's direction of travel
    wind_vector = gen_wind_vector(wind_speed, wind_direction)
    parallel_wind_component = get_projection(wind_vector, car_vector)
    parallel_wind_component_magnitude = math.sqrt(parallel_wind_component[0] * parallel_wind_component[0] +
                                                  parallel_wind_component[1] * parallel_wind_component[1])

    # If wind component is in same direction of car, must subtract wind component from car speed
    if ((parallel_wind_component[0] * car_vector[0]) >= 0) or ((parallel_wind_component[1] * car_vector[0]) >= 1):
        parallel_wind_component_magnitude *= -1

    # Set variables for the drag force equation
    fluid_density = pressure / (R * temperature)  # Density of the air at a given point
    relative_velocity = CAR_VELOCITY + parallel_wind_component_magnitude

    # Calculate Drag force
    drag_force = 1 / 2 * (fluid_density * relative_velocity * relative_velocity * DRAG_COEFFICIENT * CAR_FRONTAL_AREA)

    return drag_force


if __name__ == '__main__':
    # File paths for ASC and Heartland are commented below
    # COORDINATES_FILE = os.path.join(os.path.dirname(__file__), '..', 'routemodel/routes/ASC2021/ASC2021_draft.csv')
    # COORDINATES_FILE = os.path.join(os.path.dirname(__file__), '..', 'routemodel/routes/Heartland/heartland_coordinates.csv')

    COORDINATES_FILE = "Fill in the CSV of a route for which you want drag data"
    coordinates_list = []
    headers = ['Point 1', 'Point 2', 'Drag Force (N)']
    drag_df = pd.DataFrame(columns=headers)
    try:
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
    except FileNotFoundError as err:
        print("An error occurred:", err)
        sys.exit()

    print(drag_df)
