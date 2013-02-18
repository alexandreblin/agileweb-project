from flask import Flask
import os

# initializes the application and the session cookie's private key
app = Flask(__name__)
app.secret_key = os.urandom(24)

# import the routes from the controller
import balda.controller
