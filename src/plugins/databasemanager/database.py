from nonebot.log import logger
from tortoise import Tortoise


async def database_init():
    logger.info("Initializing database")
    models = [
        "src.plugins.databasemanager.market_data"
        ]
    await Tortoise.init(
        db_url="sqlite://robotData.db",
        modules= {"models": models}
    )
    
    await Tortoise.generate_schemas()
    logger.info("Database initialized")


async def database_close():
    logger.info("Closing database")
    await Tortoise.close_connections()
    logger.info("Database closed")