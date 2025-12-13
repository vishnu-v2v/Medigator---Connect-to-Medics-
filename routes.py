from app import app
from flask import render_template,request,redirect,url_for,flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
from datetime import datetime, date, timedelta

@app.route('/',methods=["GET"])
def home():
    return render_template('home.html')

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        fname =request.form['fname']
        age =request.form['age']
        gender=request.form['gender']
        height =request.form['height']
        weight =request.form['weight']


        exist_user= User.query.filter_by(username=username).first()
        if exist_user:
            #flash
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        p=User.query.filter_by(username=username).first()
        patient = Patient(user_id=p.id,fullname=fname,gender=gender,age=age,weight=weight,height=height)
        db.session.add(patient)
        db.session.commit()

        #flash
        return redirect(url_for('user_login'))
    return render_template('register.html')

@app.route('/user_login',methods=["GET","POST"])
def user_login():
    if request.method=="POST":
        email = request.form["email"]
        password = request.form["password"]

        exist_user = User.query.filter_by(email=email).first()
        if exist_user and check_password_hash(exist_user.password, password):
            if exist_user.blacklisted:
                # flash('Your account has been blacklisted. Please contact admin for further queries.', 'danger')
                return redirect(url_for('user_login'))
            #flash
            session['ua_id'] = exist_user.id
            session['username']=exist_user.username
            session['email']=exist_user.email
            session['role'] = exist_user.role
            if exist_user.role == "admin":
                return redirect(url_for('admin_dash'))
            return redirect(url_for('user_dash',username=exist_user.username))
        else:
            #flash
            return redirect(url_for('user_login'))

    return render_template("user_login.html")

@app.route('/doc_login',methods=["GET","POST"])
def doc_login():
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]

        exist_doctor = Doctor.query.filter_by(name=username).first()
        exist_user = User.query.filter_by(username=username).first()
        if exist_doctor and check_password_hash(exist_user.password, password):
            #flash
            if exist_doctor.blacklisted:
                #flash('Your account has been blacklisted. Please contact admin for further queries.', 'danger')
                return redirect(url_for('doc_login'))
            session['d_id'] = exist_doctor.id
            session['name']=exist_doctor.name
            session['deptid']=exist_doctor.deptid
            session['exp'] = exist_doctor.exp
            session['role'] = exist_user.role

            if not exist_user.role =="doc":
                #flash
                return redirect(url_for('home'))
            return redirect(url_for('doc_dash',myname=exist_doctor.name))
        else:
            #flash
            return redirect(url_for('user_login'))

    return render_template("doc_login.html")

@app.route('/admin_dash',methods=["GET","POST"])
def admin_dash():
    if 'ua_id' not in session :
        #flash
        return redirect(url_for('home'))
    
    if session.get('role') != "admin":
        #flash
        return redirect(url_for('user_dash',username=session.get('username')))
    
    update_doc_avail()
    patients = Patient.query.join(User).filter(User.role =='user').all()
    doctors = Doctor.query.all()
    appointments = Appointment.query.all()
    departments=Department.query.all()
    treatments=Treatment.query.all()
    
    total_appointments = Appointment.query.count()
    active_patients = Patient.query.count()
    doctorss = Doctor.query.count()
    

    return render_template("admin_dash.html",patients=patients,doctors=doctors,appointments=appointments,departments=departments,total_appointments=total_appointments,treatments=treatments,
        active_patients=active_patients,
        doctorss=doctorss)

@app.route('/create_dept', methods=['GET', 'POST'])
def create_dept():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["des"]
        
        exist_dept = Department.query.filter_by(name=name).first()
        if exist_dept:
            #flash
            return redirect(url_for('admin_dashboard'))
        
        department = Department(name=name, description=description, docsregistered=0)
        db.session.add(department)
        db.session.commit()
        
        # flash(f'Department {name} created successfully!', 'success')
        return redirect(url_for('admin_dash'))

@app.route('/create_doc',methods=["GET","POST"])
def create_doc():
    if request.method=="POST":
        name=request.form["name"]
        password=request.form["password"]
        des=request.form["des"]
        dept=request.form["dept"]
        exp=request.form["exp"] 
        fn=request.form['fn']
        an=request.form['an']

        exist_doc=Doctor.query.filter_by(name=name).first()
        if exist_doc:
            #flash
            return redirect(url_for('admin_dash'))
        
        user = User(username=name,password=generate_password_hash(password),role='doc')
        db.session.add(user)
        db.session.commit()
        t1 = User.query.filter_by(username=name).first()

        department=Department.query.filter_by(name=dept).first()   
        doc = Doctor(user_id=t1.id,name=name,description=des,deptid=department.id,exp=exp,fn_slots=fn,an_slots=an)
        db.session.add(doc)
        db.session.commit()
             
        #flash
        department.docsregistered+=1
        db.session.commit()

        t2 = Doctor.query.filter_by(user_id=t1.id).first()

        today = date.today()
        week = [today + timedelta(days=i) for i in range(1,8)]
        for day in week:
            doc_ava = DoctorAvailablitiy(doc_id=t2.id,date=day,cur_fn=t2.fn_slots,cur_an=t2.an_slots)
            db.session.add(doc_ava)
            db.session.commit()

        return redirect(url_for('admin_dash'))
    
@app.route('/edit_doc',methods=['GET','POST'])
def edit_doc():
    if request.method=='POST':
        name=request.form['name']
        des=request.form["des"]
        # dept=request.form["dept"]
        exp=request.form["exp"]
        fn=request.form['fn']
        an=request.form['an']

        exist_doc=Doctor.query.filter_by(name=name).first()
        if exist_doc:
            exist_doc.name=name
            exist_doc.description=des
            #exist_doc.deptid=dept
            exist_doc.exp=exp
            exist_doc.fn_slots=fn
            exist_doc.an_slots=an
            db.session.commit()
        return redirect(url_for('admin_dash'))
    return redirect(url_for('admin_dash'))

@app.route('/delete_doc',methods=['GET','POST'])
def delete_doc():
    if request.method == "POST":
        uid = request.form['uid']
        did = request.form['did']
        
        exist_doc = Doctor.query.filter_by(id=did).first()
        
        if exist_doc:
            doc_dept = Department.query.filter_by(name=exist_doc.department.name).first()
            if doc_dept:
                doc_dept.docsregistered -= 1
            DoctorAvailablitiy.query.filter_by(doc_id=did).delete()
            appointments = Appointment.query.filter_by(doctorid=did).all()
            for appt in appointments:
                Treatment.query.filter_by(appointmentid=appt.id).delete()
            Appointment.query.filter_by(doctorid=did).delete()
            
            db.session.delete(exist_doc)
            exist_user = User.query.filter_by(id=uid).first()
            if exist_user:
                db.session.delete(exist_user)
            db.session.commit()
            #flash
        #else:
            #flash
        
        return redirect(url_for('admin_dash'))
    
    return redirect(url_for('admin_dash'))

@app.route('/delete_patient', methods=['POST'])
def delete_patient():
    pid = request.form.get('pid')
    
    # Get all appointments for this patient
    appointments = Appointment.query.filter_by(patientid=pid).all()
    

    # Delete all treatments associated with these appointments
    for appointment in appointments:
        Treatment.query.filter_by(appointmentid=appointment.id).delete()
    
    # Delete all appointments for this patient
    Appointment.query.filter_by(patientid=pid).delete()
    Patient.query.filter_by(user_id=pid).delete()
    # Delete the patient
    patient = User.query.filter_by(id=pid).first()
    if patient:
        db.session.delete(patient)
        db.session.commit()
        #flash
    # else:
    #     flash
    
    return redirect(url_for('admin_dash'))

@app.route('/blacklist_doctor', methods=['POST'])
def blacklist_doctor():
    did = request.form.get('did')
    
    doctor = Doctor.query.filter_by(id=did).first()
    if doctor:
        doctor.blacklisted = True
        db.session.commit()
        #flash
    # else:
    #     flash
    
    return redirect(url_for('admin_dash'))

@app.route('/unblacklist_doctor', methods=['POST'])
def unblacklist_doctor():
    did = request.form.get('did')
    
    doctor = Doctor.query.filter_by(id=did).first()
    if doctor:
        doctor.blacklisted = False
        db.session.commit()
        #flash
    # else:
    #     flash
    
    return redirect(url_for('admin_dash'))

@app.route('/blacklist_patient', methods=['POST'])
def blacklist_patient():
    pid = request.form.get('pid')
    
    patient = User.query.filter_by(id=pid).first()
    if patient:
        patient.blacklisted = True
        db.session.commit()
        #flash
    # else:
    #     flash
    
    return redirect(url_for('admin_dash'))

@app.route('/unblacklist_patient', methods=['POST'])
def unblacklist_patient():
    pid = request.form.get('pid')
    
    patient = User.query.filter_by(id=pid).first()
    if patient:
        patient.blacklisted = False
        db.session.commit()
        #flash
    # else:
    #     #flasha
    
    return redirect(url_for('admin_dash'))

@app.route('/user_dash/<username>',methods=["GET","POST"])
def user_dash(username):
    
    if request.method=="POST":
        u_name = request.form["username"]
        em = request.form["email"]
        passw = request.form["password"]
        age = request.form["age"]
        h = request.form["height"]
        w = request.form["weight"]
        fname=request.form["fullname"]
        exist_user = User.query.filter_by(username=session.get('username')).first()
        exist_patient=Patient.query.filter_by(user_id=exist_user.id).first()
        exist_user.username=u_name
        exist_user.email = em
        if passw.strip():
            exist_user.password = generate_password_hash(passw)
        exist_patient.age=age
        exist_patient.height = h
        exist_patient.weight=w
        exist_patient.fullname=fname
        db.session.commit()
        session['username']=exist_user.username
        return redirect(url_for('user_dash',username=exist_user.username))
    if session.get('role')=="admin":
        #flash
        return redirect(url_for('admin_dash'))
    elif session.get('role')=="doc":
        return redirect(url_for('doc_dash'))
    if username!=session.get('username'):
        return redirect(url_for('user_dash',username=session.get('username')))
    
    if 'ua_id' not in session:
        #flash
        return redirect(url_for('user_login'))
    
    update_doc_avail()
    patient=Patient.query.filter_by(user_id=session.get('ua_id')).first()
    appointments=Appointment.query.filter_by(patientid=patient.id).all()
    departments=Department.query.all()
    treatments = Treatment.query.join(Appointment).filter(Appointment.patientid == patient.id).all()
    

    chart_treat = Treatment.query.join(Appointment).filter(
        Appointment.patientid == patient.id
    ).all()

    dates = [t.dou.strftime("%Y-%m-%d") for t in chart_treat]
    labels = dates
    counts = list(range(1, len(chart_treat) + 1))
    print(dates)
    print(labels)
    print(counts)
    return render_template("user_dash.html",username=username,me=patient,appointments=appointments,departments=departments,treatments=treatments,labels=labels,counts=counts)

@app.route('/user_dash/<username>/Doctors')
def user_doc(username):
    doctors = Doctor.query.all()
    return render_template('user_doc.html',doctors=doctors,username=username)

@app.route('/user_dash/<username>/<dept> ',methods=['GET','POST'])
def dept(username,dept):

    details=Department.query.filter_by(name=dept).first()
    doctor=Doctor.query.filter_by(deptid=details.id).all()

    return render_template('dept.html',username=username,doctor=doctor,details=details)

@app.route('/book',methods=['POST','GET'])
def book():
    if request.method=='POST':
        dept=request.form['dept']
        id=request.form['did']
        slot=request.form['slot_type']
        date=request.form['date']
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        
        pat=Patient.query.filter_by(user_id=session.get('ua_id')).first()
        appoint  = Appointment(patientid=pat.id,doctorid=id,date=date_obj,slot=slot)
        db.session.add(appoint)
        db.session.commit()

        cur_ava=DoctorAvailablitiy.query.filter_by(doc_id=id,date=date_obj).first()
        if slot=='FN':
            cur_ava.cur_fn-=1
        elif slot=='AN':
            cur_ava.cur_an-=1
        
        db.session.commit()
        return redirect(url_for('dept',username=session.get('username'),dept=dept))

@app.route('/doc_dash/<myname>',methods=["GET","POST"])
def doc_dash(myname):
    update_doc_avail()

    if session.get('role') != "doc":
        #flash
        return redirect(url_for('user_dash',username=session.get('username')))
    if 'd_id' not in session:
        #flash
        return redirect(url_for('home'))
    appoint=Appointment.query.filter_by(doctorid=session.get('d_id')).all()
    pids = set([a.patientid for a in appoint])
    patients = Patient.query.filter(Patient.id.in_(pids)).all()
    
    fcount = Appointment.query.filter_by(doctorid=session.get('d_id'), slot='FN').count()
    acount = Appointment.query.filter_by(doctorid=session.get('d_id'), slot='AN').count()
    print(fcount)
    print(acount)
    return render_template("doc_dash.html",me=myname,appointments=appoint,patients=patients,fcount=fcount,acount=acount)

@app.route('/update',methods=['POST'])
def update():
    if request.method=='POST':
        appid=request.form['appid']
        diag=request.form['diag']
        pres=request.form['pres']
        notes=request.form['notes']
        treat=Treatment(appointmentid=appid,diagnosis=diag,prescription=pres,notes=notes)
        db.session.add(treat)
        db.session.commit()
    return redirect(url_for('doc_dash',myname=session.get('name')))

@app.route('/mark',methods=['POST'])
def mark():
    # if session.get('role') != "doc":
    #     #flash
    #     return redirect(url_for('user_dash',username=session.get('username')))
    # if 'd_id' not in session:
    #     #flash
    #     return redirect(url_for('home'))
    
    if request.method=='POST':
        appid=request.form['appid']
        d=request.form['date']
        did=request.form['did']
        slot=request.form['slot_type']
        can=request.form['cancel']
        appoint=Appointment.query.filter_by(id=appid).first()
        davai=DoctorAvailablitiy.query.filter_by(doc_id=did,date=d).first()
        if slot in ['FN','AN']:
            appoint.status='Completed'
            # appoint.doc=date.today()
            if slot == 'FN':
                davai.cur_fn+=1
            elif slot =='AN':
                davai.cur_an+=1
            appoint.doc=date.today()
        else:
            appoint.status='Cancelled'
            # appoint.doc=date.today()
            if can == 'FN':
                davai.cur_fn+=1
            elif can =='AN':
                davai.cur_an+=1
            appoint.doc=date.today()
        db.session.commit()
        n=session.get('name')
    return redirect(url_for('doc_dash',myname=n))    

@app.route('/logout')
def logout():   
    session.clear()
    flash("You have logged out successfully...!","info")
    return redirect(url_for('home'))

def update_doc_avail():
    today = date.today()
    doctors = Doctor.query.all()
    
    for d in doctors:
        availabilities = DoctorAvailablitiy.query.filter_by(doc_id=d.id).all()

        for a in availabilities:
            if a.date < today:
                db.session.delete(a)
        
        existing_dates = {a.date for a in DoctorAvailablitiy.query.filter_by(doc_id=d.id).filter(DoctorAvailablitiy.date >= today).all()}
        
        for i in range(1, 8):
            future_date = today + timedelta(days=i)
            if future_date not in existing_dates:
                new_availability = DoctorAvailablitiy(
                    doc_id=d.id,
                    date=future_date,
                    cur_fn=d.fn_slots,
                    cur_an=d.an_slots
                )
                db.session.add(new_availability)
    db.session.commit()