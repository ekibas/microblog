from app import app, db
from app.models import User, Post

'$ SET FLASK_APP=microblog.py - укажем приложению точку входа'
# Данныый метод включает поддержку и настройку Shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

""" Скрипт добавляем пользователя в Shell
>>> u = User(username='susan', email='susan@example.com')
>>> db.session.add(u)
>>> db.session.commit() """