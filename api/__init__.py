from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sys
import os.path
sys.path.append('../')

class ProdConfig:
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    DATABASE_NAME = 'data.sqlite'

class DevConfig:
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    DATABASE_NAME = 'db.sqlite'


DATA_API_ENDPOINT = 'http://api.open-notify.org/iss-now.json'

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, DevConfig.DATABASE_NAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config.from_object(DevConfig)

db = SQLAlchemy()
db.init_app(app)
ma = Marshmallow()
