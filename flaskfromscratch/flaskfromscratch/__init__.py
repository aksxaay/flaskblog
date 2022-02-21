import os
from flask  import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
#  secret key for twelvedata API
# DB setup
app.config['SECRET_KEY'] = '5b42bf44132544eb99553f025eeb3779'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# make sure it is login
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'akshaykumarragavan@gmail.com'
app.config['MAIL_PASSWORD'] = '0506255975'
mail = Mail(app)

from flaskfromscratch import routes