from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__="Users"
    id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False,unique=True)
    password=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(20),unique=True)
    role=db.Column(db.String(10),default="user")


class Doctor(db.Model):
    __tablename__="Doctors"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('Users.id'),unique=True,nullable=False)
    name=db.Column(db.String(20),nullable=False)
    deptid=db.Column(db.String(20),db.ForeignKey('Departments.id'),nullable=False)
    exp = db.Column(db.Integer,nullable=False)
    description = db.Column(db.String(500),nullable=False)

    user = db.relationship('User',foreign_keys=[user_id],backref='doctors')
    department = db.relationship('Department',foreign_keys=[deptid],backref='doctors')

    

class Appointment(db.Model):
    __tablename__="Appointments"
    id = db.Column(db.Integer,primary_key=True)
    patientid = db.Column(db.Integer,db.ForeignKey('Users.id'),nullable=False)
    doctorid=db.Column(db.Integer,db.ForeignKey('Doctors.id'),nullable=False)
    date = db.Column(db.Integer,nullable=False)
    time = db.Column(db.Integer,nullable=False)   
    status = db.Column(db.String(20),default="Pending")

    patient = db.relationship('User',foreign_keys=[patientid],backref='appointments')
    doctor = db.relationship('Doctor',foreign_keys=[doctorid],backref='appointments')

class Treatment(db.Model):
    __tablename__="Treatments"
    id = db.Column(db.Integer,primary_key=True)
    appointmentid= db.Column(db.Integer,db.ForeignKey('Appointments.id'),nullable=False,unique=True)
    diagnosis= db.Column(db.String(50))
    prescription= db.Column(db.String(50))
    notes = db.Column(db.String(100))

    appointment = db.relationship('Appointment',backref='treatment')

class Department(db.Model):
    __tablename__="Departments"
    id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),unique=True,nullable=False)
    description=db.Column(db.String(400))
    docsregistered = db.Column(db.Integer)