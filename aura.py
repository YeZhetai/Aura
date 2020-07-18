import asyncio

import nonebot
import config
from os import path


def main_process():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(path.abspath(__file__)), 'Aura', 'plugins'), 'Aura.plugins'
    )
    nonebot.run()
