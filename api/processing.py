import requests
import sys
import os
sys.path.append('../')
from optimization.car_model import Car

def getMobileData():
    response = {}

    current_data = requests.get('http://api.open-notify.org/iss-now.json')
    
    if (current_data.status_code != 200):
        return [{}]
    
    current_data = current_data.json()

    response["velocity"] = current_data["iss_position"]["longitude"]
    response["recommended_velocity"] = current_data["iss_position"]["latitude"]

    car = Car()
    response["elevation"] = car.force_req(current_data["timestamp"])

    return([response])
