from flask_sqlalchemy import SQLAlchemy
from datetime import date
db = SQLAlchemy()

class User(db.Model):
    __tablename__="Users"
    id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30),nullable=False,unique=True)
    password=db.Column(db.String(30),nullable=False)
    email=db.Column(db.String(30))
    role=db.Column(db.String(10),default="user")
    blacklisted = db.Column(db.Boolean, default=False)

class Patient(db.Model):
    __tablename__="Patients"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('Users.id'),unique=True,nullable=False)
    fullname = db.Column(db.String(30),nullable=False)
    gender=db.Column(db.String(10),nullable=False)
    age = db.Column(db.Integer,nullable=False)
    weight = db.Column(db.Integer,nullable=False)
    height = db.Column(db.Integer, nullable=False)

    user = db.relationship('User',foreign_keys=[user_id],backref='patient')

class Doctor(db.Model):
    __tablename__="Doctors"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('Users.id'),unique=True,nullable=False)
    name=db.Column(db.String(30),nullable=False)
    deptid=db.Column(db.Integer,db.ForeignKey('Departments.id'),nullable=False)
    exp = db.Column(db.Integer,nullable=False)
    description = db.Column(db.String(500),nullable=False)
    fn_slots = db.Column(db.Integer,nullable=False)
    an_slots = db.Column(db.Integer,nullable=False)
    blacklisted = db.Column(db.Boolean, default=False)

    user = db.relationship('User',foreign_keys=[user_id],backref='doctors')
    department = db.relationship('Department',foreign_keys=[deptid],backref='doctors')
    

class DoctorAvailablitiy(db.Model):
    __tablename__ = "DoctorAvailability"
    id = db.Column(db.Integer,primary_key=True)
    doc_id = db.Column(db.Integer,db.ForeignKey('Doctors.id'))
    date = db.Column(db.Date,nullable=False)
    cur_fn = db.Column(db.Integer,nullable=False)
    cur_an = db.Column(db.Integer,nullable=False)
    
    @property
    def is_fn(self):
        return self.cur_fn > 0
    
    @property
    def is_an(self):
        return self.cur_an > 0

    doctor = db.relationship('Doctor',backref='available')

class Appointment(db.Model):
    __tablename__="Appointments"
    id = db.Column(db.Integer,primary_key=True)
    patientid = db.Column(db.Integer,db.ForeignKey('Patients.id'),nullable=False)
    doctorid=db.Column(db.Integer,db.ForeignKey('Doctors.id'),nullable=False)
    date = db.Column(db.Date,nullable=False)
    slot = db.Column(db.String,nullable=False)  
    doc = db.Column(db.Date)
    status = db.Column(db.String(20),default="In Progress")

    patient = db.relationship('Patient',foreign_keys=[patientid],backref='appointments')
    doctor = db.relationship('Doctor',foreign_keys=[doctorid],backref='appointments')

class Treatment(db.Model):
    __tablename__="Treatments"
    id = db.Column(db.Integer,primary_key=True)
    dou=db.Column(db.Date,nullable=False,default=date.today())
    appointmentid= db.Column(db.Integer,db.ForeignKey('Appointments.id'),nullable=False)
    diagnosis = db.Column(db.String(50),default="Not Yet Diagnised")
    prescription= db.Column(db.String(50))
    notes = db.Column(db.String(100))

    appointment = db.relationship('Appointment',backref='treatment')
    
class Department(db.Model):
    __tablename__="Departments"
    id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),unique=True,nullable=False)
    description=db.Column(db.String(400))
    docsregistered = db.Column(db.Integer,default=0)