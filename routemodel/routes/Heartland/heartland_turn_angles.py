import math
import csv
import pandas as pd


def gen_vectors(points):
    """
    Generates vectors between adjacent coordinates
    @param points: list of dictionaries of coordinates Ex: [{lat1: long1}, {lat2: long2},... {latN: longN}]
    @return: list of tuples of vector components Ex: [(x1, y1), (x2, y2) ... (xn, yn)]
    """
    vectors = []
    last_point = (0, 0)

    for val in points:
        for key, value in val.items():
            # Create vectors between adjacent coordinates
            current_point = (float(key), float(value))
            current_vector = (current_point[0] - last_point[0], current_point[1] - last_point[1])
            vectors.append(current_vector)
            last_point = current_point

    # delete the first vector as it will just be the first coordinate
    del vectors[0]
    return vectors


def angle_calculation(vectors):
    """
    Calculates angle between two vectors
    @param vectors: List of vectors
    @return: List of angles (in degrees) between consecutive vectors
    """
    deg_list = []
    for i in range(1, len(vectors)):
        # Solving for the angle between two vectors
        numerator = (vectors[i - 1][0] * vectors[i][0] + vectors[i - 1][1] * vectors[i][1])
        denominator = ((math.sqrt((vectors[i - 1][0] ** 2) + (vectors[i - 1][1] ** 2))
                        * math.sqrt((vectors[i][0] ** 2) + (vectors[i][1] ** 2))))
        if denominator == 0:
            return
        if (numerator / denominator) > 1 or (numerator / denominator) < -1:
            return

        radii = math.acos(numerator / denominator)
        # Convert to degrees
        degree_val = round(math.degrees(radii), 5)
        deg_list.append(degree_val)

    return deg_list


if __name__ == '__main__':
    COORDINATES_FILE = "heartland_turn_coordinates.csv"  # Fill in the CSV that contains the turn coordinates
    coordinates_list = []

    headers = ['Latitude', 'Longitude', 'Turn Angle (Degrees)']
    turn_angle_df = pd.DataFrame(columns=headers)
    with open(COORDINATES_FILE, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        # Iterate over each row in the csv using reader object
        i = 0
        for row in csv_reader:
            if len(row) == 0:
                continue
            i += 1
            x_val = [float(row[0])]
            y_val = [float(row[1])]
            coordinates_list.append(dict(zip(x_val, y_val)))
            # Process every 3 points so two vectors are generated
            if i % 3 == 0:
                # Extract middle point to list in the csv
                for key, value in coordinates_list[1].items():
                    lat = key
                    long = value
                vector_list = gen_vectors(coordinates_list)
                deg = angle_calculation(vector_list)
                print(deg[0])
                turn_angle_df = turn_angle_df.append({'Latitude': lat,
                                                      'Longitude': long,
                                                      'Turn Angle (Degrees)': deg[0]},
                                                     ignore_index=True)
                # Not the best of doing this but just deleting the previous list so we can process the next 3 points
                del coordinates_list
                coordinates_list = []

    print(turn_angle_df)
