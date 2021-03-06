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
import os
import requests

def authenticate(email, password):
  url = "http://graph-api/GetUser"
  result = requests.post(url, data = json.dumps({
    "email": email
  }))
  result_dict = json.loads(result.text)
  if not result_dict["error"] and result_dict["data"]["email_confirmed"] and check_password_hash(result_dict["data"]["password"], password):
    return result_dict["data"]["email"]


def send_email(email, url, subject_line):
  try:
    # Now we'll send the email confirmation link
    subject = "Confirm your email"
    token = ts.dumps(email, salt = 'email-confirm-key')
    confirm_url = url_for(
      url,
      token = token,
      _external = True
    )
    msg = MIMEText(confirm_url)
    subject = subject_line
    from_email = os.environ["GMAIL_USER"]
    to_email = email
    text = "\r\n".join([
      "From: " + from_email,
      "To: " + to_email,
      "Subject: " + subject,
      "",
      msg.as_string()
    ])
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.connect("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(os.environ["GMAIL_USER"], os.environ["GMAIL_PASS"])
    server.sendmail(from_email, to_email, text)
    server.quit()
    return json.dumps({
      "msg": subject_line + " is sent"
    }), 200
  except Exception as e:
    return json.dumps({
      "error": str(e)
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
    return send_email(email, 'confirm_email', 'Confirmation Email')

@app.route("/ResetUser", methods = ['POST'])
def reset_user():
  data = request.get_json(force = True)
  email = data["email"]
  url = "http://graph-api/GetUser"
  result = requests.post(url, data = json.dumps({
    "email": email
  }))
  result_dict = json.loads(result.text)
  if result_dict["error"]:
    return result
  else:
    #send confirmation email
    return send_email(email, 'reset_pass', 'Password Reset Email')


@app.route("/confirm/<token>")
def confirm_email(token):
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
  

@app.route("/reset/<token>", methods = ["POST"])
def reset_pass(token):
  data = request.get_json(force = True)
  password = data["password"]
  salted_pass = generate_password_hash(password)
  try:
    email = ts.loads(token, salt = "email-confirm-key", max_age = 86400)
  except:
    return json.dumps({
      "error": "Error confirming email account."
    }), 404
  url = "http://graph-api/ResetPass"
  result = requests.post(url, data = json.dumps({
    "email": email,
    "password": salted_pass
  }))
  result_dict = json.loads(result.text)
  if result_dict["error"]:
    return result
  else:
    # return success
    return json.dumps({
      "msg": "Password has been reset."
    }), 200


@app.route("/protected")
@jwt_required
def protected():
  email = get_jwt_identity()
  return json.dumps({
    "email": email
  }), 200
