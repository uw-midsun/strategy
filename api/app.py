from flask import Flask, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sys
import os.path
sys.path.append('../')
from optimization.car_model import Car
from datetime import datetime

DATABASE_NAME = 'db.sqlite'
DATA_API_ENDPOINT = 'http://api.open-notify.org/iss-now.json'

app = Flask(__name__)
app.config['DEBUG'] = True
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, DATABASE_NAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# from api.log_models import Log, LogSchema

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_time = db.Column(db.DateTime, default=datetime.utcnow)
    velocity = db.Column(db.Float)
    recommended_velocity = db.Column(db.Float)
    elevation = db.Column(db.Float)

    def __init__(self, velocity, recommended_velocity, elevation):
        self.velocity = velocity
        self.recommended_velocity = recommended_velocity
        self.elevation = elevation

class LogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # fields=('id', 'entry_time', 'velocity', 'recommended_velocity', 'elevation')
        model = Log
    id = ma.auto_field()

log_schema = LogSchema()
logs_schema = LogSchema(many=True)

car = Car()

@app.before_first_request
def init_db():
    db.create_all()

@app.route('/', methods=['GET'])
def home():
    return 'success'

@app.route('/mobile', methods=['GET'])
def mobileData():
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

    return jsonify([response])
    # return jsonify(api.processing.getMobileData())

app.run()