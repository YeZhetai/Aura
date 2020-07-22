import asyncio

import nonebot
import config
from os import path


if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(path.abspath(__file__)), 'Aura', 'plugins'), 'Aura.plugins'
    )
    nonebot.run()
