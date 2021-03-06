import json
import requests

api_key = 'IVUgOl4ATKF3lmhJv2kmhl8APY4KXxu6'
base_url = 'https://api.solcast.com.au/'

headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_key)}

def get_radiation_data(latitude, longitude):
    #creating dictionary of parameters (not sure if I should be creating this here or not)
    params = [
        {
        'latitude': latitude,
        'longitude': longitude
        },
        {
        'latitude': latitude,
        'longitude': longitude
        }
    ]

    api_url = base_url + '/world_radiation/forecasts'
    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        print(response.status_code)
        return None

#driver code
ret = get_radiation_data(-80.547245,43.473550) #UW coordinates
with open('solcast-response.txt', 'w') as f:
    f.write(json.dumps(ret))
