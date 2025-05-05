import os, inspect, tools
from flask import Flask, request, make_response, jsonify, Request

from jsonrpc import (
    jsonrpc,
    jsonrpc_error,
    is_valid_jsonrpc,
    is_valid_call
)

app = Flask(__name__)
app.secret_key = os.urandom(32)
app.name = 'general-server'

def get_function_name():
    """Return the name of caller function

    Returns:
        string: the name of caller
    """
    return inspect.stack()[1].function

def listing_tools():
    TOOLS = []
    functions = inspect.getmembers(tools, inspect.isfunction)
    for name, function in functions:
        tool = { 'name': name }
        inputschema = {}
        properties = {}
        required = []
        docstring = inspect.getdoc(function)
        
        idx = docstring.find('\n')
        description = docstring[:idx]
        tool['description'] = description

        if 'Args' in docstring:
            idx = docstring.find('Args:\n') + 6
            args = docstring[idx:]
            for line in args.splitlines():
                if line == '': break
                line = line.strip()
                arg_name, _, typ = line.partition(' ')
                if 'optional' not in line:
                    required.append(arg_name)
                typ = typ.strip('()').partition(', optional')[0]
                properties[arg_name] = { "type": typ }

        idx = docstring.find('Returns:\n    ') + 13
        typ = docstring[idx:]

        inputschema['type'] = typ
        inputschema['properties'] = properties
        inputschema['required'] = required

        tool['inputSchema'] = inputschema

        TOOLS.append(tool)

    return TOOLS

@app.route('/initialize', methods=['POST'])
def initialize():
    code = is_valid_jsonrpc(request, [get_function_name()])
    if code != 1:
        message = jsonrpc(id=-1, error=jsonrpc_error(code))
        return jsonify(message), 415

    data = request.json
    id = data.get('id')
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

@app.route('/tools/list', methods=['POST'])
def list():
    code = is_valid_jsonrpc(request, ['tools/' + get_function_name()])
    if code != 1:
        message = jsonrpc(id=-1, error=jsonrpc_error(code))
        return jsonify(message), 415
    
    data = request.json
    id = data.get('id')
    message = jsonrpc(id, result={ "tools": listing_tools() })
    return jsonify(message), 200

@app.route('/tools/call')
def tool():
    TOOLS = listing_tools()
    code = is_valid_jsonrpc(request, ['tools/' + get_function_name()])
    if code != 1:
        message = jsonrpc(id=-1, error=jsonrpc_error(code))
        return jsonify(message), 415
    
    data = request.json
    id = data.get('id')
    methods = ['tools/' + d['name'] for d in TOOLS]
    code = is_valid_call(data, TOOLS, methods)
    if code != 1:
        message = jsonrpc(id=-1, error=jsonrpc_error(code))
        return jsonify(message), 400
    
    params = data.get('params')
    name = params.get('name')
    arguments = params.get('arguments')
    actual_function = getattr(tools, name)
    result = actual_function(**arguments)

    message = jsonrpc(id=id, result=result)
    return jsonify(message), 200