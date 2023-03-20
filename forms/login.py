from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField('почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
    remember_me = BooleanField('Запомнить меня')
    tok_but = SubmitField('Зарегистрироваться')
