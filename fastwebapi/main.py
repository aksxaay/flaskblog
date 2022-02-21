import sqlite3, config
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from datetime import date

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/dashboard")
def index(request: Request):
    # print(request)
    stock_filter = request.query_params.get('filter', False)
    connection = sqlite3.connect(config.DB_FILE)
    

    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if stock_filter == 'new_closing_highs':
        cursor.execute("""
            select * from ( SELECT symbol, name, stock_id, max(close), date FROM stock_price
            JOIN stock on stock.id = stock_price.stock_id
            GROUP BY stock_id
            ORDER BY symbol ) WHERE date = ?

        """, ('2021-03-26',))
# date.today().isoformat()
    else:
        cursor.execute("""SELECT id, symbol, name FROM stock""")


    rows = cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})
    # return {"title" : "Dashboard", "stocks" : rows}


@app.get("/stock/{symbol}")
def stock_detail(request: Request, symbol):
    connection = sqlite3.connect(config.DB_FILE)
    

    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""SELECT id, symbol, name FROM stock WHERE symbol = ?""", (symbol,))
    row = cursor.fetchone()

    cursor.execute('''SELECT * FROM stock_price WHERE stock_id = ? ORDER BY date DESC''', (row['id'],))
    prices = cursor.fetchall()

    return templates.TemplateResponse("stock_detail.html", {"request": request, "stock":row, "bars": prices})

# @app.get("/register")