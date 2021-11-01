import userdates
import sqlalchemy
import pandas as pd
from binance.client import Client

pair = 'BTCUSDT'

client = Client(userdates.api_key, userdates.api_secret)

engine = sqlalchemy.create_engine('sqlite:///'+pair+'stream.db')

df = pd.read_sql(pair, engine)

def strategy(entry, lookback, qty, open_position=False):
	while True:
		df = pd.read_sql(pair, engine)
		lookbackperiod = df.iloc[-lookback:]
		cumret = (lookbackperiod.Price.pct_change() + 1).cumprod() - 1
		if cumret[cumret.last_valid_index()] < entry:
			order = client.create_order(symbol=pair,
										side='BUY',
										type='MARKET',
										quantity=qty)
			print(order)
			open_position = True
			break
		#TSL part from here on
	if open_position:
		while True:
			df = pd.read_sql(f"""SELECT * FROM {pair} WHERE \
			Time >= '{pd.to_datetime(order['transactTime'], unit='ms')}'""", engine)
			df['Benchmark'] = df.Price.cummax()
			df['TSL'] = df.Benchmark * 0.98
			if df[df.Price < df.TSL].first_valid_index():
				order = client.create_order(symbol=pair,
										side='SELL',
										type='MARKET',
										quantity=qty)
				print(order)
				break

while True:
    strategy(-0.0015, 60, 250)




