import sys
import RPi.GPIO as GPIO
from time import sleep
from gpiozero import MCP3008
import json
from flask import Flask, request, jsonify, render_template
import lcd
import threading
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

VALVE_A_OPENED_PIN = 11
VALVE_A_CLOSED_PIN = 13
VALVE_B_OPENED_PIN = 15
VALVE_B_CLOSED_PIN = 16

pot = MCP3008(0)

GPIO.setup(VALVE_A_OPENED_PIN, GPIO.OUT, initial=GPIO.LOW)   # Set pin 11 to be an output pin and set initial value to low (off)
GPIO.setup(VALVE_A_CLOSED_PIN, GPIO.OUT, initial=GPIO.LOW)   # Set pin 13 to be an output pin and set initial value to low (off)
GPIO.setup(VALVE_B_OPENED_PIN, GPIO.OUT, initial=GPIO.LOW)   # Set pin 15 to be an output pin and set initial value to low (off)
GPIO.setup(VALVE_B_CLOSED_PIN, GPIO.OUT, initial=GPIO.LOW)   # Set pin 15 to be an output pin and set initial value to low (off)

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
print(pot.value)

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

def run_app():
    app.run(debug=False, host='0.0.0.0')

def input_listener():
    while True:
        if pot.value < 0.15 and pot.value > 0.13:
            lcd.lcd_string("Up", lcd.LCD_LINE_2)
        if pot.value < 0.1:
            lcd.lcd_string("Left", lcd.LCD_LINE_2)
        if pot.value < 0.50 and pot.value > 0.48:
            lcd.lcd_string("Right", lcd.LCD_LINE_2)
        if pot.value > 0.70 and pot.value < 0.73:
            lcd.lcd_string("Ok", lcd.LCD_LINE_2)
        if pot.value > 0.31 and pot.value < 0.33:
            lcd.lcd_string("Down", lcd.LCD_LINE_2)

if __name__ == '__main__':
    try:
        server_thread = threading.Thread(target=run_app)
        input_tread = threading.Thread(target=input_listener)

        server_thread.start()
        input_tread.start()    
    except KeyboardInterrupt:
        GPIO.output(VALVE_A_OPENED_PIN, GPIO.LOW)
        GPIO.output(VALVE_A_CLOSED_PIN, GPIO.LOW)
        GPIO.output(VALVE_B_OPENED_PIN, GPIO.LOW)
        GPIO.output(VALVE_B_CLOSED_PIN, GPIO.LOW)
        print('shutting down')
        sys.exit()
    finally:
        GPIO.cleanup() # this ensures a clean exit  
        lcd.lcd_byte(0x01, lcd.LCD_CMD)
   