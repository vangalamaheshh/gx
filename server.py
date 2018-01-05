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

class User(object):
  def __init__(self, id, username, password):
    self.id = id
    self.username = username
    self.password = password

  def __str__(self):
    return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
  user = username_table.get(username, None)
  if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
    return user

def identity(payload):
  user_id = payload['identity']
  return userid_table.get(user_id, None)

#------------------------#
#    Flask methods       #
#------------------------#
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
jwt = JWT(app, authenticate, identity)

@app.route("/")
def hello():
  return "Hello World!"

@app.route('/protected')
@jwt_required()
def protected():
  return '%s' % current_identity
