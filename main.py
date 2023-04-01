from flask import Flask
from flask import render_template
from flask import redirect, request
from werkzeug.utils import secure_filename
import json
from forms.login import LoginForm
from forms.user import RegisterForm
from data import db_session
from data.user import User
from data.target import Target
from data.division import Division
from data.solo_zayavki import Solo_zayavka
from data.informationUser import InformationUser
from flask_login import LoginManager, login_user
from flask_admin import Admin
from forms.glavnaya import Glavnaya
from forms.odinochnoe import OneForm
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init()
login_manager = LoginManager()
login_manager.init_app(app)
admin = Admin(app, name='microblog', template_mode='bootstrap3')
db_sess = db_session.create_session()
for i in db_sess.query(Target).all():
    print(i)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/odinochka', methods=['GET', 'POST'])
def zayavka_odin():
    form = OneForm()
    print(1)
    if form.ochistit.data:
        return redirect("/odinochka")
    if form.podat.data:
        dicti = {"Информация о пропуске": {"начало действия заявки": form.start._value(),
                                           "конец действия заявки": form.finish._value(),
                                           "Цель посещения": form.target.data},
                 "Принимающая сторона": {"Подразделение": form.division.data,
                                         "ФИО": form.FIO.data},
                 "Информация о посетителе": {"Фамилия": form.name.data,
                                             "Имя": form.surname.data,
                                             "Отчество": form.patronymic.data,
                                             "Телефон": form.phone.data,
                                             "email": form.email.data,
                                             "Организация": form.company.data,
                                             "Примечание": form.note.data,
                                             "Дата рождения": form.birthday._value(),
                                             "Серия": form.seriya.data,
                                             "Номер": form.number.data,
                                             "Фото": form.photo.data}}
    db_sess = db_session.create_session()
    form.target.choices = db_sess.query(Target.title)
    return render_template("odinochka.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.tok_but.data:
        return redirect('/register')
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(f"/{user.email}~{user.hashed_password}")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/index')
@app.route('/', methods=['GET', 'POST'])
def glavnaya():
    Gl = Glavnaya()
    if Gl.VhodSub.data:
        return redirect("/login")
    if Gl.RegSub.data:
        return redirect("/register")
    return render_template("index.html", form=Gl)


@app.route("/<token>")
def lichniy_kab(token):
    k = token.split("~")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == k[0]).first()
    return render_template("lichniy.html", user=user)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="пользователь c takoy pochtoy уже есть")
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="пользователь c takim loginom уже есть")
        user = User(
            email=form.email.data,
            login=form.login.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
