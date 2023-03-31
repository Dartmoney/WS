from flask_wtf import FlaskForm
from wtforms import SubmitField


class Glavnaya(FlaskForm):
    RegSub = SubmitField("Регистрация")
    VhodSub = SubmitField("Вход")
