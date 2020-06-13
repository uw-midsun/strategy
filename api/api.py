from flask import Flask, jsonify
import processing

app = Flask(__name__)
app.config['DEBUG'] = True

# current_data = [
#     {
#         'velocity': 0,
#         'recommended_velocity': 0,
#         'elevation': 10
#     }
# ]

@app.route('/', methods=['GET'])
def home():
    return '<p>success</p>'

@app.route('/mobile', methods=['GET'])
def mobileData():
    return jsonify(processing.getMobileData())

app.run()