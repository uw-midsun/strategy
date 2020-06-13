from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime

db = SQLAlchemy()
ma = Marshmallow()

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

class LogSchema(ma.Schema):
    class Meta:
        fields=('id', 'entry_time', 'velocity', 'recommended_velocity', 'elevation')