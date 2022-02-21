from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=True)
    name = db.Column(db.String(50), nullable=True)
    currency = db.Column(db.String(100), nullable=True)
    exchange = db.Column(db.String(10), nullable=True)
    country = db.Column(db.String(20), nullable=True)
    Type = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return f"Post('{self.id}', '{self.symbol}', '{self.type}')"