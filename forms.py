from wtforms import Form,StringField,TextAreaField,PasswordField,validators,\
    BooleanField, IntegerField, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)


class LoginForm(Form):
    login = StringField('Login', [validators.Length(min=2, max=50)])
    password = PasswordField('Password', [validators.DataRequired()])
    #remember = BooleanField('remember me')

class NewChild(Form):
    parent_surname = StringField('Parent surname',[validators.Length(min=2, max=50)])
    parent_name = StringField('Parent name',[validators.Length(min=2, max=50)])
    parent_patronymic = StringField('Parent patronymic', [validators.Length(min=2, max=50)])
    child_surname = StringField('Child surname', [validators.Length(min=2, max=50)])
    child_name = StringField('Child name', [validators.Length(min=2, max=50)])
    child_patronymic = StringField('Child patronymic', [validators.Length(min=2, max=50)])
    # payment_sum = IntegerField('Payment sum')

class AddReport(Form):
    number_of_visiting_days = IntegerField('Number of visiting days')

