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
    if type(rq_data) is list:
        api_data = rq_data[0]
    else:
        api_data = rq_data
    return api_data


async def match_item(user_input, item_list):
    suggestions = []
    pattern = '.*'.join(user_input)
    regex = re.compile(pattern)
    for item in item_list:
        match = regex.search(item)
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]


async def data_process(api_url):
    data = await get_json(api_url)
    sell_data = data['sell']
    buy_data = data['buy']
    sell_min = "{:,.2f}".format(sell_data['min'])
    buy_max = "{:,.2f}".format(buy_data['max'])
    return f"吉他最低售价 {sell_min}\n吉他最高收价 {buy_max}"


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
    of_api_url = 'https://api.evemarketer.com/ec/marketstat/json?usesystem=30000142&typeid=' + str(item_id)
    # evemarketer的API地址
    print(of_api_url)
    gf_api_url = 'https://www.ceve-market.org/api/market/region/10000002/system/30000142/type/'+str(item_id)+'.json'
    #
    print(gf_api_url)
    of_price = await data_process(of_api_url)
    gf_price = await data_process(gf_api_url)

    return f'{item}\n----------\n国服物价：\n{gf_price}\n----------\n欧服物价：\n{of_price}'
