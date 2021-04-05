import os
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'start'
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)


from app import routes, models, forms
db.create_all()