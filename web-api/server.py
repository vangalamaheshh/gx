#!/usr/bin/env python
#vim: syntax=python tabstop=2 expandtab

#---------------------------
# @author: Mahesh Vangala
# @email: vangalamaheshh@gmail.com
# @date: Jan, 5, 2018
#---------------------------

from flask import Flask, request
from flask_jwt_extended import (
  JWTManager, 
  jwt_required, 
  create_access_token,
  get_jwt_identity
)
from werkzeug.security import (
  generate_password_hash,
  check_password_hash
)
from datetime import timedelta
import json
import requests

def authenticate(email, password):
  url = "http://graph-api/GetUser"
  result = requests.post(url, data = json.dumps({
    "email": email
  }))
  result_dict = json.loads(result.text)
  if not result_dict["error"] and check_password_hash(result_dict["data"]["password"], password):
    return result_dict["data"]["email"]

#------------------------#
#    Flask methods       #
#------------------------#
app = Flask(__name__)
app.debug = True
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days = 1) 
jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
  return {
    'email': identity
  }

@app.route("/")
def hello():
  return "Hello World!"

@app.route('/GetUser', methods = ["POST"])
def get_user():
  data = request.get_json(force = True)
  email = data["email"]
  password = data["password"]
  authenticated = authenticate(email, password)
  if authenticated:
    return json.dumps({
      "access_token": create_access_token(authenticated)
    }), 200
  else:
    return json.dumps({
      "error": "Authentication Failed."
    }), 401


@app.route("/CreateUser", methods = ['POST'])
def create_user():
  data = request.get_json(force = True)
  username = data["username"]
  password = data["password"]
  salted_pass = generate_password_hash(password)
  email = data["email"]
  url = "http://graph-api/CreateUser"
  result = requests.post(url, data = json.dumps({
    "username": username,
    "email": email,
    "password": salted_pass
  }))
  result_dict = json.loads(result.text)
  if result_dict["error"]:
    return result
  else:
    return json.dumps({
      'access_token': create_access_token(authenticate(email, password))
    }), 200


@app.route("/protected")
@jwt_required
def protected():
  email = get_jwt_identity()
  return json.dumps({
    "email": email
  }), 200
