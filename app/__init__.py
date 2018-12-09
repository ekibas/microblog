'В Python подкаталог, содержащий файл __init__.py, считается пакетом и может быть импортирован. '
'Мы создали пакет по названием app'
from flask import Flask
'Класс содержащий описание конфигурации Flask-приложения'
from config import Config
'Класс описывающий драйвер по работе с СУБД, в данном примере SQLLite'
from flask_sqlalchemy import SQLAlchemy
'Класс облегчающий процесс миграции данных в СУБД'
'В эти дни Alembic — намного более лучший выбор для миграции чем SQLAlchemy.'
from flask_migrate import Migrate
from flask_login import LoginManager

'__name__ -  переменная содержит имя модуля в котором она используется'
app = Flask(__name__) 
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models