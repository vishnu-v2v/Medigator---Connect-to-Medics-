from flask import Flask
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os
load_dotenv()
from models import *



app= Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"]= os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
from routes import *

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="Admin").first():
        admin = User(
            id = 1,
            username="Admin",
            email='admin@dummy.com',
            password = generate_password_hash("admin123"),
            role="admin"
            )
        db.session.add(admin)
        db.session.commit()
        print("ADMIN CREATED!")  
    else:
        print("ADMIN EXISTS!")

if __name__ == '__main__':
    app.run(debug=True)