import pandas as pd
from haversine import haversine, Unit
import matplotlib.pyplot as plt
import sys
import os.path
sys.path.append(os.path.dirname(__file__))

ELEVATIONS_FILE = os.path.join(sys.path[0], '../routemodel/routes/ASC2021/ASC2021_elevations_draft.csv')
df = pd.read_csv(ELEVATIONS_FILE, delimiter=',', index_col=0)

elevations = df['elevation'].to_numpy()
distances = [0]

for i in range(1, len(df)):
    distances.append(
        distances[-1] +
        haversine(
            (df.loc[i - 1, 'latitude'], df.loc[i - 1, 'longitude']), 
            (df.loc[i, 'latitude'], df.loc[i, 'longitude']), 
            unit = Unit.METERS)
    )

print(elevations)
print(distances)

plt.plot([d / 1000 for d in distances], elevations)
# plt.grid(b=True)
plt.title("Draft ASC 2021 route")
plt.xlabel("Distance travelled (km)")
plt.ylabel("Current elevation")
plt.show()
