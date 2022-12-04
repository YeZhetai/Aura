from nonebot import get_driver, get_bot
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.log import logger
from nonebot_plugin_rauthman import isInService
from nonebot.adapters.onebot.v11 import Event as onebot_event
import datetime
from .config import Config


plugin_config = Config.parse_obj(get_driver().config)


ping = on_command("ping", rule = to_me(), priority = 5)
broadcast = on_command("广播", rule = to_me() & isInService('broadcast', 10), priority = 5)


@ping.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    stripped_arg = args.extract_plain_text()  # 去掉消息首尾的空白符

    if stripped_arg:
        matcher.set_arg("ping_data", args)
    logger.info("ping is " + args)


@ping.got("ping_data", prompt="没有识别到内容，请发送ping的内容")
async def receive(ping_data: Message = Arg(), ping_name: str = ArgPlainText("ping_data")):
    
    logger.info("received ping is " + ping_name)
 
    bot = get_bot()

    await bot.call_api(api="_send_group_notice",group_id=641726234, content = "1234")
#    await ping.finish(ping_name)


@broadcast.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    stripped_arg = args.extract_plain_text()

    if stripped_arg:
        matcher.set_arg("broadcast_data", args)
    logger.info("broadcast is " + args)

@broadcast.got("broadcast_data", prompt="没有识别到内容，请发送广播的内容")
async def receive(broadcast_data: Message = Arg(), broadcast_name: str = ArgPlainText("broadcast_data")):
    logger.info("received broadcast is " + broadcast_name)

    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = '[CQ:at,qq=all]\n※※※  集结通知  ※※※\n{}\n{}'.format(time, broadcast_name) 
    group_id = get_driver().config.broadcast_channel
    bot = get_bot()
    await bot.call_api(api="send_group_msg",group_id=group_id, message = message)
