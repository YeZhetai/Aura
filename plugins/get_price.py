import yaml
import json
from urllib.request import Request, urlopen
import os


def get_json(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) like Gecko'
    }
    request = Request(url, headers=headers)
    html = urlopen(request)
    rq_data = json.loads(html.read())
    return rq_data[0]


async def get_price(item: str) -> str:
    with open('DB.yaml', 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.Loader)
    if item not in data:
        return f'物品名称不正确，暂时仅支持完整物品名称'

    item_id = data[item]
    api_url = 'https://api.evemarketer.com/ec/marketstat/json?usesystem=30000142&typeid='+str(item_id)
    print(api_url)
    data = get_json(api_url)
    sell_data = data['sell']
    price = sell_data['min']

    return f'{item}的id是{item_id},吉他最低售价是{price}'
