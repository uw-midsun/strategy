import gpxpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#from mpl_toolkits.basemap import Basemap
import datetime
from geopy import distance
from math import sqrt, floor
import numpy as np
import pandas as pd
from pandas import DataFrame


gpx_file = open('ASC-2018-GPS-Route-Data.gpx','r')

gpx = gpxpy.parse(gpx_file)
data = []
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            data.append(point)
for waypoint in gpx.waypoints:
                print('waypoint{0} -> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude))

for route in gpx.routes:
    print('Route:')
    for point in route.points:
        print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

start = data[0]
end = data [-1]

print(len(gpx.tracks))
print(len(gpx.tracks[0].segments))
print(len(gpx.tracks[0].segments[0].points))
print(gpx.tracks[0])

#plt.figure(figsize=(8,8))
#m = Basemap(projection='ortho', resolution=None, lat_0=50, lon_0=-100)
#m.bluemarble(scale=0.5)


df = pd.DataFrame(columns=['lon','lat','alt','time'])

for point in data:
    df = df.append({'lon': point.longitude, 'lat': point.latitude, 'alt': point.elevation, 'time': point.time}, ignore_index=True)
df.to_csv('ASC2018.csv')
threedee = plt.figure().gca(projection='3d')
threedee.scatter(df['lat'], df['lon'], df['alt'])
threedee.set_xlabel('Lat')
threedee.set_ylabel('Lon')
threedee.set_zlabel('Alt')
plt.show()

print(df['lon'][0] - df['lon'][1])
print(df['lon'][1] - df['lon'][2])
print(df['lon'][2] - df['lon'][3])


