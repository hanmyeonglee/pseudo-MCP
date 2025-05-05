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