import os, csv
import secrets
from PIL import Image

from flask  import render_template, url_for, flash, redirect, request, abort, jsonify
from flaskfromscratch import app, db, bcrypt, mail
from flaskfromscratch.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flaskfromscratch.models import User, Post, Stock, Crypto
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


from binance.client import Client
from binance.enums import *

from newsapi import NewsApiClient






# stocks = [
#     {
#         'id' : 'okay',
#         'symbol' : 'okay',
#         'currency' : 'okay',
#         'exchange' : 'okay',
#         'type' : 'okay'
#     },

#     {
#         'id' : 'okay',
#         'symbol' : 'okay',
#         'currency' : 'okay',
#         'exchange' : 'okay',
#         'type' : 'okay'
#     },

#     {
#         'id' : 'okay',
#         'symbol' : 'okay',
#         'currency' : 'okay',
#         'exchange' : 'okay',
#         'type' : 'okay'
#     }
# ]

@app.route("/index")
def index():
    return render_template('index.html')



@app.route("/")
@app.route("/home")
@app.route("/blog")

def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)



@app.route("/stock")
@login_required
def stock_list():
    page = request.args.get('page', 1, type=int)
    stocks = Stock.query.order_by(Stock.id).paginate(page=page, per_page=20)
    print(stocks)
    return render_template('stock_list.html', title='Stock List',stocks=stocks)


# crypto
@app.route("/crypto")
@login_required
def crypto_list():
    page = request.args.get('page', 1, type=int)
    cryptos = Crypto.query.order_by(Crypto.id).paginate(page=page, per_page=20)
    # print(cryptos)
    return render_template('crypto_list.html', title='Crypto List',cryptos=cryptos)


@app.route("/stock/<string:stock_symbol>", methods=['GET', 'POST'])
def stock_detail(stock_symbol):
    # stock_symbol = request.args.get('stock_symbol')
    print(stock_symbol)
    # stock = Stock.query.get(stock_symbol)
    stock = Stock.query.filter_by(symbol=stock_symbol).first_or_404(description='There is no data with {}'.format(stock_symbol))
    print()
    print(stock)
    print()
    return render_template('stock_detail.html', title=stock_symbol, stock=stock)
    # return ''' <h1>The language value is: {}</h1>'''.format(stock_symbol)


@app.route("/crypto/<string:crypto_symbol>", methods=['GET', 'POST'])
def crypto_detail(crypto_symbol):
    # stock_symbol = request.args.get('stock_symbol')
    print(crypto_symbol)
    # stock = Stock.query.get(stock_symbol)
    crypto = Crypto.query.filter_by(symbol=crypto_symbol).first_or_404(description='There is no data with {}'.format(crypto_symbol))
    print()
    print(crypto)
    print()
    return render_template('crypto_detail.html', title=crypto_symbol, crypto=crypto)


# @app.route("/stocks/<string:stock_symbol>")
# def stock_detail():
#     symbol = request.args.get('symbol', 1, type=string)
#     render_template ('stock_detail.html', title=symbol)



@app.route("/about")
def about():
    return render_template('about2.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    #redirect when logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))


    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created! You are now able to login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))


    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # returns back to the page
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account credentials have been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)


    return render_template('account.html', title='Account', image_file=image_file, form=form)





# POSTS ROUTES


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='akshaykumarragavan@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token!', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

# ERROR HANDLING
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/500.html'), 590

@app.route('/history')
def history():
    sym = request.args.get('crypto_symbol')
    print(sym)
    client = Client('FULgMs4X94itKmsHtke5J7SMyb6fUPXENomyS3iE6VO0sXnrLmoc5rTOegEn5248', 'CYyhgBG0xknpS7pD1iPDigzXYTr957gV3p88aqlqPpZmDzyb8sbWCBRYv55FaU9v', tld='us')
    
    candlesticks = client.get_historical_klines(f"{sym.upper()}USDT", Client.KLINE_INTERVAL_15MINUTE, "1 Jul, 2020", "12 Jul, 2020")
    

    processed_candlesticks = []

    for data in candlesticks:
        candlestick = { 
            "time": data[0] / 1000, 
            "open": data[1],
            "high": data[2], 
            "low": data[3], 
            "close": data[4]
        }

        processed_candlesticks.append(candlestick)

    return jsonify(processed_candlesticks)


@app.route('/news')
def news():
    newsapi = NewsApiClient(api_key="6e4b61167b3942538283343ece8437c9")
    topheadlines = newsapi.get_top_headlines(sources="business-insider")


    articles = topheadlines['articles']

    desc = []
    news = []
    img = []


    for i in range(len(articles)):
        myarticles = articles[i]


        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])



    mylist = zip(news, desc, img)


    return render_template('news.html', context=mylist, title='News')
