import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
import hashlib


class Solo_zayavka(SqlAlchemyBase, UserMixin):
    __tablename__ = 'solo_zayavki'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    userID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("InformationUser.id"))
    start_date = sqlalchemy.Column(sqlalchemy.DATE, index=True, unique=True, nullable=False)
    finish_date = sqlalchemy.Column(sqlalchemy.DATE, index=True, unique=True, nullable=False)
    targetID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("target.id"))
    divisionID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("division.id"))
    FIO_prin = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    InformationUser = orm.relationship("InformationUser")
    target = orm.relationship("Target")
    division = orm.relationship("Division")
