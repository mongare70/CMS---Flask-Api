from app import User, app, db, bcrypt
from flask import request, json

@app.route("/")
def index():
    return "<h1>Hello World</h1>"

@app.route("/api/createUser", methods=["POST"])
def createUser():

    request_data = json.loads(request.data)
    hashed_password = bcrypt.generate_password_hash(request_data['password'])
    user = User(username=request_data['username'],
      email=request_data['email'],
      password=hashed_password)

    db.session.add(user)
    db.session.commit()

    return {'201': 'User created successfully'}
