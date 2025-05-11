from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import os

from agent import generate

app = Flask(__name__)
app.secret_key = os.urandom(32)
app.name = "MCP-finetuned-LLM"

CORS(app)

def is_valid_tool(tool: dict):
    return isinstance(tool, dict) and \
        'name' in tool and \
        'description' in tool and \
        'inputSchema' in tool and \
        isinstance(inputSchema := tool.get('inputSchema'), dict) and \
        'type' in inputSchema and \
        'properties' in inputSchema and \
        'required' in inputSchema

@app.route("/", methods=["POST"])
def index():
    if not request.is_json:
        abort(415)
    
    data = request.json
    if 'tools_list' not in data \
        or 'user_input' not in data \
        or 'id' not in data:
        print("Not Valid JSONRPC")
        abort(400)
    
    id = data.get('id')
    tools_list = data.get('tools_list')
    user_input = data.get('user_input')
    if any(not is_valid_tool(tool) for tool in tools_list):
        print("Not Valid ToolList")
        abort(400)
    
    try:
        answer = generate(tools_list, user_input)
        print(answer)
    except Exception as e:
        print(e)
        abort(500)
    
    return jsonify({
        'id': id,
        'answer': answer
    }), 200

app.run('0.0.0.0', 3001)