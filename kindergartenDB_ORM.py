#!/usr/bin/env python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask import Flask, render_template, request, redirect, url_for, session, json

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import click

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

class Kindergarten(db.Model):
    __tablename__ = 'kindergarten'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.INTEGER)
    name = db.Column(db.String(80))
    price = db.Column(db.INTEGER)
    childs = db.relationship('Child_accounting', backref='child_accounting', lazy='dynamic')

    def __init__(self,number,name,price):
        self.number = number
        self.name = name
        self.price = price


class Month(db.Model):
    __tablename__ = 'month'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.INTEGER)
    name = db.Column(db.String(80))
    number_of_work_days = db.Column(db.INTEGER)
    report_visits = db.relationship('Report_visits', backref='report_visits', lazy='dynamic')

    def __init__(self,code,name,number_of_work_days):
        self.code = code
        self.name = name
        self.number_of_work_days = number_of_work_days

class Subdivision(db.Model):
    __tablename__ = 'subdivision'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.INTEGER)
    name = db.Column(db.String(80))
    parents = db.relationship('Parents',backref='parents',lazy='dynamic')

    def __init__(self,number,name):
        self.number = number
        self.name = name

class Report_visits(db.Model):
    __tablename__ = 'report_visits'
    id = db.Column(db.Integer, primary_key=True)
    month_id = db.Column(db.INTEGER, db.ForeignKey('month.id'))
    number_of_visiting_days = db.Column(db.INTEGER)
    child_accounting_id = db.Column(db.INTEGER, db.ForeignKey('child_accounting.id'))
    payment_sum = db.Column(db.INTEGER)
    child_accounting = db.relationship('Child_accounting',back_populates="report_visits")


    def __init__(self,month_id,number_of_visiting_days,child_accounting_id,payment_sum):
        self.month_id = month_id
        self.number_of_visiting_days = number_of_visiting_days
        self.child_accounting_id = child_accounting_id
        self.payment_sum = payment_sum

class Parents(db.Model):
    __tablename__ = 'parents'
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(80))
    name = db.Column(db.String(80))
    patronymic = db.Column(db.String(80))
    subdivision_id = db.Column(db.INTEGER, db.ForeignKey('subdivision.id'))
    childs = db.relationship('Child_accounting', backref='child_accounting2', lazy='dynamic')

    def __init__(self,surname,name,patronymic,subdivision_id):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.subdivision_id = subdivision_id


class Child_accounting(db.Model):
    __tablename__ = 'child_accounting'
    id = db.Column(db.Integer, primary_key=True)
    kindergarten_id = db.Column(db.INTEGER, db.ForeignKey('kindergarten.id'))
    parent_id = db.Column(db.INTEGER, db.ForeignKey('parents.id'))
    surname = db.Column(db.String(80))
    name = db.Column(db.String(80))
    patronymic = db.Column(db.String(80))
    payment_sum = db.Column(db.INTEGER)
    report_visits = db.relationship("Report_visits", uselist=False, back_populates="child_accounting")

    def __init__(self,kindergarten_id,parent_id,surname,name,patronymic,payment_sum):
        self.kindergarten_id = kindergarten_id
        self.parent_id = parent_id
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.payment_sum = payment_sum


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=True)

    def __init__(self, login, password):
        self.login = login
        self.password = password


    def __repr__(self):
        return '<User %r>' % self.username


if __name__ == '__main__':
    manager.run()


#db.create_all()






#admin = User('Ostap39','i44easy99lab61','admin10@example.com','dydyaStosa7')
#db.create_all() # In case user table doesn't exists already. Else remove it.
#db.session.add(admin)
#db.session.commit() # This is needed to write the changes to database
#User.query.all()
#User.query.filter_by(username='admin').first()