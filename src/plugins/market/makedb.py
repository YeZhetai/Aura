import sqlite3
import json
import datetime
from tortoise import Tortoise
from src.plugins.databasemanager.market_data import MarketData


async def make_db():
    with open ('marketdata.json', 'r') as f:
        data = json.load(f)
        for line in data:
            await MarketData.add_market_data(line['duration'], line['is_buy_order'], line['issued'], line['location_id'], line['min_volume'], line['order_id'], line['price'], line['range'], line['type_id'], line['volume_remain'], line['volume_total'])
    return()



# async def make_1db():


#     connect = sqlite3.connect ("robotData.db")
#     print ("Opened database successfully")
#     with open ('marketdata.json', 'r') as f:
#         data = json.load (f)
#         i = 0 
#         for line in data:
#             sql = "INSERT INTO marketData VALUES (%u, %u, '%s', '%s', %u, %u, %u, %u, '%s', %u, %u, %u)"%(i, line['duration'], line['is_buy_order'], line['issued'], line['location_id'], line['min_volume'], line['order_id'], line['price'], line['range'], line['type_id'], line['volume_remain'], line['volume_total'])
#             connect.execute (sql)
#             i = i + 1
#     connect.commit ()
#     connect.close ()
#     return()
