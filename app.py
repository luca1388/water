import RPi.GPIO as GPIO
from time import sleep
from gpiozero import MCP3008
import json
from flask import Flask, request, jsonify, render_template
import lcd
GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

# VALVE_A_OPENED_PIN = 11
# VALVE_A_CLOSED_PIN = 13
# VALVE_B_OPENED_PIN = 15
# VALVE_B_CLOSED_PIN = 16

pot = MCP3008(0)

# GPIO.setup(VALVE_A_OPENED_PIN, GPIO.OUT, initial=GPIO.LOW)   # Set pin 11 to be an output pin and set initial value to low (off)
# GPIO.setup(VALVE_A_CLOSED_PIN, GPIO.OUT, initial=GPIO.LOW)   # Set pin 13 to be an output pin and set initial value to low (off)
# GPIO.setup(VALVE_B_OPENED_PIN, GPIO.OUT, initial=GPIO.LOW)   # Set pin 15 to be an output pin and set initial value to low (off)
# GPIO.setup(VALVE_B_CLOSED_PIN, GPIO.OUT, initial=GPIO.LOW)   # Set pin 15 to be an output pin and set initial value to low (off)

valve_dictionary = {
    "a": {
        "opened_pin": VALVE_A_OPENED_PIN,
        "closed_pin": VALVE_A_CLOSED_PIN,
    },
    "b": {
        "opened_pin": VALVE_B_OPENED_PIN,
        "closed_pin": VALVE_B_CLOSED_PIN,
    }
}
lcd.lcd_init()
lcd.lcd_string("Selezionare menu", lcd.LCD_LINE_1)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
        status_message = 'opening valve ' + valve_id
        GPIO.output(valve_dictionary[valve_id]['opened_pin'], GPIO.HIGH)
        GPIO.output(valve_dictionary[valve_id]['closed_pin'], GPIO.LOW)
        
    elif body_state == "off":
        status_message = 'closing valve'  + valve_id
        GPIO.output(valve_dictionary[valve_id]['opened_pin'], GPIO.LOW)
        GPIO.output(valve_dictionary[valve_id]['closed_pin'], GPIO.HIGH)

    print (status_message)
    return jsonify(success=True)

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0')
    except KeyboardInterrupt:
        GPIO.output(VALVE_A_OPENED_PIN, GPIO.LOW)
        GPIO.output(VALVE_A_CLOSED_PIN, GPIO.LOW)
        GPIO.output(VALVE_B_OPENED_PIN, GPIO.LOW)
        GPIO.output(VALVE_B_CLOSED_PIN, GPIO.LOW)
    finally:
        GPIO.cleanup() # this ensures a clean exit  
        lcd.lcd_byte(0x01, lcd.LCD_CMD)

while True:
    print(pot.value)