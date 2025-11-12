from app import app
from flask import render_template,request,redirect,url_for,flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
@app.route('/',methods=["GET"])
def home():
    return render_template('home.html')

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password']) 

        exist_user= User.query.filter_by(username=username).first()
        if exist_user:
            #flash
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, password=password)
        db.session.add(user)
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
            #flash
            session['ua_id'] = exist_user.id
            session['username']=exist_user.username
            session['email']=exist_user.email
            session['role'] = exist_user.role
            if exist_user.role == "admin":
                return redirect(url_for('admin_dash'))
            return redirect(url_for('user_dash'))
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
            session['d_id'] = exist_doctor.id
            session['name']=exist_doctor.name
            session['deptid']=exist_doctor.deptid
            session['exp'] = exist_doctor.exp
            session['role'] = exist_user.role
            if not exist_user.role =="doc":
                #flash
                return redirect(url_for('home'))
            return redirect(url_for('doc_dash'))
        else:
            #flash
            return redirect(url_for('user_login'))

    return render_template("doc_login.html")
@app.route('/admin_dash',methods=["GET","POST"])
def admin_dash():
    if not session.get('role') == "admin":
        #flash
        return redirect(url_for('user_dash'))
    
    if 'ua_id' not in session :
        #flash
        return redirect(url_for('home'))
    
    patients = User.query.filter_by(role='user').all()
    doctors = Doctor.query.all()
    appointments = Appointment.query.all()
    
    
    return render_template("admin_dash.html",patients=patients,doctors=doctors,appointments=appointments)

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
        department=Department.query.filter_by(name=dept).first()

        if exist_doc =="name":
            #flash
            return redirect(url_for('admin_dash'))
        
        user = User(username=name,password=generate_password_hash(password),role='doc')
        db.session.add(user)
        db.session.commit()
        temp = User.query.filter_by(username=name).first()
        doc = Doctor(user_id=temp.id,name=name,description=des,deptid=department.id,exp=exp,fn_slots=fn,an_slots=an)
        db.session.add(doc)
        db.session.commit()
        #flash
        if department:
            department.docsregistered+=1
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
    if request.method=='POST':
        uid= request.form['uid']
        did= request.form['did']
        
        exist_doc=Doctor.query.filter_by(id=did).first()
        db.session.delete(exist_doc)
        
        exist_user=User.query.filter_by(id=uid).first()
        db.session.delete(exist_user)
        db.session.commit()
        return redirect(url_for('admin_dash'))
    return redirect(url_for('admin_dash'))

@app.route('/user_dash',methods=["GET","POST"])
def user_dash():
    if session.get('role')=="admin":
        #flash
        return redirect(url_for('admin_dash'))
    elif session.get('role')=="doc":
        return redirect(url_for('doc_dash'))
    
    if 'ua_id' not in session:
        #flash
        return redirect(url_for('user_login'))
    

    return render_template("user_dash.html")

@app.route('/doc_dash',methods=["GET","POST"])
def doc_dash():
    if session.get('role') != "doc":
        #flash
        return redirect(url_for('user_dash'))
    if 'd_id' not in session:
        #flash
        return redirect(url_for('home'))
    
    
    
    return render_template("doc_dash.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))