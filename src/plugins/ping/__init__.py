from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot import get_bot
from nonebot import on_command, on_message
from nonebot.rule import to_me
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.log import logger


ping = on_command("ping", rule = to_me, priority = 5)


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

# @ping.got("check", prompt = "check")
# async def check(check: Message = Arg(), check_cmd: str = ArgPlainText("check")):
#     if check_cmd == "1":
#         return True


# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

