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

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as err:
        print(err)

    return conn

def delete_old_entries(conn):
    sql = f"""DELETE FROM {pair} WHERE Time < DATETIME('now', '-2 minute')"""
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit

async def main():

    async with socket as tscm:
        t = dt.datetime.now()
        while True:

            res = await tscm.recv()
            if res:
                frame = createframe(res)
                frame.to_sql(pair, engine, if_exists='append', index=False)
                c = create_connection()
                with c:
                    delete_old_entries(c)
                delta = dt.datetime.now() - t
                if delta.seconds >= 60:
                    print(frame)
                    t = dt.datetime.now()

    await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

