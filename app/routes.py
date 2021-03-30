from app import app
from flask import render_template, jsonify
from .forms import LoginRegisterForm
from flask import request
import json


# -------------------------------------------------endpoints--------------------------------------------------------- #
@app.route('/')
def index():
    form = LoginRegisterForm()
    return render_template('start.html', form=form)


# --------------------------------------------------auth------------------------------------------------------------- #
@app.route('/register', methods=['POST'])
def login_register():
    form = LoginRegisterForm()
    if request.method == 'POST':
        print(request.form.get('email'))
        return render_template('index.html')
