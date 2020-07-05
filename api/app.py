from flask import jsonify
import sys
import os.path
sys.path.append('../')
from api import app, db, ma, DATA_API_ENDPOINT
from optimization.car_model import Car
import requests
import time
from datetime import datetime, timedelta
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

from api.models import Log, LogSchema

log_schema = LogSchema()
logs_schema = LogSchema(many=True)

car = Car()

def make_repeated_requests():
    with app.app_context():
        current_data = requests.get(DATA_API_ENDPOINT)

        if (current_data.status_code != 200):
            return
        current_data = current_data.json()

        response = {}
        response["velocity"] = current_data["iss_position"]["longitude"]
        response["recommended_velocity"] = current_data["iss_position"]["latitude"]
        response["elevation"] = car.force_req(current_data["timestamp"])

        new_entry = Log(response["velocity"], response["recommended_velocity"], response["elevation"])
        print(new_entry)
        db.session.add(new_entry)
        db.session.commit()

@app.before_first_request
def init():
    db.create_all()

    scheduler = BackgroundScheduler()
    scheduler.add_job(make_repeated_requests, trigger="interval", seconds=10)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    make_repeated_requests()

@app.route('/', methods=['GET'])
def home():
    return 'success'

@app.route('/current', methods=['GET'])
def get_current_data():
    response_query = Log.query.order_by(Log.id.desc()).first()
    return log_schema.jsonify(response_query)

@app.route('/previous/<time_in_minutes>', methods=['GET'])
def get_data_over_last(time_in_minutes=60):
    # all values for last time_in_minutes
    # ordered earlier -> later
    if time_in_minutes < 1:
        time_in_minutes = 1.5

    response = Log.query.filter(datetime.utcnow() - timedelta(minutes=float(time_in_minutes)) < Log.entry_time)
    return logs_schema.jsonify(response)

if __name__ == "__main__":
    app.run()
