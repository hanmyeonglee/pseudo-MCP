from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = "C:\xampp\htdocs\main\model\osmosis-mcp-4b"

# 모델 로드 (자동으로 CPU+GPU 혼합 메모리 사용)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map="auto",  # CPU+GPU 자동 혼합
    torch_dtype="auto",  # bfloat16이 config.json에 지정되어 있으면 그대로 사용
)

tokenizer = AutoTokenizer.from_pretrained(model_path)

# 입력 및 생성
input_text = "Hello, how are you?"
inputs = tokenizer(input_text, return_tensors="pt")
inputs = {k: v.to(model.device) for k, v in inputs.items()}  # GPU에 올릴 수 있으면 올림

output = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(output[0], skip_special_tokens=True))
