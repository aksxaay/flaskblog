import sqlite3
import os
import twelvedata
import config




connection = sqlite3.connect(os.path.join(config.BASE_DIR, 'site.db'))
# print(os.path.join(config.BASE_DIR, 'app.db'))

connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
    SELECT symbol, name, exchange FROM stock
""")


rows = cursor.fetchall()
# print(rows)
# symbols = [row['symbol'] for row in rows]
# print(symbols)

symbols = [
    'LUV',
'JPM',
'MSFT',
'GM',
'AAPL',
'AMZN',
'MCD',
'HOG',
'WFC',
'JNJ',
'WMT',
'DIS',
'ADBE',
'INTC',
'KO',
'NFLX',
'PFE',
'TM',
'PEP',
'ACN',
'TXN',
'COST',
'C',
'MS',
'PM',
'UL',
'BA',
'SBUX',
'RY',
'SONY',
'IBM',
'HSBC',
'JD',
'GE',
'UBER',
'ABNB',
'MU',
'CVS',
'SNAP',
'INFY',
'DELL',
'CNI',
'FDX',
'NSC',
'ADSK',
'HCA',
'SNP',
'BMO',
'IBN',
'SPOT',
'NOC',
'RACE',
'TWTR',
'VOD',
'HMC',
'F',
'PINS',
'MAR',
'BCS',
'HPQ',
'EBAY',
'DD',
'WIT',
'SNPS',
'GIS',
'HLT',
'PSX',
'LU',
'W',
'WMB',
'KSU',
'NET',
'NDAQ',
'DB',
'SIRI',
'EXPE',
'WDC',
'SKM',
'MDB',
'ESS',
'DISCA',
'TW',
'J',
'CINF',
'VICI',
'UAL',
'EMN',
'DPZ',
'TTM',
'GDDY',
'BSY',
'CHGG',
'APO',
'SID',
'RE',
'DLB',
'AXON',
'RS'
]

td = twelvedata.TDClient(apikey=config.API_KEY)
# assets = td.get_stocks_list().as_json()

crypto_assets = td.get_cryptocurrencies_list().as_json()

# print(assets)

# for asset in assets:
#print(asset)
    # try:
    #     if asset['symbol'] in symbols:
    #         if (asset['exchange'] == 'NASDAQ') or (asset['exchange'] == 'NYSE'):
    #             print(f"new stock {asset['symbol']}")
    #             cursor.execute('''INSERT INTO stock (symbol, name, currency, exchange, country, type) VALUES (?, ?, ?, ?, ?, ?)''', (asset['symbol'], asset['name'], asset['currency'], asset['exchange'], asset['country'], asset['type']))
    # except Exception as e:


try:
    for crypto in crypto_assets:
        if crypto['currency_quote'] == 'US Dollar':
            print(f"new crypto asset {crypto['symbol']}")
            cursor.execute('''INSERT INTO crypto (symbol, name, currency, exchange, country, type) VALUES (?, ?, ?, ?, ?, ?)''', (crypto['symbol'].split('/')[0], crypto['currency_base'], crypto['currency_quote'], crypto['available_exchanges'][0], 'International', 'Crpyto'))

except Exception as e:
    print(e)
    print(crypto['symbol'])
        









connection.commit()