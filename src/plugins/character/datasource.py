from weakref import proxy
import httpx
import re
from nonebot.log import logger


async def get_character_id(name):
    with httpx.Client() as client:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) like Gecko'  # 伪装浏览器
        }
        url = 'http://board.ceve-market.org/'
        r = client.get(url=url, headers=headers, proxy="httpx://localhost:1080")
        reg = r"<input type='hidden' name='csrfmiddlewaretoken' value='(.*)' />"
        pattern = re.compile(reg)
        result = pattern.findall(str(r.content, 'utf8'))
        token = result[0]
        logger.info("token = " + token)

        my_data = {
            'csrfmiddlewaretoken': token,
            'search': name
        }
        r = client.post(url + 'search', data=my_data)
        char = re.findall(r"char/(.+?)/", str(r.next_request))
        logger.info(char)
    return char[0]


async def call_eve_esi(char_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) like Gecko'  # 伪装浏览器
    }
    url = 'https://esi.evepc.163.com/latest/characters/' + char_id + '/?datasource=serenity'
    print(url)
    client = httpx.Client()
    r = client.get(url, headers=headers)
    response = r.json()
    print(response)
    return response


async def esi_info_convert(info):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) like Gecko'  # 伪装浏览器
    }
    url_alliance = 'https://esi.evepc.163.com/latest/alliances/' + str(info["alliance_id"]) + '/?datasource=serenity'
    client = httpx.Client()
    r = client.get(url_alliance, headers=headers)
    response = r.json()
    alliance_name = response['name']
    print(alliance_name)
    url_corporation = 'https://esi.evepc.163.com/latest/corporations/' + str(info["corporation_id"]) + '/?datasource=serenity'
    r = client.get(url_corporation, headers=headers)
    response = r.json()
    corporation_name = response['name']
    print(corporation_name)
    char = str(info["name"])
    security = str(info["security_status"])
    return corporation_name, alliance_name, char, security


async def data_process(corporation_name, alliance_name, char, security):
    output = char + "\n----------\n" + corporation_name + "成员" + "\n----------\n" + alliance_name + "\n安全等级:" + security
    return output