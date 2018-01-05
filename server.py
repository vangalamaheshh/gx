#!/usr/bin/env python
#vim: syntax=python tabstop=2 expandtab

#---------------------------
# @author: Mahesh Vangala
# @email: vangalamaheshh@gmail.com
# @date: Jan, 5, 2018
#---------------------------

from flask import Flask, request
import json

#------------------------#
#    Flask methods       #
#------------------------#
app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"
