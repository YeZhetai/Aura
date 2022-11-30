from tortoise import models
from tortoise import Tortoise, fields, run_async


class AbstractModel(models.Model):

    id = fields.IntField(pk=True)
    class Meta:
        abstract = True


class MarketData(AbstractModel):
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
        table = "marketData"

async def dbinit():
    models = [MarketData]
    await Tortoise.init(
        db_url="sqlite://robotData.db",
        modules= {"models": models}
    )
    
    await Tortoise.generate_schemas()


