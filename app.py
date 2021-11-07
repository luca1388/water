import RPi.GPIO as GPIO
from time import sleep
import json
from flask import Flask, request, jsonify

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

VALVE_A_OPENED_PIN = 11
VALVE_A_CLOSED_PIN = 13
VALVE_B_OPENED_PIN = 15
VALVE_B_CLOSED_PIN = 16

GPIO.setup(VALVE_A_OPENED_PIN, GPIO.OUT, initial=GPIO.LOW)   # Set pin 11 to be an output pin and set initial value to low (off)
GPIO.setup(VALVE_A_CLOSED_PIN, GPIO.OUT, initial=GPIO.LOW)   # Set pin 13 to be an output pin and set initial value to low (off)
GPIO.setup(VALVE_B_OPENED_PIN, GPIO.OUT, initial=GPIO.LOW)   # Set pin 15 to be an output pin and set initial value to low (off)
GPIO.setup(VALVE_B_CLOSED_PIN, GPIO.OUT, initial=GPIO.LOW)   # Set pin 15 to be an output pin and set initial value to low (off)

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'

@app.route('/valves/<valve_id>', methods=['GET'])
def get_relay(valve_id):
    return ''+ valve_id

@app.route('/valves/<valve_id>', methods=['PUT'])
def update_relay(valve_id):
    try:
        body = json.loads(request.data)
        print body
        body_state = body['data']['state']
    except:
        return 'malformed request'

    if body_state == "on":
        status_message = 'opening valve' + valve_id
    elif body_state == "off":
        status_message = 'closing valve' + valve_id

    print (status_message)
    return status_message

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
