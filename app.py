import RPi.GPIO as GPIO
from time import sleep
import json
from flask import Flask, request, jsonify

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)   # Set pin 11 to be an output pin and set initial value to low (off)
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)   # Set pin 13 to be an output pin and set initial value to low (off)
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)   # Set pin 15 to be an output pin and set initial value to low (off)

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'

@app.route('/relays/<relay_id>', methods=['GET'])
def get_relay(relay_id):
    return ''+ relay_id

@app.route('/relays/<relay_id>', methods=['PUT'])
def update_relay(relay_id):
    try:
        body = json.loads(request.data)
        print body
        bodyState = body['data']['state']
    except:
        return 'malformed request'

    return ''+ bodyState

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
