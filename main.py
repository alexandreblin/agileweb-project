from flask import Flask, request, render_template, redirect, url_for, g
from model.dictionary import Dictionary

app = Flask(__name__)

from google.appengine.ext import db
from google.appengine.api import users


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test_word', methods=['GET', 'POST'])
def test_word():
    word = None
    isvalid = None

    if request.method == 'POST':
        dictionary = Dictionary('dictionary.txt')
        word = request.form['word']
        isvalid = dictionary.isWordValid(word)

    return render_template('test_word.html', word=word, valid=isvalid)
