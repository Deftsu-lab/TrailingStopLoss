# coding: utf-8
import userdates
import sqlalchemy
import pandas as pd
from binance.client import Client
import datetime as dt
import time
import sqlite3
import os

pair = 'BTCUSDT'

client = Client(userdates.api_key, userdates.api_secret)

engine = sqlalchemy.create_engine('sqlite:///'+pair+'stream.db')

df = pd.read_sql(pair, engine)
#Reversal Einstieg
def strategy(entry, lookback, qty, open_position=False):
	print('Warte auf neue Daten')
	time.sleep(61)
	print((f'Schaue nach nem guten Preis von {pair}'))
	while True:
		df = pd.read_sql(pair, engine)
		lookbackperiod = df.iloc[-lookback:]
		cumret = (lookbackperiod.Price.pct_change() + 1).cumprod() - 1
		try:
			if cumret[cumret.last_valid_index()] < entry:
				order = client.create_order(symbol=pair,
										side='BUY',
										type='MARKET',
										quantity=qty)
				print(order)
				open_position = True
				break
		except KeyError:
			print('Nicht genug Daten warte noch weiter...')
			time.sleep(20)
			print('Neuer Versuch...')
		#TSL part from here on
	if open_position:
		while True:
			df = pd.read_sql(f"""SELECT * FROM {pair} WHERE \
			Time >= '{pd.to_datetime(order['transactTime'], unit='ms')}'""", engine)
			df['Benchmark'] = df.Price.cummax()
			df['TSL'] = df.Benchmark * 0.96
			if df[df.Price < df.TSL].last_valid_index():
				order = client.create_order(symbol=pair,
										side='SELL',
										type='MARKET',
										quantity=qty)
				print(order)
				break

while True:
    strategy(-0.0015, 60, 0.0008)




