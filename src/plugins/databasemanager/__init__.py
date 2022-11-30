from nonebot import get_driver
from tortoise import Tortoise
from nonebot.log import logger

from src.plugins.databasemanager.database import database_init, database_close


dirver = get_driver()


@dirver.on_startup
async def connect():
    await database_init()


@dirver.on_shutdown
async def disconnect():
    await database_close()

