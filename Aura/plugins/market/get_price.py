import yaml
import json
from urllib.request import Request, urlopen
import re


async def get_json(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) like Gecko'  # 伪装浏览器
    }
    request = Request(url, headers=headers)
    html = urlopen(request)
    rq_data = json.loads(html.read())  # 这里取到的是一个包含字典的列表，我也不知道为啥，以后再说
    return rq_data[0]


async def match_item(user_input, item_list):
    suggestions = []
    pattern = '.*'.join(user_input)
    regex = re.compile(pattern)
    for item in item_list:
        match = regex.search(item)
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]


async def get_price(url: str) -> str:
    with open('DB.yaml', 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.Loader)
        item_list = []
        for key in data:
            item_list.append(key)
    if url not in data:
        return '查询到以下物品：\n.isk '+'\n.isk '.join(await match_item(url, item_list))

    item = url
    item_id = data[item]
    api_url = 'https://api.evemarketer.com/ec/marketstat/json?usesystem=30000142&typeid=' + str(item_id)
    # evemarketer的API地址
    print(api_url)
    data = await get_json(api_url)
    sell_data = data['sell']
    price = "{:,}".format(sell_data['min'])

    return f'欧服物价：\n{item}\n\n吉他最低售价 {price}\n\n价格来自EVEMARKETER'
