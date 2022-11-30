import httpx
import json


async def refreshtoken():
    with open('keys.json', 'r') as f:
        keys = json.load(f)
        refresh_token = keys['refresh_token']


    url = "https://login.evepc.163.com/v2/oauth/token"
    # 请求参数
    headers= {
        'Content-Type': 'application/x-www-form-urlencoded',
        'host': 'login.evepc.163.com'
        }
    payload = {
        "grant_type":"refresh_token",
        "refresh_token":refresh_token,#填入刷新令牌
        "client_id":"bc90aa496a404724a93f41b4f4e97761"#填入client_id
    }
    with httpx.Client() as client:
        res = client.post(url, data=payload,headers=headers)

    if res.status_code == 200:
        print(res.json())
        keys = res.json()
        with open('keys.json', 'w') as f:
            json.dump(keys, f)

    else:
        print(res)
    return()
    