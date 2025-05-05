import os, inspect, time
from flask import Flask, request, make_response, jsonify, Request

from jsonrpc import (
    jsonrpc,
    jsonrpc_error,
    is_valid_jsonrpc
)

from db import IDS, DB

app = Flask(__name__)
app.secret_key = os.urandom(32)
app.name = 'general-server'

def get_function_name():
    return inspect.stack()[1].function

@app.route('/initialize', methods=['POST'])
def initialize():
    code = is_valid_jsonrpc(request, [get_function_name()])
    if code != 1:
        message = jsonrpc(id=-1, error=jsonrpc_error(code))
        return jsonify(message), 415

    data = request.json
    id = data.get('id')
    if id in IDS:
        message = jsonrpc(id=-1, error=jsonrpc_error(-32002))
        return jsonify(message), 409
    
    IDS.add(id)
    message = jsonrpc(id=id, result={
        'capabilities': {
            'tools': {}
        },
        'serverInfo': {
            'name': app.name,
            'version': '0.1.0'
        }
    })

    return jsonify(message), 200

@app.route('/initialized', methods=['POST'])
def initialized():
    code = is_valid_jsonrpc(request, ['notification/' + get_function_name()])
    if code != 1:
        message = jsonrpc(id=-1, error=jsonrpc_error(code))
        return jsonify(message), 415
    
    data = request.json
    id = data.get('id')
    if id not in IDS:
        message = jsonrpc(id=id, error=jsonrpc_error(-32001))
        return jsonify(message), 425
    
    DB[id] = time.time()