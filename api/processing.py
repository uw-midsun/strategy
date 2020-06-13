import requests
import sys
import os
sys.path.append('../')
from optimization.car_model import Car

DATA_API_ENDPOINT = 'http://api.open-notify.org/iss-now.json'

def getMobileData():
    current_data = requests.get(DATA_API_ENDPOINT)
    
    if (current_data.status_code != 200):
        return [{}]
    
    current_data = current_data.json()

    response = {}
    
    response["velocity"] = current_data["iss_position"]["longitude"]
    response["recommended_velocity"] = current_data["iss_position"]["latitude"]

    car = Car()
    response["elevation"] = car.force_req(current_data["timestamp"])

    return([response])
