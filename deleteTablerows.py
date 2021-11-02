import sqlite3

db = 'BTCUSDTstream.db'



def delete_old(db):
     conn = sqlite3.connect(db)
     c = conn.cursor()
     c.execute('DELETE FROM btcusdt;',)
     print('Entferne ', c.rowcount, ' Zeilen an alten Daten')
     conn.commit()
     conn.close()
     print('Sammle Livedaten...')



delete_old(db)