# route.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from fastapi.responses import JSONResponse
import requests
import json
from Extension.RAGFastGPT.setting import FastGPT_URL, FastGPT_Qwen_API_KEY, FastGPT_Erniebot_API_KEY

router = APIRouter(prefix="/rag")


class Message(BaseModel):
    content: str
    role: str


class RequestData(BaseModel):
    chatId: str
    stream: bool
    detail: bool
    messages: List[Message]


@router.post("/ask1")
async def chat_completions(request: RequestData):

    headers = {
        'Authorization': 'Bearer ' + FastGPT_Qwen_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'chatId': request.chatId,
        'stream': request.stream,
        'detail': request.detail,
        'messages': [message.dict() for message in request.messages]
    }

    response = requests.post(FastGPT_URL, headers=headers,
                             data=json.dumps(data), stream=True)
    response.raise_for_status()  # Raise an HTTPError for bad responses

    response_data = ""

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            print(f"Decoded line: {decoded_line}")  # Debugging output
            if decoded_line.startswith("data: "):
                response_data += decoded_line[6:]
            else:
                response_data += decoded_line

    print(f"Accumulated response data: {response_data}")  # Debugging output

    # Remove the [DONE] part
    if "[DONE]" in response_data:
        response_data = response_data.replace("[DONE]", "")

    # Split the accumulated string into individual JSON objects
    response_data = response_data.strip().split("}{")
    response_data = [
        line + "}" if not line.endswith("}") else line for line in response_data]
    response_data = [
        "{" + line if not line.startswith("{") else line for line in response_data]

    # Parse the JSON objects
    json_objects = []
    for line in response_data:
        try:
            json_object = json.loads(line)
            json_objects.append(json_object)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e} for line: {line}")

    return JSONResponse(content=json_objects)
