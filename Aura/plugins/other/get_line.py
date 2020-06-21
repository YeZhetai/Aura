import requests


async def get_line(flower: str) -> str:
    flower = '绣球花'
    data = {
        'server': '剑胆琴心',
        'flower': flower,
        'random': '1611002475',
        'token': 'a0e2901fc93958c9416d6693ee5e9983'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    url = 'http://hua.arkwish.com/'
    result = requests.post(url, data, headers=headers)

    html = result.text

    print(html)
548