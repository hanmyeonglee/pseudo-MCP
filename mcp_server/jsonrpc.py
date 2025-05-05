from flask import Request
import json

ERROR_INFO = json.load(open('jsonrpc_config.json'))
ERROR_INFO = {code: msg for code, msg, _ in ERROR_INFO}

def jsonrpc_error(code):
    code = code if code in ERROR_INFO else -32000
    msg = ERROR_INFO.get(code)
    return {
        "code": code, "message": msg
    }

def jsonrpc(id: int | str, mode: str = "2.0", result = None, error = None):
    ret = { 'jsonrpc': mode, 'id': id }
    if result is not None: ret['result'] = result
    elif error is not None: ret['error'] = error
    else:
        ret['error'] = jsonrpc_error(-32603)

    return ret

def is_valid_jsonrpc(request: Request, methods: list[str]) -> int:
    if not request.is_json: return -32700

    if not isinstance(data := request.json, dict) \
        or data.get('jsonrpc', None) != '2.0' \
        or 'id' not in data: 
            return -32600
    
    if data.get('method') not in methods: return -32601

    return 1

def is_valid_call(data: dict, spec: dict, methods: list):
    if 'params' not in data: return -32600
    params = data.get('params')
    
    if 'name' not in params or 'arguments' not in params: return -32602
    name = params.get('name')
    arguments = params.get('arguments')

    if name not in methods: return -32602
    specification = next(filter(lambda d: d.get('name') == name, spec))
    inputSchema = specification.get('inputSchema')
    properties = inputSchema.get('properties')
    required = inputSchema.get('required')
    
    if any(required_variable not in arguments.keys() for required_variable in required): return -32602
    if any(given_variable not in properties.keys() for given_variable in arguments.keys()): return -32602

    return 1