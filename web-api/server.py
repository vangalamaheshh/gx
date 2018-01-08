#!/usr/bin/env python
#vim: syntax=python tabstop=2 expandtab

#---------------------------
# @author: Mahesh Vangala
# @email: vangalamaheshh@gmail.com
# @date: Jan, 5, 2018
#---------------------------

from flask import Flask, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from werkzeug.security import safe_str_cmp
import json
import requests

def authenticate(email, password):
  url = "http://graph-api/GetUser"
  result = requests.post(url, data = json.dumps({
    "email": email
  }))
  result_dict = json.loads(result.text)
  if not result_dict["error"] and safe_str_cmp(result_dict["data"]["password"].encode('utf-8'), password.encode('utf-8')):
    return result_dict["data"]["email"]

#------------------------#
#    Flask methods       #
#------------------------#
app = Flask(__name__)
app.debug = True
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
  return {
    'email': identity
  }

@app.route("/")
def hello():
  return "Hello World!"

@app.route('/protected')
@jwt_required
def protected():
  user = get_jwt_identity()
  return json.dumps({"user": user}), 200


@app.route("/CreateUser", methods = ['POST'])
def create_user():
  data = request.get_json(force = True)
  username = data["username"]
  password = data["password"]
  email = data["email"]
  url = "http://graph-api/CreateUser"
  result = requests.post(url, data = json.dumps({
    "username": username,
    "email": email,
    "password": password
  }))
  result_dict = json.loads(result.text)
  if result_dict["error"]:
    return result
  else:
    return json.dumps({
      'access_token': create_access_token(authenticate(email, password))
    }), 200

