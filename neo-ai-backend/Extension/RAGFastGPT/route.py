from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import List
from fastapi.responses import StreamingResponse
import requests
import json
from Extension.RAGFastGPT.setting import FastGPT_URL, FastGPT_Qwen_API_KEY, FastGPT_Erniebot_API_KEY

router = APIRouter(prefix="/rag_fastgpt")


class Message(BaseModel):
    content: str
    role: str


class RequestData(BaseModel):
    chatId: str
    stream: bool
    detail: bool
    messages: List[Message]


@router.post("/ask")
async def chat_completions(request: RequestData):

    headers = {
        'Authorization': 'Bearer ' + FastGPT_Qwen_API_KEY,
        'Content-Type': 'application/json'
    }
    data = request.dict()

    response = requests.post(FastGPT_URL, headers=headers,
                             data=json.dumps(data), stream=True)
    response.raise_for_status()  # Raise an HTTPError for bad responses

    def generate():
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                print(f"Decoded line: {decoded_line}")  # Debugging output
                yield f"{decoded_line}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
