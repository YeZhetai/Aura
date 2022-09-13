# @Time : 2021/2/12 23:46
# @Author : YeZhetai
# @File : test.py
# @Software : PyCharm
import httpx
import re


def get_character_id(name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) like Gecko'  # 伪装浏览器
    }
    url = 'http://board.ceve-market.org/'
    client = httpx.Client()
    r = client.get(url)
    reg = r"<input type='hidden' name='csrfmiddlewaretoken' value='(.*)' />"
    pattern = re.compile(reg)
    result = pattern.findall(str(r.content, 'utf8'))
    token = result[0]

    my_data = {
        'csrfmiddlewaretoken': token,
        'search': name
    }
    r = client.post(url + 'search', data=my_data)
    print(r.url)
    char = re.findall(r"char/(.+?)/", str(r.next_request))
    return char[0]


def get_character_info():
    return


character_id = get_character_id('怎么可能日不完')
print(character_id)


