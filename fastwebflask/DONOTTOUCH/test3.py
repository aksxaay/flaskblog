from main import db

db.create_all()

from main import User, Post


user_1 = User(username='Corey', email='C@demo.com', password='password')
user_2 = User(username='John', email='jd@demo.com', password='password')
db.session.add(user_1)
db.session.add(user_2)
db.session.commit()


User.query.all()



d.drop_all()