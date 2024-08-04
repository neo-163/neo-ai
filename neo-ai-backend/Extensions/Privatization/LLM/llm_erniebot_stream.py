import requests
import json
import time
from Extensions.Privatization.LLM.setting import Erniebot_API_KEY, Erniebot_SECRET_KEY


def gen_erniebot_stream(prompt, ai_name, ai_role, agent):
    response = get_stream_response(prompt, ai_name, ai_role)
    for chunk in response.iter_lines():
        chunk = chunk.decode("utf8")
        if chunk[:5] == "data:":
            chunk = chunk[5:]
        yield chunk
        time.sleep(0.01)


def get_access_token(ak, sk):
    auth_url = "https://aip.baidubce.com/oauth/2.0/token"
    resp = requests.get(auth_url, params={
                        "grant_type": "client_credentials", "client_id": ak, 'client_secret': sk})
    return resp.json().get("access_token")


def get_stream_response(prompt, ai_name, ai_role):
    # token价格：https://cloud.baidu.com/doc/WENXINWORKSHOP/s/hlrk4akp7?feedback=1
    # ernie-tiny-8k ernie_speed

    model = "ernie-tiny-8k"
    ak = Erniebot_API_KEY
    sk = Erniebot_SECRET_KEY
    source = "&sourceVer=0.0.1&source=app_center&appName=streamDemo"

    base_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/"+model
    url = base_url + "?access_token=" + get_access_token(ak, sk) + source
    data = {
        "system": ai_name+' '+ai_role,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
    }
    payload = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    return requests.post(url, headers=headers, data=payload, stream=True)
