import sqlite3
import os
import alpaca_trade_api as tradeapi
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
print(symbols)
    
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url= config.API_URL) # or use ENV Vars shown below
assets = api.list_assets()

for asset in assets:
#print(asset)
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            print(f"new stock {asset.symbol}")
            cursor.execute('''INSERT INTO stock (symbol, name, exchange) VALUES (?, ?, ?)''', (asset.symbol, asset.name, asset.exchange))
    except Exception as e:
        print(e)
        print(asset.symbol)

connection.commit()