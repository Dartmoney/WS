import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
import hashlib


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def set_password(self, password):
        self.hashed_password = hashlib.md5(bytes(password, encoding='utf-8')).hexdigest()

    def check_password(self, password):
        return self.hashed_password == hashlib.md5(bytes(password, encoding='utf-8')).hexdigest()
