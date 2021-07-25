from app import User, app, db, bcrypt
from flask import request, json, jsonify, session
from flask_login import login_user, login_required, logout_user, current_user

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

@app.route("/api/login", methods=["POST"])
def loginUser():

    request_data = json.loads(request.data)
    user = User.query.filter_by(username=request_data['username']).first()
    if user:
      if bcrypt.check_password_hash(user.password, request_data['password']):
        login_user(user)
        session['username'] = user.username
        return jsonify({"login": True})
        
    return jsonify({"login": False})


@app.route("/api/getsession", methods=["GET"])
def check_session():
  if current_user.is_authenticated:
    return jsonify({"username": session['username']})

  return jsonify({"login": False})


@app.route("/api/logout", methods=["GET"])
@login_required
def logout():
  logout_user()
  return jsonify({"logout": True})

