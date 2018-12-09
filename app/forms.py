""" Расширение Flask-WTF использует классы Python для представления веб-форм. 
Класс формы просто определяет поля формы как переменные класса. Поля, определенные 
в классе LoginForm, знают, как визуализировать себя как HTML"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')