from multiprocessing.connection import Client
import yaml
import httpx
import re
from nonebot.log import logger


async def match_item(name, item_list):
    suggestions = []
    pattern = '.*'.join(name)
    regex = re.compile(pattern)
    for item in item_list:
        match = regex.search(item)
        if match:
            suggestions.append((len(match.group()), match.start(), item))
            logger.info(suggestions)
    return [x for _, _, x in sorted(suggestions)]


async def suggestion(name):
    with open('DB.yaml', 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.Loader)
        item_list = []
        for key in data:
            item_list.append(key)
        suggestion = await match_item(name, item_list)

        return '查询到以下物品：\n.isk '+'\n.isk '.join(suggestion)


async def get_json(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) like Gecko'  # 伪装浏览器
    }
    Client = httpx.Client()
    r = Client.get(url=url)
    rq_data = r.json()
    return rq_data


async def find_id(user_input):
    with open('DB.yaml', 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.Loader)
        item_id = data.get(user_input)
    return item_id
    

async def data_process(url):
    data = await get_json(url)
    if data is list:
        return data
    sell_data = data['sell']
    buy_data = data['buy']
    sell_min = "{:,.2f}".format(float(sell_data['min']))
    buy_max = "{:,.2f}".format(float(buy_data['max']))
    return f"吉他最低售价 {sell_min}\n吉他最高收价 {buy_max}"


async def check(item_id):
    of_api_url = 'https://www.ceve-market.org/tqapi/market/region/10000002/system/30000142/type/'+str(item_id)+'.json'
    # evemarketer的API地址
    logger.info("check api "+ of_api_url)
    of_price = await data_process(of_api_url)
    gf_api_url = 'https://www.ceve-market.org/api/market/region/10000002/system/30000142/type/'+str(item_id)+'.json'
    #
    logger.info("check api "+ gf_api_url)
    gf_price = await data_process(gf_api_url)

    return f'\n----------\n国服物价：\n{gf_price}\n----------\n欧服物价：\n{of_price}'


async def get_price(item_id) -> str:
    api_data = await check(item_id)
    return api_data