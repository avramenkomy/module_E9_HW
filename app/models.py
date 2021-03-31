from app import db
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask_login import LoginManager, UserMixin, current_user

Base = declarative_base()
metadata = Base.metadata


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def __repr__(self):
        return "{}".format(self.email)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, db.ForeignKey('user.email'))
    photo =
    title = db.Column(db.String)
    topic = db.Column(db.String)
    start =
    end =
    description =
    tags =
    create_date =