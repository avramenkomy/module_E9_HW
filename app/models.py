from app import db
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask_login import LoginManager, UserMixin, current_user
from datetime import datetime, timedelta

Base = declarative_base()
metadata = Base.metadata


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='post_author') # lazy='author_post'

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def __repr__(self):
        return "{}".format(self.email)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, db.ForeignKey('users.email'), index=True)
    title = db.Column(db.String, index=True)
    topic = db.Column(db.String, index=True)
    start = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String, nullable=False)
    # tags = db.Column(db.ARRAY(db.String()))
    create_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    # picture_path = db.Column(db.String)
