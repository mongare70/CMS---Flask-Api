from app import User, app, db, bcrypt
from flask import request, json, jsonify, session
from flask_login import login_user, login_required, logout_user, current_user


@app.route("/api/createUser", methods=["POST"])
def createUser():
    request_data = json.loads(request.data)
    user = User.query.filter_by(username=request_data['username']).first()
    
    if user:
      return jsonify({ "registered": False})

    else:
      hashed_password = bcrypt.generate_password_hash(request_data['password'])
      user = User(username=request_data['username'],
        email=request_data['email'],
        password=hashed_password)

      db.session.add(user)
      db.session.commit()

      return {"registered": True}

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
    return jsonify({"login": True, "username": session['username']})

  return jsonify({"login": False})


@app.route("/api/logout", methods=["GET"])
@login_required
def logout():
  logout_user()
  return jsonify({"logout": True})


@app.route("/api/editUser", methods=["POST"])
@login_required
def editUser():
  request_data = json.loads(request.data)
  user = User.query.filter_by(username=request_data['username']).first()
  if user:
    hashed_password = bcrypt.generate_password_hash(request_data['password'])
    user.firstname = request_data['firstname']
    user.lastname = request_data['lastname']
    user.email = request_data['email']
    user.password = hashed_password

    db.session.commit()

    return jsonify({"editUser": True})
  
  return jsonify({"editUser": False})


@app.route("/api/deleteUser", methods=["POST"])
@login_required
def deleteUser():
  username = json.loads(request.data)
  user = User.query.filter_by(username=username).first()

  if user:
    db.session.delete(user)
    db.session.commit()
    logout()

    return jsonify({"deleteUser": True})

  return jsonify({"deleteUser": False})


@app.route("/api/getUserData", methods=["POST"])
@login_required
def getUserData():
  username = json.loads(request.data)
  user = User.query.filter_by(username=username).first()

  if user:
    return jsonify(user.__str__())

  return jsonify({"getUserData": False})



