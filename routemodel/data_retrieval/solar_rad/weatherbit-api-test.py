import json
import requests
import time
import sys
import os.path
from config import WEATHERBIT_API_KEY
api_key = WEATHERBIT_API_KEY

base_url = 'https://api.weatherbit.io/v2.0/forecast/hourly'

headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_key)}

def makeAPICall (longitude, lattitude, hour):
        #make api call
	params = {'key': api_key, 'lat': lattitude, 'lon': longitude, 'hours': hour}
	response = requests.get(base_url, headers=headers, params=params)
	#print solar rad field
	if response.status_code == 200:
		#print(json.loads(response.content.decode('utf-8')))
		extract_response = json.loads(response.content.decode('utf-8'))
		print(extract_response["data"][hour-1]["solar_rad"])
		print('\n')
	else:
		print('None')



# adding call every 15 mins -------------
# !! -> having an issue here with the file path
path = os.path.join(os.path.dirname(__file__),'..','../routes/ASC2018.csv')
with open(path, 'r') as asc2018:
	next(asc2018)
	num = 0
	for line in asc2018:
		row = line.split(',')
                #get long and lat
		longitude = float(row[1])
		lattitude = float(row[2])
                #make api call
		makeAPICall(longitude, lattitude, 1)		

		#get second (predictive) call for next location
		next(asc2018)
		longitude = float(row[1])
		lattitude = float(row[2])
		#make second api call
		makeAPICall(longitude, lattitude, 2)

		num += 1

		if num > 0: #do first 20 calls
			break
		#wait 15 minutes (900 seconds, assuming we reach every new destination in 15 minutes)
		time.sleep(1)
