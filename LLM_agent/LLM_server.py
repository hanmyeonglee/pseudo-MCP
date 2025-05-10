from flask import Flask, request, abort, jsonify
import os

from agent import generate

app = Flask(__name__)
app.secret_key = os.urandom(32)
app.name = "MCP-finetuned-LLM"

def is_valid_tool(tool: dict):
    return isinstance(tool, dict) and \
        'name' in tool and \
        'description' in tool and \
        'inputSchema' in tool and \
        isinstance(inputSchema := tool.get('inputSchema'), dict) and \
        'type' in inputSchema and \
        'properties' in inputSchema and \
        'required' in inputSchema

@app.route("/", method=["POST"])
def index():
    if not request.is_json:
        abort(415)
    
    data = request.json
    if 'tools_list' not in data \
        or 'user_input' not in data \
        or 'id' not in data:
        abort(400)
    
    id = data.get('id')
    tools_list = data.get('tools_list')
    user_input = data.get('user_input')
    if any(is_valid_tool(tool) for tool in tools_list):
        abort(400)
    
    try:
        answer = generate(tools_list, user_input)
    except:
        abort(500)
    
    return jsonify({
        'id': id,
        'answer': answer
    }), 200

app.run('0.0.0.0', 3001)