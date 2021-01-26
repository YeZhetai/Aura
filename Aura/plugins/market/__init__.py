import yaml
import requests
import re
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import Permission


market = on_command("isk", rule=None, permission=Permission(), priority=5)


@market.handle()
async def _(bot: Bot, event: Event, state: T_State):
    stripped_arg = str(event.get_message()).strip()  # 去掉消息首尾的空白符

    if stripped_arg:
        state["item"] = stripped_arg
    print("item")


@market.got("item", prompt='123')
async def receive(bot: Bot, event: Event, state: T_State):
    item = state["item"]
    price = await get_price(item)
    await market.send(price)


async def get_json(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) like Gecko'  # 伪装浏览器
    }
    request = requests.get(url, headers=headers)
    if request.status_code == requests.codes.ok:
        rq_data = request.json()
    else:
        rq_data = {request.status_code}
    print(rq_data)
    return rq_data


async def match_item(user_input, item_list):
    suggestions = []
    pattern = '.*'.join(user_input)
    regex = re.compile(pattern)
    for item in item_list:
        match = regex.search(item)
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]


async def data_process(url):
    data = await get_json(url)
    if data is list:
        return data
    sell_data = data['sell']
    buy_data = data['buy']
    sell_min = "{:,.2f}".format(float(sell_data['min']))
    buy_max = "{:,.2f}".format(float(buy_data['max']))
    return f"吉他最低售价 {sell_min}\n吉他最高收价 {buy_max}"


async def get_price(url: str) -> str:
    with open('DB.yaml', 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.Loader)
        item_list = []
        for key in data:
            item_list.append(key)
    if url not in data:
        suggestion = await match_item(url, item_list)

        return '查询到以下物品：\n.isk '+'\n.isk '.join(suggestion)

    item = url
    item_id = data[item]
    of_api_url = 'https://www.ceve-market.org/tqapi/market/region/10000002/system/30000142/type/'+str(item_id)+'.json'
    # evemarketer的API地址
    print(of_api_url)
    of_price = await data_process(of_api_url)
    gf_api_url = 'https://www.ceve-market.org/api/market/region/10000002/system/30000142/type/'+str(item_id)+'.json'
    #
    print(gf_api_url)
    gf_price = await data_process(gf_api_url)

    return f'{item}\n----------\n国服物价：\n{gf_price}\n----------\n欧服物价：\n{of_price}'










