from app import app
from flask import render_template
@app.route('/',methods=["GET"])
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    return render_template('home.html')