from datetime import datetime
import flask
import config
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    # try to convert this into stocks
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(50), nullable=True)
    currency = db.Column(db.String(100), nullable=True)
    exchange = db.Column(db.String(10), nullable=True)
    country = db.Column(db.String(20), nullable=True)
    Type = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return f"Post('{self.id}', '{self.symbol}', '{self.type}')"




@app.route('/')
def index():
    # request: Request
    # print(request)
    # stock_filter = request.query_params.get('filter', False)
    connection = sqlite3.connect(config.DB_FILE)   
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    #     if stock_filter == 'new_closing_highs':
    #         cursor.execute("""
    #             select * from ( SELECT symbol, name, stock_id, max(close), date FROM stock_price
    #             JOIN stock on stock.id = stock_price.stock_id
    #             GROUP BY stock_id
    #             ORDER BY symbol ) WHERE date = ?

    #         """, ('2021-03-26',))
    # # date.today().isoformat()
    #     else:
    cursor.execute("""SELECT * FROM stock""")


    rows = cursor.fetchall()
    print(type(rows))
    # return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})
    return render_template('stock_list.html', stocks=rows)

if __name__ == '__main__':
    app.run(debug=True)