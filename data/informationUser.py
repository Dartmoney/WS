import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
import hashlib


class InformationUser(SqlAlchemyBase, UserMixin):
    __tablename__ = 'InformationUser'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    patronymic = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.BIGINT, index=True, unique=True, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    company = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    note = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    birthday = sqlalchemy.Column(sqlalchemy.DATE, index=True, unique=True, nullable=False)
    seriya = sqlalchemy.Column(sqlalchemy.Integer,index=True,unique=True,nullable=False)
    number = sqlalchemy.Column(sqlalchemy.Integer,index=True,unique=True,nullable=False)
    signID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    users = orm.relationship("users")

