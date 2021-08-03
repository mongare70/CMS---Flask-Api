from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager
import os

# initialize the app 
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(255), nullable=True)
    lastname = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # def __init__(self, firstname, lastname, username, email, password):
    #     self.firstname = firstname
    #     self.lastname = lastname
    #     self.username = username
    #     self.email = email
    #     self.password = password

    # def __repr__(self):
    #     return '<id {}>'.format(self.id)

    def __str__(self):
        return {"id": self.id, "firstname": self.firstname, 
        "lastname": self.lastname, "username": self.username,
        "email": self.email}

# load the views
from app import views


