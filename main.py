from flask import Flask, request, render_template, redirect, url_for, g
from model.dictionary import Dictionary

app = Flask(__name__)

from google.appengine.ext import db
from google.appengine.api import users

@app.route('/')
def index():
	return render_template('index.html')
