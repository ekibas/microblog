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
'Включение логера'
import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler



'__name__ -  переменная содержит имя модуля в котором она используется'
app = Flask(__name__) 
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

""" Flask-Login - управляет состоянием входа пользователя в систему.
Пользователи могут войти в приложение, а затем перейти на разные страницы,
пока приложение «помнит», что пользователь вошел в систему. Оно также 
предоставляет функциональность «запомнить меня», которая позволяет пользователям 
оставаться в системе даже после закрытия окна браузера. """ 
login = LoginManager(app)
""" Flask-Login предоставляет функцию, которая заставляет пользователей регистрироваться, 
прежде чем они смогут просматривать определенные страницы. Если пользователь, который 
не выполнил вход в систему, пытается просмотреть защищенную страницу, 
Flask-Login автоматически перенаправляет пользователя в форму для входа.
Чтобы эта функция была реализована, Flask-Login должен знать, что такое функция просмотра, 
которая обрабатывает логины. """
login.login_view = 'login'


if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    
    if not os.path.exists('logs'):
            os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

from app import routes, models, errors