#!/usr/bin/env python
#vim: syntax=python tabstop=2 expandtab

#---------------------------
# @author: Mahesh Vangala
# @email: vangalamaheshh@gmail.com
# @date: Jan, 5, 2018
#---------------------------

from flask import Flask, request, url_for, render_template
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
from itsdangerous import URLSafeTimedSerializer as URLSerialize
import smtplib
from email.mime.text import MIMEText
import json
import requests

def authenticate(email, password):
  url = "http://graph-api/GetUser"
  result = requests.post(url, data = json.dumps({
    "email": email
  }))
  result_dict = json.loads(result.text)
  if not result_dict["error"] and result_dict["email_confirmed"] and check_password_hash(result_dict["data"]["password"], password):
    return result_dict["data"]["email"]


def send_email(email):
  # Now we'll send the email confirmation link
  subject = "Confirm your email"
  token = ts.dumps(email, salt = 'email-confirm-key')
  confirm_url = url_for(
    'confirm_email',
    token = token,
    _external = True
  )
  msg = MIMEText(confirm_url)
  msg['Subject'] = "Confirmation email"
  msg['From'] = os.environ["GMAIL_USER"]
  msg['To'] = email
  s = smtplib.SMTP("smtp.gmail.com", 587)
  s.login(os.environ["GMAIL_USER"], os.environ["GMAIL_PASS"])
  s.send_message(msg)
  s.quit()
  return json.dumps({
    "msg": "confirmation email is sent"
  }), 200

#------------------------#
#    Flask methods       #
#------------------------#
app = Flask(__name__)
app.debug = True
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days = 1) 
ts = URLSerialize(app.config['JWT_SECRET_KEY'])
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
    #send confirmation email
    return send_email(email)


@app.route("/confirm/<token>")
def confirm_email():
  try:
    email = ts.loads(token, salt = "email-confirm-key", max_age = 86400)
  except:
    return json.dumps({
      "error": "Error confirming email account."
    }), 404
  # flip neo4j email_confirmed property to True
  url = "http://graph-api/ConfirmEmail"
  result = requests.post(url, data = json.dumps({
    "email": email
  }))
  result_dict = json.loads(result.text)
  if result_dict["error"]:
    return result
  else:
    # return success
    return json.dumps({
      "msg": "Account confirmed. Please login with credentials."
    }), 200
  

@app.route("/protected")
@jwt_required
def protected():
  email = get_jwt_identity()
  return json.dumps({
    "email": email
  }), 200
