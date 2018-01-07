#!/usr/bin/env python
#vim: syntax=python tabstop=2 expandtab

#---------------------------
# @author: Mahesh Vangala
# @email: vangalamaheshh@gmail.com
# @date: Jan, 5, 2018
#---------------------------

from flask import Flask, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import json
import requests

def authenticate(email, password):
  url = "http://graph-api/GetUser"
  result = requests.post(url, data = json.dumps({
    "email": email
  }))
  result_dict = json.loads(result)
  if not result_dict["error"] and safe_str_cmp(result_dict["data"]["password"].encode('utf-8'), password.encode('utf-8')):
    return result_dict["data"]["email"]

def identity(payload):
  email = payload['identity']
  return {"email": email}

#------------------------#
#    Flask methods       #
#------------------------#
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_AUTH_USERNAME_KEY'] = "email"
jwt = JWT(app, authenticate, identity)

@app.route("/")
def hello():
  return "Hello World!"

@app.route('/protected')
@jwt_required()
def protected():
  return '%s' % current_identity


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
  result_dict = json.loads(result)
  if result_dict["error"]:
    return result
  else:
    return requests.post("http://localhost/auth", data = json.dumps({
      "email": email,
      "password": password
    }))


