from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from Extensions.Privatization.RAGWeaviate.llm_erniebot_stream import gen_erniebot_stream
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/rag_weaviate")


class RequestData1(BaseModel):
    text: str
    messages: List[Dict] = []
    ai_name: str = None
    ai_role: str = None
    agent: bool = None


DEFAULT_AI_NAME = '你的名字叫Neo AI。'
DEFAULT_AI_ROLE = '你是一个AI助手。'
DEFAULT_AGENT = False


@router.post("/ask")
async def erniebot_stream(request: RequestData1):
    ai_name = request.ai_name if request.ai_name else DEFAULT_AI_NAME
    ai_role = request.ai_role if request.ai_role else DEFAULT_AI_ROLE
    agent = request.agent if request.agent else DEFAULT_AGENT
    prompt = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in request.messages])
    return StreamingResponse(gen_erniebot_stream(prompt, ai_name, ai_role, agent))
