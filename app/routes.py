from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from app import app, db, login_manager, bcrypt
from flask import render_template, jsonify, redirect, make_response, request, flash, url_for
from app.forms import LoginRegisterForm, CreatePostForm, UpdatePostForm
from flask import request
from .models import User, Post
from config import Config as config
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os
from datetime import datetime, timedelta
import uuid


# -------------------------------------------------functions--------------------------------------------------------- #
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS


# -------------------------------------------------endpoints--------------------------------------------------------- #
@app.route('/')
def start():
    if current_user.is_authenticated:
        return redirect('/posts')
    return render_template('start.html')


# Главная страница для авторизованного пользователя
# @app.route('/index', methods=['POST', 'GET'])
# @login_required
# def index():
#     return render_template('index.html')


# Тест загрузки изображения на сервер
@app.route('/uploads', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(config.UPLOAD_FOLDER_IMAGES, filename))
            flash("You have successfully upload file: {}".format(filename))
            return redirect(url_for('index'))
    return render_template('uploads.html')


# Создание поста для авторизованного пользователя
@app.route('/create_post', methods=['POST', 'GET'])
@login_required
def create_post():
    form = CreatePostForm()
    if request.method == 'POST':

        if form.validate_on_submit():

            title = request.form.get('title')
            topic = request.form.get('topic')
            if request.form.get('start_event'):
                start_event = request.form.get('start_event')
            else:
                start_event = None
            if request.form.get('stop_event'):
                stop_event = request.form.get('stop_event')
            else:
                stop_event = None
            description = request.form.get('description')
            # if request.form.get('tags'):
            #     tags = request.form.get('tags')
            # else:
            #     tags = None

            # if request.files['file']:
            #     file = request.files['file']
            #     if file and allowed_file(file.filename):
            #         filename = secure_filename(file.filename)
            #         filename = str(uuid.uuid4()) + '.' + filename.split('.')[-1]
            #         picture_path = os.path.join(config.FOLDER_IMAGES, 'posts', filename)
            #         print('filename: ', filename)
            #         print('picture_path: ', picture_path)
            # else:
            #     picture_path = os.path.join(config.UPLOAD_FOLDER_IMAGES, 'no_photo.jpg')

            post = Post(
                author=current_user.email,
                title=title,
                topic=topic,
                start=start_event,
                end=stop_event,
                description=description,
                # tags=tags,
                # picture_path=picture_path
            )
            db.session.add(post)
            db.session.commit()
            # file.save(os.path.join(config.UPLOAD_FOLDER_IMAGES, 'posts', filename))
            flash("You have successfully created post: {}.".format(title))
            return redirect('/posts')
    return render_template('create_post.html', form=form)


@app.route('/delete', methods=['GET', 'POST', 'DELETE'])
@login_required
def delete_posts():
    posts = Post.query.filter_by(author=current_user.email)
    message = "List of your posts available for deletion"
    return render_template('delete_posts.html', posts=posts, message=message)


@app.route('/delete/<id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def delete_post(id):
    post = Post.query.get(id)
    title, id = post.title, post.id
    db.session.delete(post)
    db.session.commit()
    flash("You have successfully deleted post id: {}, title: {}.".format(id, title))
    return redirect('/')

# Просмотр на главной странице всех постов
@app.route('/index', methods=['POST', 'GET'])
@app.route('/posts', methods=['GET'])
@login_required
def posts_view():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


# Просмотр конкретного поста по id
@app.route('/<int:id>', methods=['GET'])
@login_required
def post(id):
    post = Post.query.filter_by(id=id).first()
    return render_template('post_view.html', post=post)


# Просмотр всех постов созданных авторизованным пользователем
@app.route('/posts_user', methods=['GET'])
@login_required
def user_posts():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    posts = user.posts
    return render_template('index.html', posts=posts)


# Просмотр поста созданного авторизованным пользователем
@app.route('/post_user', methods=['GET'])
@login_required
def user_post(id):
    # post = Post.query.filter_by(author=current_user).filter_by(id=id).first_or_404()
    post = Post.query.get(id)
    return render_template('post_view.html', post=post)


@app.route('/update', methods=['POST', 'GET'])
@login_required
def update_posts():
    posts = Post.query.filter_by(author=current_user.email)
    message = "List of your posts available for update"
    return render_template('update_posts.html', posts=posts, message=message)


@app.route('/update/<id>', methods=['POST', 'GET'])
@login_required
def update_post(id):
    post = Post.query.get(id)
    form = UpdatePostForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            title = request.form.get('title')
            topic = request.form.get('topic')
            start_event = request.form.get('start_event')
            stop_event = request.form.get('stop_event')
            description = request.form.get('description')

            if title:
                post.title = title
            if topic:
                post.topic = topic
            if start_event:
                post.start = start_event
            if stop_event:
                post.end = stop_event
            if description:
                post.description = description

            db.session.add(post)
            db.session.commit()
            flash("Post {} successfully update.".format(title))
            return redirect('/{}'.format(post.id))
    return render_template('update_post.html', post=post, form=form)


# --------------------------------------------------auth------------------------------------------------------------- #
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = LoginRegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = request.form.get('email')
            password = request.form.get('password')
            user = User(
                email=email,
                password=bcrypt.generate_password_hash(password).decode('utf-8'),
                authenticated=True
            )
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            flash("You have successfully registered")
            return redirect('/index')
            # return render_template('index.html')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginRegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.get(form.email.data)
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user, remember=True)
                    flash("you entered the site as {}".format(user.email))
                    user.authenticated = True
                    db.session.add(user)
                    db.session.commit()
                    return redirect('/posts')
                else:
                    flash("Invalid email/password", 'error')
                    return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    user = User.query.get(current_user.email)
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('start'))
