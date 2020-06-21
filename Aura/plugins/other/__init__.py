from nonebot import on_command, CommandSession
from nonebot.permission import GROUP_MEMBER
from Aura.plugins.other import get_line


@on_command('花价', permission=GROUP_MEMBER, only_to_me=False, aliases='价格')
async def market(session: CommandSession):
    item = session.get('item', prompt='请输入花的种类')
    price = await get_line(item)
    await session.send(price)


@market.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()  # 去掉消息首尾的空白符

    if session.is_first_run:
        if stripped_arg:
            session.state['item'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('花的种类不能为空，请重新输入')

    session.state[session.current_key] = stripped_arg
