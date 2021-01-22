import pandas as pd
import os
import sys

DATA = "can_messages.csv"

df = pd.read_csv(os.path.join(sys.path[0], DATA))
df.dropna(inplace=True)
df.drop(df[df.sender != "BMS_CARRIER"].index, inplace=True)
print(df)
print(len(df.index))