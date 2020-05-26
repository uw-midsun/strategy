# This file calculates the angle per cell from the solar array
# 0 rad/degrees is in reference to the tail of car
from math import pi, atan
import csv


filename = 'MSXIV-Strategy-Cell-Angles.csv'

# Write new file or append to file
mode = input("New (n) or Append (a): ")


# Calculation formulas
def to_deg(angle_rad):

    deg = float(angle_rad * 180 / pi)
    return deg


# Average angle of the panel
def calculate_angle(dy, dz, data):  # calculates angle from normal

    norm_angle = atan(dy/dz)

    print("Normalized Angle:", norm_angle, "radians")
    data.append(norm_angle)

    norm_angle_deg = to_deg(norm_angle)
    print("Normalized Angle:", norm_angle_deg, "degrees")
    data.append(norm_angle_deg)


# Writing a new file
if mode == 'n':
    # Adding headers to the file: W
    headers = ['Cell ID', 'dy', 'dz', 'Angle (Radians)', 'Angle (Degrees)']

    with open(filename, 'w', newline='\n') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        wr.writerow(headers)


# Appending to file
with open(filename, 'a', newline='\n') as csvfile:
    wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    data = []

    try:
        # When complete, use Ctrl-C KeyboardInterrupt
        while True:

            solar_cell_id = input("Solar Cell ID: ")  # STRING ID of cell
            data.append(solar_cell_id)

            dy = float(input("dy value - opposite (mm): "))  # in x-y plane
            data.append(dy)

            dz = float(input("dz value - adjacent (mm): "))
            data.append(dz)

            calculate_angle(dy, dz, data)

            wr.writerow(data)

            data = []

    except (KeyboardInterrupt,EOFError):  # Ctrl-C Ctrl-D
        pass
