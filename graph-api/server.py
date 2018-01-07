#!/usr/bin/env python
#vim: syntax=python tabstop=2 expandtab

#---------------------------
# @author: Mahesh Vangala
# @email: vangalamaheshh@gmail.com
# @date: Jan, 5, 2018
#---------------------------

from flask import Flask, g, Response, request
import json
import os
from py2neo import Graph, Node

graph = Graph(host = "neo4j", user = "neo4j", password = os.getenv("NEO4J_PASSWORD"))
#------------------------#
#    Flask methods       #
#------------------------#
app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/CreateUser", methods = ['POST'])
def create_user():
  data = request.get_json(force = True)
  username = data["username"]
  password = data["password"]
  email = data["email"]
  results = graph.run("MATCH (a:Person {email: {email}}) return a", {"email": email}).data()
  if results:
    return json.dumps({
      "error": "{user} already exists.".format(user = username)
    }), 200
  else:
    user_node = Node("User", **{
      "email": email,
      "name": username,
      "password": password
    })
    graph.create(user_node)
    if graph.exists(user_node):
      return json.dumps({
        "error": None,
        "msg": "{user} account created.".format(user = username)
      }), 200
    else:
      return json.dumps({
        "error": "Error in creating {user} account.".format(user = username)
      }), 200


@app.route("/GetUser", methods = ['POST'])
def get_user():
  data = request.get_json(force = True)
  email = data["email"]
  results = graph.run("MATCH (a:User {email: {email}}) return a", {"email": email}).data()
  if results:
    return json.dumps({
      "error": None,
      "data": {
        "email": email,
        "password": results[0]["a"]["password"]
      }
    }), 200
  else:
    return json.dumps({
      "error": "{user} account not found".format(user = email)
    }), 200
