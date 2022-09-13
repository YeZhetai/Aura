from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot_plugin_rauthman import isInService
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.log import logger
from .datasource import get_character_id, call_eve_esi, esi_info_convert, data_process

character = on_command("人物", rule=None, priority=5)


@character.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    stripped_arg = args.extract_plain_text()  # 去掉消息首尾的空白符

    if stripped_arg:
        matcher.set_arg("name", args)
        logger.info("name is " + args)


@character.got("name", prompt='name not received')
async def receive(name: Message = Arg(), char_name: str = ArgPlainText("name")):
    char_id = await get_character_id(char_name)
    if char_id is None:
        logger.info("cannot find charactor.")
        await character.finish("无法找到人物，请确认名字")
    else:
        logger.info("char_id is " + char_id)
        info = await call_eve_esi(char_id)
        corporation_name, alliance_name, char, security = await esi_info_convert(info)
        logger.info(corporation_name + alliance_name + char + security)
        char_info = await data_process(corporation_name, alliance_name, char, security)
        await character.finish(char_info)





