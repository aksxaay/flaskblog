


import sqlite3
import os




# file imports
import config

print(config.BASE_DIR)

connection = sqlite3.connect(os.path.join(config.BASE_DIR, 'app.db'))

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY, 
        symbol TEXT NOT NULL, 
        name TEXT NOT NULL,
        currency TEXT NOT NULL,
        exchange TEXT NOT NULL,
        country TEXT NOT NULL,
        type TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_price (
        id INTEGER PRIMARY KEY, 
        stock_id INTEGER,
        date NOT NULL,
        open NOT NULL, 
        high NOT NULL, 
        low NOT NULL, 
        close NOT NULL, 
         
        volume NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
    )
""")

connection.commit()