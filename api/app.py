from flask import jsonify
import sys
import os.path
sys.path.append('../')
from api import app, db, ma, DATA_API_ENDPOINT
from optimization.car_model import Car
import requests

from api.models import Log, LogSchema

log_schema = LogSchema()
logs_schema = LogSchema(many=True)

car = Car()

@app.before_first_request
def init_db():
    db.create_all()

@app.route('/', methods=['GET'])
def home():
    return 'success'

# expected_data_format = [{
#         'velocity': 0,
#         'recommended_velocity': 0,
#         'elevation': 10
# }]

@app.route('/mobile', methods=['GET'])
def getMobileData():
    current_data = requests.get(DATA_API_ENDPOINT)
    
    if (current_data.status_code != 200):
        return jsonify([{}])
    current_data = current_data.json()

    response = {}
    response["velocity"] = current_data["iss_position"]["longitude"]
    response["recommended_velocity"] = current_data["iss_position"]["latitude"]
    response["elevation"] = car.force_req(current_data["timestamp"])

    new_entry = Log(response["velocity"], response["recommended_velocity"], response["elevation"])
    print(new_entry)
    db.session.add(new_entry)
    db.session.commit()

    response_query = Log.query.order_by(Log.id.desc()).first()
    return log_schema.jsonify(response_query)

    # return jsonify([response])

app.run()