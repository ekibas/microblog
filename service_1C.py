from app import app, db, cli
from app.models import User, Post

'$ SET FLASK_APP=service_1C.py - укажем приложению точку входа'
# Данныый метод включает поддержку и настройку Shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

""" Скрипт добавляем пользователя в Shell
>>> u = User(username='susan', email='susan@example.com')
>>> db.session.add(u)
>>> db.session.commit() """

"""Внутренний эмулятор почтового сервера python
   запуск: python -m smtpd -n -c DebuggingServer localhost:8025
   AIL_SERVER = localhost и MAIL_PORT = 8025"""

"""Для отправки электронной почты,Flask имеет  расширение Flask-Mail, 
$ pip install flask-mail
Ссылки на сброс пароля должны содержать в себе безопасный токен. 
Чтобы сгенерировать эти токены, необходимо установить пакет JSON Web Tokens, 
(venv) $ pip install pyjwt """