import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from Extensions.Online.Speech.setting import AccessKey_ID, AccessKey_Secret

# 如果有redis，token在有效时间内，可以保存在redis中，每次请求时，先从redis中获取token，如果token过期，则重新获取token并更新redis。
def get_token():
    client = AcsClient(
        AccessKey_ID,
        AccessKey_Secret,
        "cn-shanghai"
    )

    request = CommonRequest()
    request.set_method('POST')
    request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
    request.set_version('2019-02-28')
    request.set_action_name('CreateToken')

    try:
        response = client.do_action_with_exception(request)
        print(response)

        jss = json.loads(response)
        if 'Token' in jss and 'Id' in jss['Token']:
            token = jss['Token']['Id']
            expireTime = jss['Token']['ExpireTime']
            print("token = " + token)
            print("expireTime = " + str(expireTime))
            return token
    except Exception as e:
        print(e)
