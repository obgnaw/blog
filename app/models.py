from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
from peewee import *
import datetime

class BaseModel(Model):
    class Meta:
        database = db

class Roles(BaseModel):
    name = CharField(null=True, unique=True)

    class Meta:
        table_name = 'roles'

class Users(UserMixin,BaseModel):
    id = IntegerField(primary_key=True)
    email = CharField(null=True, unique=True)
    password_hash = CharField(null=True)
    role = ForeignKeyField(column_name='role_id', field='id', model=Roles, null=True)
    username = CharField(null=True, unique=True)
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    class Meta:
        table_name = 'users'
# class User(UserMixin, db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(64), unique=True, index=True)
#     username = db.Column(db.String(64), unique=True, index=True)
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#     password_hash = db.Column(db.String(128))

#     @property
#     def password(self):
#         raise AttributeError('password is not a readable attribute')

#     @password.setter
#     def password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def verify_password(self, password):
#         return check_password_hash(self.password_hash, password)

#     def __repr__(self):
#         return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return Users.get_or_none(int(user_id))

class Posts(BaseModel):
    author = ForeignKeyField(column_name='author_id', field='id', model=Users, null=True)
    body = TextField()
    timestamp = DateTimeField(index=True, default=datetime.datetime.now)
    title = CharField()
    summary = TextField(null=True)
    toc = TextField(null=True)
    class Meta:
        table_name = 'posts'