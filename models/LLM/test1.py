import requests

url = "http://127.0.0.1:8001/llm_private/chat1"
headers = {"Content-Type": "application/json"}
data = {"message": "你好"}

response = requests.post(url, json=data, headers=headers, stream=True)

for chunk in response.iter_content(chunk_size=None):
    print(chunk.decode('utf-8'), end="")
