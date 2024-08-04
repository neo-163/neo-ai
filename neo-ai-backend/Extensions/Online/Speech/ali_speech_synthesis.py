import http.client
import json
import os
from datetime import datetime
from Extensions.Online.Speech.ali_token import get_token
from Extensions.Online.Speech.setting import appKey


def ali_speech_synthesis(text, voice):

    format = 'wav'
    sampleRate = 16000

    host = 'nls-gateway-cn-shanghai.aliyuncs.com'
    url = 'https://' + host + '/stream/v1/tts'

    httpHeaders = {
        'Content-Type': 'application/json'
    }

    body = {'appkey': appKey, 'token': get_token(), 'text': text,
            'format': format, 'sample_rate': sampleRate}
    # voice 发音人，可选，默认是xiaoyun，选项：标准女：zhiya，播音女：zhistella，标准男：kenny，播音男：stanley，儿童女声：xiaobei
    body['voice'] = voice
    # volume 音量，范围是0~100，可选，默认50
    body['volume'] = 50
    # speech_rate 语速，范围是-500~500，可选，默认是0
    body['speech_rate'] = 0
    # pitch_rate 语调，范围是-500~500，可选，默认是0
    body['pitch_rate'] = 0

    body = json.dumps(body)
    print('The POST request body content: ' + body)

    conn = http.client.HTTPSConnection(host)
    conn.request(method='POST', url=url, body=body, headers=httpHeaders)

    response = conn.getresponse()
    print('Response status and response reason:')
    print(response.status, response.reason)

    contentType = response.getheader('Content-Type')
    print(contentType)

    body = response.read()

    now = datetime.now()
    year = now.strftime("%Y")
    year_month_day = now.strftime("%Y%m%d")
    timestamp = now.strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}."+format

    audio_dir = f"Resources/Audio/{year}/{year_month_day}"
    os.makedirs(audio_dir, exist_ok=True)

    audioSaveFile = f"{audio_dir}/{filename}"

    if 'audio/mpeg' == contentType:
        with open(audioSaveFile, mode='wb') as f:
            f.write(body)
        print('The POST request succeed!')
        with open(audioSaveFile, mode='rb') as f:
            audio_data = f.read()
        result = 'The POST request succeed!'
    else:
        print('The POST request failed: ' + str(body))
        result = 'The POST request failed: ' + str(body)
        audio_data = None

    conn.close()

    return result, audio_data
