
from nonebot import on_command, require, get_driver, get_bot

require("nonebot_plugin_apscheduler")

from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from nonebot_plugin_rauthman import isInService
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.log import logger
from nonebot_plugin_apscheduler import scheduler
from src.plugins.market.datasource import find_id, get_price, suggestion, get_local_price
from src.plugins.market.makedb import make_db
from src.plugins.market.refreshtoken import refreshtoken
from src.plugins.market.marketdata import downdata



market = on_command("isk", rule=isInService('查价'), priority=5)
local = on_command("1V", rule=isInService("查价"), priority=5)
download = on_command('update', priority=1, permission=SUPERUSER)


@scheduler.scheduled_job('cron', hour=0, minute=0)
async def update_market_data():
    bot = get_bot()
    driver = get_driver()
    superid = driver.config.superusers
    for id in superid:
        await bot.send_private_msg(user_id=int(id), message='开始更新市场数据')
    await refreshtoken()
    await downdata()
    await make_db()
    logger.info("Market data updated")
    for id in superid:
        await bot.send_private_msg(user_id=int(id), message='市场数据更新完成')


@market.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    stripped_arg = args.extract_plain_text()  # 去掉消息首尾的空白符

    if stripped_arg:
        matcher.set_arg("item", args)
    logger.info("search item is " + args)


@market.got("item", prompt='123')
async def receive(item: Message = Arg(), item_name: str = ArgPlainText("item")):
    logger.info("received item name is " + item_name)
    item_id = await find_id(item_name)    
    logger.info(item_id)
    if item_id is None:
        await market.finish(await suggestion(item_name))
    else:
        price = await get_price(item_id)
        price_1v = await get_local_price(item_id)
        await market.finish(item_name + price + price_1v)


@local.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    stripped_arg = args.extract_plain_text()

    if stripped_arg:
        matcher.set_arg("item", args)
    logger.info("search item is " + args)


@local.got("item", prompt='123')
async def receive(item: Message = Arg(), item_name: str = ArgPlainText("item")):
    logger.info("received item name is " + item_name)
    item_id = await find_id(item_name)
    logger.info(item_id)
    if item_id is None:
        await local.finish(await suggestion(item_name))
    else:
        price = await get_local_price(item_id)
        await local.finish(item_name + price)


@download.handle()
async def _():
    logger.info("update market data")
    await download.send("update market data")
    await refreshtoken()
    await downdata()
    await make_db()
    await download.send("update market data done")












