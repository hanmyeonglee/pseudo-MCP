from transformers import AutoTokenizer, AutoModelForCausalLM
import json

MODEL_PATH = "C:\\xampp\\htdocs\\main\\model\\osmosis-mcp-4b"
MODEL = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    trust_remote_code=True,
    torch_dtype="auto"
)

Tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

TEMPLATE = """<|im_start|>system
You are an AI assistant that selects and uses tools to answer user requests.

You have access to the following tools:
%s

Given a user's natural language request, pick the most appropriate tool and generate a JSON call using the tool name and valid input arguments.

Only respond in the following format:

<tool_call>
{"name": "<tool_name>", "arguments": { ... }}
</tool_call>
<|im_end|>

<|im_start|>user
%s<|im_end|>
"""

def generate(tools_list: list, user_input: str) -> dict:
    input_text = TEMPLATE % (json.dumps(tools_list), user_input)
    inputs = Tokenizer(input_text, return_tensors="pt")
    inputs = {k: v.to(MODEL.device) for k, v in inputs.items()}

    output = MODEL.generate(**inputs, max_new_tokens=50)
    answer = Tokenizer.decode(output[0], skip_special_tokens=True).strip()

    delimiter = "<tool_call>"
    answer = answer.split(delimiter)[2].replace("</tool_call>", "").strip()

    return json.loads(answer)