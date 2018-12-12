"""   Данные, которые будут храниться в базе данных, будут представлены набором классов, 
называемых моделями баз данных. Уровень ORM в SQLAlchemy будет выполнять переводы, 
необходимые для сопоставления объектов, созданных из этих классов, 
в строки в соответствующих таблицах базы данных. """
from app import db, login
from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

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

    def set_password(self, password):
            'Генерация хэш пароля пакетом Werkzeug'
            self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        'Проверка переданного пароля с хранимым хэш'
        return check_password_hash(self.password_hash, password)
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
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

    def __repr__(self):
        return '<Post {}>'.format(self.body)