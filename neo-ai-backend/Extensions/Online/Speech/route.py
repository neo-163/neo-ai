from fastapi import FastAPI, APIRouter, APIRouter, File, Body, UploadFile, Response
from pydantic import BaseModel
from Extensions.Online.Speech.ali_speech_recognition import ali_speech_recognition
from Extensions.Online.Speech.ali_speech_synthesis import ali_speech_synthesis
from Extensions.Online.Speech.ali_speech_voice_list import ali_speech_voice_list

app = FastAPI()


class RequestData(BaseModel):
    text: str
    voice: str

router = APIRouter(prefix="/speech")


@router.post("/ali_speech_short_recognition")
async def ali_speech_recognition_route(audio_file: UploadFile = File(...)):
    result = await ali_speech_recognition(audio_file)
    if result:
        return {"code": 200, "result": result}
    else:
        return {"code": 400, "error": "Speech recognition failed"}


@router.post("/ali_speech_short_synthesis")
async def ali_speech_synthesis_route(request: RequestData):
    result, audio_data = ali_speech_synthesis(request.text, request.voice)
    if audio_data:
        return Response(content=audio_data, media_type="audio/wav")
    else:
        return {"code": 400, "result": result}

app.include_router(router)


@router.post("/ali_speech_voice_list")
async def ali_speech_voice_list_route():
    result = ali_speech_voice_list()
    return {"code": 200, "result": {"voice_list": result}}