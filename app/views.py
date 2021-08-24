from app import Users, app, db, bcrypt
from flask import request, json, jsonify
from flask_cors import cross_origin

# API test route
@app.route("/api", methods=["GET", "POST"])
@cross_origin()
def apiTest():
  return "<h1>Test Success</h1>"


# User registration route
@cross_origin()
@app.route("/api/createUser", methods=["POST", "GET"])
def createUser():
    request_data = json.loads(request.data)
    user = Users.query.filter_by(username=request_data['username']).first()
    
    if user:
      return jsonify({ "registered": False})

    else:
      hashed_password = bcrypt.generate_password_hash(request_data['password']).decode('utf-8')
      user = Users(username=request_data['username'],
        email=request_data['email'],
        password=hashed_password)

      db.session.add(user)
      db.session.commit()

      return {"registered": True}


# User login route
@cross_origin()
@app.route("/api/login", methods=["POST", "GET"])
def loginUser():

    request_data = json.loads(request.data)
    user = Users.query.filter_by(username=request_data['username']).first()
    if user:
      if bcrypt.check_password_hash(user.password, request_data['password']):
        
        return jsonify({"login": True, "username": user.username})
        
    return jsonify({"login": False})
   

#Edit user firstname, lastname, and email route
@cross_origin()
@app.route("/api/editUser", methods=["POST", "GET"])
def editUser():
  request_data = json.loads(request.data)
  user = Users.query.filter_by(username=request_data['username']).first()
  if user:
    if bcrypt.check_password_hash(user.password, request_data['password']):
      user.firstname = request_data['firstname']
      user.lastname = request_data['lastname']
      user.email = request_data['email']

      db.session.commit()
      return jsonify({"editUser": True})

    else:
      return jsonify({"password": False})
    
  return jsonify({"editUser": False})

  
#Edit user password route
@cross_origin()
@app.route("/api/editUserPassword", methods=["POST", "GET"])
def editUserPassword():
  request_data = json.loads(request.data)
  user = Users.query.filter_by(username=request_data['username']).first()
  if user:
    if bcrypt.check_password_hash(user.password, request_data['oldPassword']):
      hashed_password = bcrypt.generate_password_hash(request_data['newPassword']).decode('utf-8')
      user.password = hashed_password

      db.session.commit()
      return jsonify({"editUserPassword": True})

    else:
      return jsonify({"password": False})
    
  return jsonify({"editUserPassword": False})


# Delete user route
@cross_origin()
@app.route("/api/deleteUser", methods=["POST", "GET"])
def deleteUser():
  username = json.loads(request.data)
  user = Users.query.filter_by(username=username).first()

  if user:
    db.session.delete(user)
    db.session.commit()

    return jsonify({"deleteUser": True})

  return jsonify({"deleteUser": False})


# Get user data route
@cross_origin()
@app.route("/api/getUserData", methods=["GET", "POST"])
def getUserData():
  username = json.loads(request.data)
  user = Users.query.filter_by(username=username).first()

  if user:
    return jsonify(user.__str__())

  return jsonify({"getUserData": False})



