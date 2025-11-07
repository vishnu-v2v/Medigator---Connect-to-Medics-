from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Doctors(db.Model):
    __tablename__="Doctors"
    id = db.Column(db.Integer,primary_key=True)

class Appointments(db.Model):
    __tablename__="Appointments"
    id = db.Column(db.Integer,primary_key=True)
    patientid = db.Column(db.Integer,unique=True)
    doctorid=db.Column(db.Integer,primary_key=True,nullable=False)
    date = db.Column(db.Integer,primary_key=True,)
    time = db.Column(db.Integer,primary_key=True)   
    status = db.Column(db.String(10))

class Treatments(db.Model):
    __tablename__="Treatments"
    id = db.Column(db.Integer,primary_key=True)
    appointmentid= db.Column(db.Integer,nullable=False,unique=True)
    diagnosis= db.Column(db.String(50))
    prescription= db.Column(db.String(50))
    Notes = db.Column(db.String(100))

class Departments(db.Model):
    __tablename__="Doctors"
    id = db.Column(db.Integer,primary_key=True)
    deptid= db.Column(db.Integer,unique=True)
    deptname=db.Column(db.String(20))
    description=db.Column(db.String(400))
    docsregistered = db.Column(db.Integer)