import http.client
import json
from Extension.Speech.ali_token import get_token
from Extension.Speech.setting import appKey


async def ali_speech_recognition(audio_file):
    token = get_token()

    url = 'https://nls-gateway-cn-shanghai.aliyuncs.com/stream/v1/asr'

    format = 'wav'
    sampleRate = 16000
    enablePunctuationPrediction = True
    enableInverseTextNormalization = True
    enableVoiceDetection = False

    request = url + '?appkey=' + appKey
    request = request + '&format=' + format
    request = request + '&sample_rate=' + str(sampleRate)

    if enablePunctuationPrediction:
        request = request + '&enable_punctuation_prediction=' + 'true'

    if enableInverseTextNormalization:
        request = request + '&enable_inverse_text_normalization=' + 'true'

    if enableVoiceDetection:
        request = request + '&enable_voice_detection=' + 'true'

    print('Request: ' + request)

    audioContent = await audio_file.read()

    host = 'nls-gateway-cn-shanghai.aliyuncs.com'

    httpHeaders = {
        'X-NLS-Token': token,
        'Content-type': 'application/octet-stream',
        'Content-Length': len(audioContent)
    }

    conn = http.client.HTTPSConnection(host)

    conn.request(method='POST', url=request,
                 body=audioContent, headers=httpHeaders)

    response = conn.getresponse()
    print('Response status and response reason:')
    print(response.status, response.reason)

    body = response.read()
    try:
        print('Recognize response is:')
        body = json.loads(body)
        print(body)

        status = body['status']
        if status == 20000000:
            result = body['result']
            print('Recognize result: ' + result)
            return {"text": result}
        else:
            print('Recognizer failed!')
            return {"text": "Recognizer failed!"}

    except ValueError:
        print('The response is not json format string')
        return {"text": "The response is not json format string"}

    finally:
        conn.close()
