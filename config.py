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