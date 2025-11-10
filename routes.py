from app import app
from flask import render_template,request,redirect,url_for,flash
from models import *
@app.route('/',methods=["GET"])
def home():
    return render_template('home.html')

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        exist_user= User.query.filter_by(name=username).first()
        if exist_user==username:
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login',methods=["GET","POST"])
def login():
    return render_template("login.html")