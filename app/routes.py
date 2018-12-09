from app import app
from flask import render_template, redirect, flash, url_for, request
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

""" Декораторы связывают URL-адреса с функцией. Это означает, что когда веб-браузер
запрашивает URL-адрес, Flask будет вызывать эту функцию и передать возвращаемое
значение обратно в браузер в качестве ответа """

"""   Операция, которая преобразует шаблон в HTML-страницу, называется рендерингом.
Эта функция принимает имя файла шаблона и переменную список аргументов шаблона
и возвращает один и тот же шаблон, но при этом все заполнители в нем заменяются 
фактическими значениями.
  Функция render_template() вызывает механизм шаблонов Jinja2, который поставляется 
в комплекте с Flask. Jinja2 заменяет блоки {{...}} значениями, заданными аргументами, 
указанными в вызове render_template(), управляющие операторы, заданные внутри блоков {% ...%}. """

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'ekibas'}
    posts =[
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }, 
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]
    return render_template('index.html', title='1C:Enterprise', user=user, posts = posts)

#Показывает что обрабатывает как запросы GET так и POST
@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    'Создаем форму и передаем ее в шаблон для рендеринга'
    form = LoginForm()
    'Собирает все данные и запускает все валидаторы'
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))