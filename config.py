import os
from dotenv import load_dotenv



'Абсолютный путь до директории, где лежит config.py'
'в данном примере: D:\\Repo\\Flask_WSGI_1C'
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, 'flask.env'))

"""   SECRET_KEY используется в качестве криптографического ключа, полезного для 
генерации подписей или токенов. Расширение Flask-WTF использует его для защиты 
веб-форм от атаки под названием Cross-Site Request Forgery или CSRF """

class Config(object):
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    'Пробуем получить ключ из переменной окружения, если нет задаем явно'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTS_PER_PAGE = 10

    """Настройка данных электронной почты"""
    '''MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 8025)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['makandreev@korusconsulting.ru']'''
    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'selderey.max@gmail.com'
    MAIL_PASSWORD = 'Surface1980!'
    ADMINS = ['selderey.max@gmail.com']

    'Список поддерживаемых языков в конфигурации'
    LANGUAGES = ['en', 'ru']

    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    #set MS_TRANSLATOR_KEY=1caf2b17917d43ceab910d2cc19e9103
    ELASTICSEARCH_URL  = os.environ.get('ELASTICSEARCH_URL')
    #set ELASTICSEARCH_URL=http://localhost:9200