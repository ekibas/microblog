"""   Данные, которые будут храниться в базе данных, будут представлены набором классов, 
называемых моделями баз данных. Уровень ORM в SQLAlchemy будет выполнять переводы, 
необходимые для сопоставления объектов, созданных из этих классов, 
в строки в соответствующих таблицах базы данных. """
from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login

followers = db.Table('followers',
        db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
        )
""" Flask-Login ожидает, что в пользовательской модели будут реализованы определенные 
свойства и методы. 
обязательные элементы:
    is_authenticated: True, если пользователь имеет действительные учетные данные.
    is_active:        True, если учетная запись Пользователя активна.
    is_anonymous:     True, если пользователь анонимный.
    get_id(): возвращает уникальный идентификатор пользователя в виде строки 

Flask-Login предоставляет mixin класс UserMixin, который включает в себя общие реализации, 
которые подходят для большинства классов пользовательских моделей.  """
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #Можно получить записи о темах пользователя
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship('User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def set_password(self, password):
            'Генерация хэш пароля пакетом Werkzeug'
            self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        'Проверка переданного пароля с хранимым хэш'
        return check_password_hash(self.password_hash, password)
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
    
    'Метод возвращает строку токена для конкретного пользователя'
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod #Статический метод может быть вызван прямо из класса
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)       
    'Метод определяет представление объектов данного класса'
    def __repr__(self):
        return '<User {}>'.format(self.username) 


""" Flask-Login отслеживает зарегистрированного пользователя, сохраняя 
его уникальный идентификатор в пользовательском сеансе Flask
Flask-Login ничего не знает о базах данных и расширение ожидает, 
что приложение настроит функцию загрузчика пользователя, 
которую можно вызвать для загрузки пользователя с идентификатором. 
Пользовательский загрузчик зарегистрирован в Flask-Login с 
помощью декоратора @login.user_loader.  """
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    #Определим внешний ключ для связи с таблицей пользователей
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

