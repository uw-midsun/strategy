import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config['DEBUG'] = True

current_data = [
    {
        'velocity': 0,
        'recommended_velocity': 0,
        'elevation': 10
    }
]

@app.route('/', methods=['GET'])
def home():
    return '<p>success</p>'

@app.route('/current', methods=['GET'])
def data():
    return jsonify(current_data)

app.run()