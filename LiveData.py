#userdaten für binance
import userdates

#datenverwaltung
import pandas as pd
import sqlalchemy
import sqlite3

#binance anmeldung und datenbeschaffung
from binance.client import Client
from binance import BinanceSocketManager

#taskverwaltung mit zeit
import asyncio
import datetime as dt
from time import sleep


pair = 'BTCUSDT'
db = pair+'stream.db'
tableUrl = 'sqlite:///'+pair+'stream.db'
client = Client(userdates.api_key, userdates.api_secret)
bsm = BinanceSocketManager(client)
socket = bsm.trade_socket(pair)
engine = sqlalchemy.create_engine(tableUrl)

def createframe(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:,['s', 'E', 'p']]
    df.columns = ['symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df


async def main():
    time.sleep(30)

    async with socket as tscm:
        print('sammle Livedaten...')
        while True:

            res = await tscm.recv()
            if res:
                frame = createframe(res)
                frame.to_sql(pair, engine, if_exists='append', index=False)
    await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

