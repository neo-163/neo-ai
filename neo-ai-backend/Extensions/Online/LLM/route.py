from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from Extensions.Online.LLM.llm_erniebot import erniebot
from Extensions.Online.LLM.llm_erniebot_stream import gen_erniebot_stream
from Extensions.Online.LLM.llm_qwen import qwen
from Extensions.Online.LLM.llm_chatgpt import chatgpt
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/llm")


class RequestData(BaseModel):
    text: str
    messages: List[Dict] = []
    ai_name: str = None
    ai_role: str = None
    agent: bool = None


DEFAULT_AI_NAME = '你的名字叫Neo AI。'
DEFAULT_AI_ROLE = '你是一个AI助手。'
DEFAULT_AGENT = False


@router.post("/erniebot_stream")
async def erniebot_stream(request: RequestData):
    ai_name = request.ai_name if request.ai_name else DEFAULT_AI_NAME
    ai_role = request.ai_role if request.ai_role else DEFAULT_AI_ROLE
    agent = request.agent if request.agent else DEFAULT_AGENT
    prompt = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in request.messages])
    return StreamingResponse(gen_erniebot_stream(prompt, ai_name, ai_role, agent))


@router.post("/erniebot")
async def llm_erniebtot_route(request: RequestData):
    ai_name = request.ai_name if request.ai_name else DEFAULT_AI_NAME
    ai_role = request.ai_role if request.ai_role else DEFAULT_AI_ROLE
    prompt = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in request.messages])

    try:
        result = erniebot(prompt, ai_name, ai_role)
        if result:
            return {"code": 200, "result": result}
        else:
            return {"code": 400, "result": result}
    except Exception as e:
        return {"code": 500, "error": str(e)}


@router.post("/qwen")
async def llm_qwen_route(request: RequestData):
    ai_name = request.ai_name if request.ai_name else DEFAULT_AI_NAME
    ai_role = request.ai_role if request.ai_role else DEFAULT_AI_ROLE
    prompt = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in request.messages])

    try:
        result = qwen(prompt, ai_name, ai_role)
        if result:
            return {"code": 200, "result": result}
        else:
            return {"code": 400, "result": result}
    except Exception as e:
        return {"code": 500, "error": str(e)}


@router.post("/chatgpt")
async def llm_chatgpt_route(request: RequestData):
    ai_name = request.ai_name if request.ai_name else DEFAULT_AI_NAME
    ai_role = request.ai_role if request.ai_role else DEFAULT_AI_ROLE
    prompt = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in request.messages])

    try:
        result = chatgpt(prompt, ai_name, ai_role)
        if result:
            return {"code": 200, "result": result}
        else:
            return {"code": 400, "result": result}
    except Exception as e:
        return {"code": 500, "error": str(e)}
