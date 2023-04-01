from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField, StringField, IntegerField, EmailField, FileField
from wtforms.validators import DataRequired, Optional
import datetime

class OneForm(FlaskForm):
    start = DateField("начало", format='%d/%m/%Y')
    finish = DateField("конец", format='%d/%m/%Y')
    target = SelectField()
    division = SelectField()
    FIO = StringField(validators=[DataRequired()])
    surname = StringField(validators=[DataRequired()])
    name = StringField(validators=[DataRequired()])
    patronymic = StringField(validators=[DataRequired()])
    phone = StringField(validators=[DataRequired()])
    email = EmailField(validators=[DataRequired()])
    company = StringField(validators=[DataRequired()])
    note = StringField(validators=[DataRequired()])
    birthday = DateField(format='%d/%m/%Y')
    seriya = StringField(validators=[DataRequired()])
    number = StringField(validators=[DataRequired()])
    photo = FileField()
    docs = FileField()
    podat = SubmitField("офоромить заявку")
    ochistit = SubmitField("очистить заявку")
