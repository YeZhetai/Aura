
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot
from os import path


nonebot.init()

nonebot.load_plugins("Aura/plugins")
# 加载插件目录
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
nonebot.load_builtin_plugins()

app = nonebot.get_asgi()

if __name__ == '__main__':

    nonebot.run()
