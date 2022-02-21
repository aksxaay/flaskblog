import sqlite3
import os
import twelvedata
import config




connection = sqlite3.connect(os.path.join(config.BASE_DIR, 'app.db'))
# print(os.path.join(config.BASE_DIR, 'app.db'))

connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
    SELECT symbol, name, exchange FROM stock
""")


rows = cursor.fetchall()
# print(rows)
symbols = [row['symbol'] for row in rows]
# print(symbols)


td = twelvedata.TDClient(apikey=config.API_KEY)
assets = td.get_stocks_list().as_json()

# print(assets)

for asset in assets:
#print(asset)
    try:
        if asset['symbol'] not in symbols:
            print(f"new stock {asset['symbol']}")
            cursor.execute('''INSERT INTO stock (symbol, name, currency, exchange, country, type) VALUES (?, ?, ?, ?, ?, ?)''', (asset['symbol'], asset['name'], asset['currency'], asset['exchange'], asset['country'], asset['type']))
    except Exception as e:
        print(e)
        print(asset['symbol'])

connection.commit()