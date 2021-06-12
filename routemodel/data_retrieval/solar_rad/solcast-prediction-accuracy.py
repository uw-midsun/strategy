import time
import sys
import os.path
import csv
from utilities import get_radiation_data, get_time, find_distance
from config import SOLCAST_API_KEY
api_key = SOLCAST_API_KEY

#WARNING: test periodically stops running for ~4 hrs and then continues afterwards

#ALGORITHM OUTLINE
#*** writing to predictions.csv 
#find distance you will be at in 30 mins
    #calc distance between p1 and p2
    #if time travelled < 30 mins, find distance between p2 and next point
    #else return p2
#make prediction -> write to csv
#wait 30 mins
#get current -> write to csv
# ^ repeat

#returns [lon, lat]
def getCoordinates(f):
    temp = next(f)
    row = temp.split(',')
    return [float(row[1]), float(row[2])]

path = os.path.join(os.path.dirname(__file__),'..','../routes/ASC2018.csv')
total_time = 0 #in minutes
with open(path, 'r') as asc2018:
    next(asc2018)
    total_time = 0
    p2 = None
    p1 = getCoordinates(asc2018) #[long, lat]
    f = open('predictions.csv', 'a')
    for i in range(16): 
        while total_time < 30:
            p2 = getCoordinates(asc2018)
            d = find_distance(p1[0],p1[1], p2[0], p2[1])
            total_time += get_time(d) * 60 #get time in mins
            p1 = p2

        #PRINTING COORDINATES USED
        print(p1)
        print(p2) 

        #get prediction forecast (API CALL)
        raw_forecast = get_radiation_data(p2[0], p2[1], api_key)
        future_forecast = [i, raw_forecast['forecasts'][1]['ghi']]
        #current time
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(current_time)

        #wait 30 minutes
        time.sleep(1800)

        #get current forecast (API CALL)
        raw_curr = get_radiation_data(p2[0], p2[1], api_key)
        future_forecast.append(raw_curr['forecasts'][0]['ghi'])
        #write shtuff to csv
        writer = csv.writer(f)
        writer.writerow(future_forecast)

        #reset time accumulator
        total_time = 0
    f.close()
