from flask_login import LoginManager, UserMixin,  login_required, login_user, current_user, logout_user
from app import app, db, login_manager, bcrypt
from flask import render_template, jsonify, redirect, make_response, request, flash, url_for
from .forms import LoginRegisterForm
from flask import request
from .models import User


# -------------------------------------------------endpoints--------------------------------------------------------- #
@app.route('/')
def start():
    if current_user.is_authenticated:
        return redirect('/index')
    return render_template('start.html')


@app.route('/index', methods=['POST', 'GET'])
@login_required
def index():
    return render_template('index.html')


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
                    user.authenticated=True
                    db.session.add(user)
                    db.session.commit()
                    return redirect('/index')
                else:
                    flash("Invalid email/password", 'error')
                    return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    user = User.query.get(current_user.email)
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('start'))
