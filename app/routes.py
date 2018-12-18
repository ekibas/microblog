from app import app, db
from flask import render_template, redirect, flash, url_for, request
from app.forms import LoginForm, SignUpForm, EditProfileForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime

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

@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
@login_required # Flask-Login защищает функцию просмотра от анонимных пользователей
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts = current_user.followed_posts().all()
    return render_template('index.html', title='1C:Enterprise', form=form, posts = posts)

@app.route('/explore')
@login_required
def explore():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', title='Explore', posts=posts)

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
        """Необходимо определить, что URL является относительным, анализируем его с 
           помощью функции url_parse() Werkzeug, а затем проверяем, установлен ли компонент 
           netloc или нет."""
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

"""Страница профиля пользователя"""
"""Динамический компонент заключенный в скобки <>, будет передан в качестве аргумента"""
@app.route('/user/<username>')
@login_required #Будет доступна только для зарегистрированных пользователей
def user(username):
    #first_or_404() - если пользователь не найден в БД, отправляем ошибку 404
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',form=form)


"""Декоратор @before_request от Flask регистрирует декорированную функцию, 
которая должна быть выполнена непосредственно перед функцией просмотра."""
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        #db.session.add() - Эта функция не нужна
        db.session.commit()

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))