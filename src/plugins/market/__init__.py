
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot_plugin_rauthman import isInService
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.log import logger
from .datasource import find_id, get_price, suggestion


market = on_command("isk", rule=isInService('查价', 1), priority=5)


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
        await market.finish(item_name + price)













