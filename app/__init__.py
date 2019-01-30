'В Python подкаталог, содержащий файл __init__.py, считается пакетом и может быть импортирован. '
'Мы создали пакет по названием app'
from flask import Flask, request, current_app
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
from flask_mail import Mail
'Инициализация Bootstrap'
from flask_bootstrap import Bootstrap
'Инициализация библиотеки форматирования даты в пользовательскую локаль'
from flask_moment import Moment
'''
см. user.html
moment('2017-09-28T21:45:23Z').format('L')
"09/28/2017"
moment('2017-09-28T21:45:23Z').format('LL')
"September 28, 2017"
moment('2017-09-28T21:45:23Z').format('LLL')
"September 28, 2017 2:45 PM"
moment('2017-09-28T21:45:23Z').format('LLLL')
"Thursday, September 28, 2017 2:45 PM"
moment('2017-09-28T21:45:23Z').format('dddd')
"Thursday"
moment('2017-09-28T21:45:23Z').fromNow()
"7 hours ago"
moment('2017-09-28T21:45:23Z').calendar()
"Today at 2:45 PM"
'''
'расширение, которое упрощает работу с переводами'
from flask_babel import Babel,  lazy_gettext as _l
from elasticsearch import Elasticsearch




db = SQLAlchemy()
migrate = Migrate()
""" Flask-Login - управляет состоянием входа пользователя в систему.
Пользователи могут войти в приложение, а затем перейти на разные страницы,
пока приложение «помнит», что пользователь вошел в систему. Оно также 
предоставляет функциональность «запомнить меня», которая позволяет пользователям 
оставаться в системе даже после закрытия окна браузера. """ 
""" Flask-Login предоставляет функцию, которая заставляет пользователей регистрироваться, 
прежде чем они смогут просматривать определенные страницы. Если пользователь, который 
не выполнил вход в систему, пытается просмотреть защищенную страницу, 
Flask-Login автоматически перенаправляет пользователя в форму для входа.
Чтобы эта функция была реализована, Flask-Login должен знать, что такое функция просмотра, 
которая обрабатывает логины. """
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
'''Настройка эмулятора:
        $ python -m smtpd -n -c DebuggingServer localhost:8025
        Чтобы настроить этот сервер, необходимо установить две переменные среды:
        (venv) $ export MAIL_SERVER=localhost
        (venv) $ export MAIL_PORT=8025'''
'/__init__.py: Инициализация Flask-Bootstrap.'
bootstrap = Bootstrap()
'''Создаем экземпляр Flask-Moment. библиотека для отображения времени серверного времени 
    UTC в формате пользователя'''
moment = Moment()
babel = Babel()

def create_app(config_class=Config):
    '__name__ -  переменная содержит имя модуля в котором она используется'
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
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
        file_handler = RotatingFileHandler('logs/microblog.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')
        
    return app

'''Экземпляр Babel предоставляет декоратор localeselector. 
   Декорированная функция вызывается для каждого запроса, чтобы выбрать перевод языка для использования:'''
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

from app import models