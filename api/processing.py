from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import requests
import sys
import os
sys.path.append('../')
from optimization.car_model import Car

DATA_API_ENDPOINT = 'http://api.open-notify.org/iss-now.json'

# expected_data_format = [{
#         'velocity': 0,
#         'recommended_velocity': 0,
#         'elevation': 10
# }]

car = Car()

def getMobileData():

    current_data = requests.get(DATA_API_ENDPOINT)
    
    if (current_data.status_code != 200):
        return [{}]
    current_data = current_data.json()

    response = {}
    response["velocity"] = current_data["iss_position"]["longitude"]
    response["recommended_velocity"] = current_data["iss_position"]["latitude"]
    response["elevation"] = car.force_req(current_data["timestamp"])

    new_entry = Log(response["velocity"], response["recommended_velocity"], response["elevation"])
    print(new_entry)
    db.session.add(new_entry)
    db.session.commit()

    return([response])
