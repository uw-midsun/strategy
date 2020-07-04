from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sys
import os.path
sys.path.append('../')

DATABASE_NAME = 'db.sqlite'
DATA_API_ENDPOINT = 'http://api.open-notify.org/iss-now.json'

print("hello")

app = Flask(__name__)
app.config['DEBUG'] = True
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, DATABASE_NAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)
ma = Marshmallow()
