from flask.helpers import url_for
from app import Users, app, db, bcrypt, mail
from flask import request, json, jsonify
from flask_cors import cross_origin
from flask_mail import Message

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
      return jsonify({ "username": False})

    user2 = Users.query.filter_by(email=request_data['email']).first()

    if user2:
      return jsonify({ "email": False})

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


def send_mail(user):
  token = user.get_token()
  msg = Message('Password Reset Request', recipients=[user.email], sender='noreply@cms.com')
  msg.body=f""" To reset your password. Please click the link below.

  {'http://localhost:3000/reset_password/{}'.format(token)}

  This link will expire in 5 minutes.
  If you didn't send a password reset request. Please ignore this message.

  
  """

  try:
        mail.send(msg)
        return jsonify({"sent": True})
  except:
      return jsonify({"sent": False})


# Reset Password route
@cross_origin()
@app.route("/api/reset_password", methods=["GET", "POST"])
def reset_password_request():
  email = json.loads(request.data)
  user = Users.query.filter_by(email=email).first()

  if user:
    send_mail(user)
    return jsonify({"password_reset": True})

  return jsonify({"reset": False})


# Reset Password token route
@cross_origin()
@app.route("/api/reset_password_form/<token>", methods=["GET", "POST"])
def reset_password_token(token):
  user=Users.verify_token(token)
  if user is None:
    return jsonify({"reset": False})

  password =  json.loads(request.data)
  hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
  user.password = hashed_password

  db.session.commit()
  return jsonify({"reset": True})
