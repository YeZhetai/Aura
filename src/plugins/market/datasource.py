import yaml
import httpx
import re
import sqlite3
from nonebot.log import logger
from tortoise import Tortoise
from src.plugins.databasemanager.market_data import MarketData


#async def match_commend():



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

        if len(suggestion) == 0:
            return "无法找到物品，请确认物品名称"
        else:
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


async def check_sn(item_id):
    sn_api_url = 'https://www.ceve-market.org/api/market/region/10000002/system/30000142/type/'+str(item_id)+'.json'
    #
    logger.info("check api "+ sn_api_url)
    sn_price = await data_process(sn_api_url)

    return f'\n----------\n国服物价：\n{sn_price}'


# async def check_tq(item_id):
#     tq_api_url = 'https://www.ceve-market.org/tqapi/market/region/10000002/system/30000142/type/'+str(item_id)+'.json'
#     logger.info("check api "+ tq_api_url)
#     tq_price = await data_process(tq_api_url)
#     return f'\n----------\n欧服物价：\n{tq_price}'


async def check_1v(item_id):
    return

async def get_price(item_id) -> str:
    api_data = await check_sn(item_id)
    return api_data

async def get_local_price(item_id) -> str:
    result = await MarketData.get_market_data(item_id)
    logger.info(result)
    price_list = []
    if result:
        for line in result:
            price_list.append(line['price'])
        logger.debug(price_list)
        sell_price = "{:,.2f}".format(min(price_list))
        return f'\n----------\n1V星城售价 {sell_price}'
    else:
        return f'\n----------\n1V星城售价\n未找到本地数据，请确认星城有订单或稍后再试\n当前版本可能是出错了，请联系管理员'