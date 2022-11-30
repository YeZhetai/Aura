# [02:00:58] Ozhika > <url=showinfo:35834//1010978252945>1V-LI2 - 不忘初心丨牢记使命 (太太你也不想雇佣记录留下可怕的痕迹吧)</url>
# [15:07:40] Ozhika > <url=showinfo:3//10000008>灼热之径</url>


import httpx
import json


async def downdata():
    with open('keys.json', 'r') as f:
        keys = json.load(f)
        access_token = keys['access_token']
        refresh_token = keys['refresh_token']


    urls = "https://esi.evepc.163.com/latest/markets/structures/1010978252945/"

    payload = {
        "datasource":"serenity",
        "page":'',
        "token":access_token
    }

    marketdata = []

    with httpx.Client() as client:
        for i in range(1, 100):
            payload['page'] = i
            res = client.get(urls, params=payload)
            print(res.url)
            if res.status_code == 200:
                data = res.json()
                print(type(data))
                marketdata.extend(data)
            else:
                print(res)
                break
            i = i + 1

    with open('marketdata.json', 'w') as f:
        json.dump(marketdata, f, indent=4)
    return()



