from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager
from flask_cors import CORS
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask_mail import Mail
import os

# initialize the app 
app = Flask(__name__, static_url_path='/')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

# Mail SMTP settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'williamwanger35@gmail.com'
app.config['MAIL_PASSWORD'] = 'jxeb wzqi wibn nljh'

cors = CORS(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

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
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


    def get_token(self):
        serial=Serializer("this-really-needs-to-be-changed")
        return serial.dumps(self.id)


    @staticmethod
    def verify_token(token, expire_time=300):
        serial = Serializer("this-really-needs-to-be-changed")
        try:
            user_id = serial.loads(token, max_age=expire_time)

        except:
            return None

        return Users.query.get(user_id)


    def __str__(self):
        return {"id": self.id, "firstname": self.firstname, 
        "lastname": self.lastname, "username": self.username,
        "email": self.email}


# load the views
from app import views


