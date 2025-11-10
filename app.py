from flask import Flask,render_template
from werkzeug.security import generate_password_hash, check_password_hash

from models import *


app= Flask(__name__)
app.config["SECRET_KEY"] = "MyKey"
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///HMS.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
from routes import *

with app.app_context():
    db.create_all()
    if not User.query.filter_by(name="ADMIN").first():
        admin = User(
            id = 1,
            name="ADMIN",
            password = generate_password_hash("pass")
            )
        db.session.add(admin)
        db.session.commit()
        print("ADMIN CREATED!")  
    else:
        print("ADMIN EXISTS!")



if __name__ == '__main__':
    app.run(debug=True)