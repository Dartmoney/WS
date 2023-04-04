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
import flask
import ws_api
from flask_restful import reqparse, abort, Api, Resource
from data.Zayavki_Resource import Zayavka_Resource, Zayavka_list_Resource

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init()
login_manager = LoginManager()
login_manager.init_app(app)
admin = Admin(app, name='microblog', template_mode='bootstrap3')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/odinochka', methods=['GET', 'POST'])
def zayavka_odin():
    if flask.session["id"]:
        form = OneForm()
        print(1)
        db_sess = db_session.create_session()
        if form.ochistit.data:
            return redirect("/odinochka")
        if form.podat.data:
            info = InformationUser(signID=flask.session["id"],
                                   name=form.name.data,
                                   surname=form.surname.data,
                                   patronymic=form.patronymic.data,
                                   phone=form.phone.data,
                                   email=form.email.data,
                                   company=form.company.data,
                                   note=form.note.data,
                                   birthday=form.birthday._value(),
                                   seriya=form.seriya.data,
                                   number=form.number.data
                                   )
            db_sess.add(info)
            db_sess.commit()
            zayavka = Solo_zayavka(
                userID=list(map(lambda x: x[0], db_sess.query(InformationUser.id).filter(
                    InformationUser.signID == flask.session["id"])))[
                    0],
                start_date=form.start._value(),
                finish_date=form.finish._value(),
                targetID=list(map(lambda x: x[0], db_sess.query(Target.id).filter(Target.title == form.target.data)))[
                    0],
                divisionID=
                list(map(lambda x: x[0], db_sess.query(Division.id).filter(Division.title == form.division.data)))[0],
                FIO_prin=form.FIO.data
            )

            db_sess.add(zayavka)
            db_sess.commit()
            return redirect("/lichniy")
        form.target.choices = list(map(lambda x: x[0], db_sess.query(Target.title).all()))
        form.division.choices = list(map(lambda x: x[0], db_sess.query(Division.title).all()))
        return render_template("odinochka.html", form=form)


@app.route('/group', methods=['GET', 'POST'])
def group():
    if flask.session["id"]:
        form = OneForm()
        print(1)
        db_sess = db_session.create_session()
        if form.ochistit.data:
            return redirect("/group")
        if form.podat.data:
            info = InformationUser(signID=flask.session["id"],
                                   name=form.name.data,
                                   surname=form.surname.data,
                                   patronymic=form.patronymic.data,
                                   phone=form.phone.data,
                                   email=form.email.data,
                                   company=form.company.data,
                                   note=form.note.data,
                                   birthday=form.birthday._value(),
                                   seriya=form.seriya.data,
                                   number=form.number.data,
                                   team=form.team.data)
            db_sess.add(info)
            db_sess.commit()
            zayavka = Solo_zayavka(
                userID=list(map(lambda x: x[0], db_sess.query(InformationUser.id).filter(
                    InformationUser.signID == flask.session["id"])))[
                    0],
                start_date=form.start._value(),
                finish_date=form.finish._value(),
                targetID=list(map(lambda x: x[0], db_sess.query(Target.id).filter(Target.title == form.target.data)))[
                    0],
                divisionID=
                list(map(lambda x: x[0], db_sess.query(Division.id).filter(Division.title == form.division.data)))[0],
                FIO_prin=form.FIO.data
            )

            db_sess.add(zayavka)
            db_sess.commit()
            return redirect("/lichniy")
        form.target.choices = list(map(lambda x: x[0], db_sess.query(Target.title).all()))
        form.division.choices = list(map(lambda x: x[0], db_sess.query(Division.title).all()))
        return render_template("group.html", form=form)


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
            flask.session["id"] = user.id
            return redirect(f"/lichniy")
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


@app.route("/lichniy")
def lichniy_kab():
    if flask.session["id"]:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == flask.session["id"]).first()
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
    app.register_blueprint(ws_api.blueprint)
    # для списка объектов
    api.add_resource(Zayavka_list_Resource, '/api/v2/zayavki')

    # для одного объекта
    api.add_resource(Zayavka_Resource, '/api/v2/news/<int:zayavka_id>')
    app.run(port=8080, host='0.0.0.0')
