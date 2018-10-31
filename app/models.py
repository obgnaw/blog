from peewee import *

from . import db

class BaseModel(Model):
    class Meta:
        database = db


class Roles(BaseModel):
    name = CharField(null=True, unique=True)

    class Meta:
        table_name = 'roles'

class Users(BaseModel):
    role = ForeignKeyField(column_name='role_id', field='id', model=Roles, null=True)
    username = CharField(null=True, unique=True)

    class Meta:
        table_name = 'users'

