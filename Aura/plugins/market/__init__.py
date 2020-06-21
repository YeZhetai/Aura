from nonebot import on_command, CommandSession
from nonebot.permission import GROUP_MEMBER
from Aura.plugins.market.get_price import get_price


@on_command('isk', permission=GROUP_MEMBER, only_to_me=False, aliases='价格')
async def market(session: CommandSession):
    item = session.get('item', prompt='请输入物品')
    price = await get_price(item)
    await session.send(price)


@market.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()  # 去掉消息首尾的空白符

    if session.is_first_run:
        if stripped_arg:
            session.state['item'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('物品名称不能为空，请重新输入')

    session.state[session.current_key] = stripped_arg
