from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from openai import OpenAI
from typing import List, Dict

router = APIRouter(prefix="/llm_private")

# 设置 OpenAI 客户端
openai_client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="not-needed")

# 对话历史：设定系统角色是一个智能助理
history: List[Dict[str, str]] = [
    {"role": "system", "content": "你是一个智能助理，你的回答总是容易理解的、正确的、有用的和内容非常精简。"},
]

def get_assistant_reply():
    completion = openai_client.chat.completions.create(
        model="local-model",
        messages=history,
        temperature=0.7,
        stream=True,
    )
    
    reply = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
            reply += chunk.choices[0].delta.content
            
    history.append({"role": "assistant", "content": reply})

@router.post("/chat")
async def chat(request: Request):
    user_input = (await request.json()).get("input")
    history.append({"role": "user", "content": user_input})
    
    return StreamingResponse(get_assistant_reply(), media_type="text/plain")

