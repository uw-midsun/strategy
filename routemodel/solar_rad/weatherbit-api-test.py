import json
import requests
import time

api_key = 'na'
base_url = 'https://api.weatherbit.io/v2.0/forecast/hourly'

headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_key)}



# adding call every 15 mins -------------
# will edit this path so it is not reliant on my computer
path = '/Users/linnaluo/Documents/OneDrive/mid-sun/strategy/routemodel/routes/ASC2018.csv'
with open(path, 'r') as asc2018:
	h = next(asc2018)
	num = 0
	for line in asc2018:
		row = line.split(',')
                #get long and lat
		longitude = float(row[1])
		lattitude = float(row[2])
                #make api call
		params = {'key': api_key, 'lat': lattitude, 'lon': longitude, 'hours': 1}
		response = requests.get(base_url, headers=headers, params=params)
		#print solar rad field
		if response.status_code == 200:
			#print(json.loads(response.content.decode('utf-8')))
			extract_response = json.loads(response.content.decode('utf-8'))
			print(extract_response["data"][0]["solar_rad"])
			print('\n')
			num += 1
		else:
			print('None')
		if num > 19: #do first 20 calls
			break
		#wait 15 minutes (900 seconds, assuming we reach every new destination in 15 minutes)
		time.sleep(900)
