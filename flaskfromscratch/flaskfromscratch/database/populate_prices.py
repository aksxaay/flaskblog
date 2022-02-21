import sqlite3, config
import time
from twelvedata import TDClient

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
cursor.execute("""
    SELECT id, symbol, name FROM stock WHERE country='United States' OR country='India'
""")
rows = cursor.fetchall()
symbols = []
stock_dict = {}
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']
print(stock_dict)
print(symbols[:20])


chunk_size = 8



td = TDClient(apikey=config.API_KEY)

# for i in range(0, len(symbols)):

# print(barsets)
# print(stock_dict[barsets['id']])

# for i in range(0, len(symbols)):

start_time = time.time()

for i in range(0, len(symbols), chunk_size):
    try:
        sample_list = symbols[i:i+chunk_size]
        ts = td.time_series(symbol=sample_list, interval="2h", outputsize=5, timezone='Asia/Kolkata').as_pandas()


        for i, val in enumerate(sample_list):
            print (i, "processing symbol,",val, "stock_id",stock_dict[val])
            cursor.execute('''INSERT INTO stock (symbol, name, currency, exchange, country, type) VALUES (?, ?, ?, ?, ?, ?)''', (ts.loc[val]['open'][0], asset['name'], asset['currency'], asset['exchange'], asset['country'], asset['type']))
        print()
        print()
        # for symbol in barsets:
        
        time.sleep(8)

    except Exception as e:
        print(e)
        print(symbol)

current_time = time.time()
elapsed_time = current_time - start_time
print()
print("Finished iterating in: " + str(int(elapsed_time))  + " seconds")
