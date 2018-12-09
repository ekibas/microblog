"""   Данные, которые будут храниться в базе данных, будут представлены набором классов, 
называемых моделями баз данных. Уровень ORM в SQLAlchemy будет выполнять переводы, 
необходимые для сопоставления объектов, созданных из этих классов, 
в строки в соответствующих таблицах базы данных. """

from app import db, login
from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #Можно получить записи о темах пользователя
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
            self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    'Метод определяет представление объектов данного класса'
    def __repr__(self):
        return '<User {}>'.format(self.username) 

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    #Определим внешний ключ для связи с таблицей пользователей
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)