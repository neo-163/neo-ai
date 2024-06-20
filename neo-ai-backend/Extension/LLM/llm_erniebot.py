import requests
import json
from Extension.LLM.setting import Erniebot_API_KEY, Erniebot_SECRET_KEY


def erniebot(prompt, ai_name, ai_role):
    # token价格：https://cloud.baidu.com/doc/WENXINWORKSHOP/s/hlrk4akp7?feedback=1
    # ernie-tiny-8k ernie_speed

    model = "ernie-tiny-8k"
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/" + \
        model + "?access_token=" + get_access_token()

    payload = json.dumps({
        "system": ai_name+' '+ai_role,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        # 如果设置为False，AI可能会使用搜索功能来查找最新的信息或解决特定的查询，从而提供更准确、更及时的信息。
        "disable_search": False,
        # 如果设置为True，AI在提供信息时会尝试包含引用来源，比如网页链接、书籍引用等，这有助于验证信息的准确性和来源。
        "enable_citation": True,
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    data = json.loads(response.text)

    usage = data['usage']

    result = {
        "reply": data['result'],
        "prompt_tokens": usage['prompt_tokens'],
        "completion_tokens": usage['completion_tokens'],
        "total_tokens": usage['total_tokens']
    }

    return result


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """

    API_KEY = Erniebot_API_KEY
    SECRET_KEY = Erniebot_SECRET_KEY

    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials",
              "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
