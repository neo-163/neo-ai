from fastapi import APIRouter, Form
from pydantic import BaseModel
from Extension.Demo.demo_logic import test1, test2

router = APIRouter(prefix="/demo")


class RequestData(BaseModel):
    text: str


@router.get("/")
async def root():
    return {"code": 200, "result": "Neo AI!"}


@router.get("/test_get")
async def test1_route(request: RequestData):
    result = test1(request.text)
    if result:
        return {"code": 200, "text": result}
    else:
        return {"code": 400, "text": result}


@router.post("/test_post")
async def test2_route(text: str = Form(...)):
    result = test2(text)
    if result:
        return {"code": 200, "text": result}
    else:
        return {"code": 400, "text": result}
