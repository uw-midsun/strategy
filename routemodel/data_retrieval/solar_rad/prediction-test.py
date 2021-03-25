import time
import sys
import os.path
import csv
import utilities #utility functions
from config import SOLCAST_API_KEY
api_key = SOLCAST_API_KEY
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
    p1 = getCoordinates(asc2018)
    f = open('test.csv', 'a')
    for i in range(2): 
        while total_time < 30:
            p2 = getCoordinates(asc2018)
            #print statement CHECK
            d = utilities.findDistance(p1[0],p1[1], p2[0], p2[1])
            total_time += utilities.getTime(d) * 60 #distance in km
            p1 = p2 #tuple with lat and long

        #TEST DISTANCE FUNC
        print(p1)
        print(p2)

        #get prediction forecast (API CALL)
        ##raw_forecast = utilities.get_radiation_data(p2[0], p2[1], api_key)
        future_forecast = [i, i]
        #wait 5 minutes
        time.sleep(1)
        #get current forecast (API CALL)
        ##raw_curr = utilities.get_radiation_data(p2[0], p2[1], api_key)
        future_forecast.append(i)
        #write shtuff to csv
        
        writer = csv.writer(f)
        writer.writerow(future_forecast)
        
        #get next points for distance calculation
        total_time = 0
    f.close()
