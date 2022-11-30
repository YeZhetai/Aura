from tortoise import fields
from tortoise.models import Model
import datetime
from nonebot.log import logger


date = datetime.date.today().strftime("%Y-%m-%d")


class MarketData(Model):
    duration = fields.IntField()
    is_buy_order = fields.BooleanField()
    issued = fields.DatetimeField()
    location_id = fields.IntField()
    min_volume = fields.IntField()
    order_id = fields.IntField()
    price = fields.FloatField()
    range = fields.CharField(max_length=255)
    type_id = fields.IntField()
    volume_remain = fields.IntField()
    volume_total = fields.IntField()
    
    class Meta:
        table = "marketdata-" + date
        table_description = "Market data from the EVE Online API"
    
    @classmethod
    async def add_market_data(cls, duration, is_buy_order, issued, location_id, min_volume, order_id, price, range, type_id, volume_remain, volume_total):
        flag, _ = await cls.get_or_create(duration=duration, is_buy_order=is_buy_order, issued=issued, location_id=location_id, min_volume=min_volume, order_id=order_id, price=price, range=range, type_id=type_id, volume_remain=volume_remain, volume_total=volume_total)
        await flag.save()

    @classmethod
    async def get_market_data(cls, type_id):
        data = await cls.filter(type_id=type_id).values("price")
        logger.debug(data)
        #logger.debug(lowest_price)
        return data
    
    # @classmethod
    # async def get_time(cls):
    #     data = await cls.
    #     return data
