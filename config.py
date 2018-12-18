import os
'Абсолютный путь до директории, где лежит config.py'
'в данном примере: D:\\Repo\\Flask_WSGI_1C'
basedir = os.path.abspath(os.path.dirname(__file__))

"""   SECRET_KEY используется в качестве криптографического ключа, полезного для 
генерации подписей или токенов. Расширение Flask-WTF использует его для защиты 
веб-форм от атаки под названием Cross-Site Request Forgery или CSRF """

class Config(object):
    'Пробуем получить ключ из переменной окружения, если нет задаем явно'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTS_PER_PAGE = 3

    """Настройка данных электронной почты"""
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 8025)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['makandreev@korusconsulting.ru']