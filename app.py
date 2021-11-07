import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'

@app.route('/relays/<relay_id>', methods=['GET'])
def get_relay(relay_id):
    return ''+ relay_id

@app.route('/relays/<relay_id>', methods=['PUT'])
def update_relay(relay_id):
    data = json.loads(request.data)
    return ''+ data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')