from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sys
import os.path

import processing

DATABASE_NAME = 'test.db'

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(sys.path[0], DATABASE_NAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.create_all()

ma = Marshmallow(app)

@app.route('/', methods=['GET'])
def home():
    return 'success'

@app.route('/mobile', methods=['GET'])
def mobileData():
    return jsonify(processing.getMobileData())

app.run()