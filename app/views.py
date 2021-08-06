from app import Users, app, db, bcrypt
from flask import request, json, jsonify
from flask_cors import cross_origin


@app.route("/api", methods=["GET", "POST"])
@cross_origin()
def apiTest():
  return "<h1>Test Success</h1>"


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


@cross_origin()
@app.route("/api/login", methods=["POST", "GET"])
def loginUser():

    request_data = json.loads(request.data)
    user = Users.query.filter_by(username=request_data['username']).first()
    if user:
      if bcrypt.check_password_hash(user.password, request_data['password']):
        
        return jsonify({"login": True, "username": user.username})
        
    return jsonify({"login": False})
   

@cross_origin()
@app.route("/api/editUser", methods=["POST", "GET"])
def editUser():
  request_data = json.loads(request.data)
  user = Users.query.filter_by(username=request_data['username']).first()
  if user:
    hashed_password = bcrypt.generate_password_hash(request_data['password']).decode('utf-8')
    user.firstname = request_data['firstname']
    user.lastname = request_data['lastname']
    user.email = request_data['email']
    user.password = hashed_password

    db.session.commit()
    return jsonify({"editUser": True})
    
  return jsonify({"editUser": False})


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


@cross_origin()
@app.route("/api/getUserData", methods=["GET", "POST"])
def getUserData():
  username = json.loads(request.data)
  user = Users.query.filter_by(username=username).first()

  if user:
    return jsonify(user.__str__())

  return jsonify({"getUserData": False})



