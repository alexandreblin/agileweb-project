from flask import Flask, request, render_template, redirect, url_for, g
from model.dictionary import Dictionary
from model.game import Game

app = Flask(__name__)

from google.appengine.ext import db
from google.appengine.api import users

game = Game()
   
game.addPlayer("Alex")
game.addPlayer("Tanya")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test_word', methods=['GET', 'POST'])
def test_word():
    word = None
    isvalid = None
    
    if request.method == 'POST':
    	word = request.form['word']
        isvalid = game.addWord(1, word)

    return render_template('test_word.html', word=word, valid=isvalid)

@app.route('/word')
def word():
    word = None
  
    game = Game()
    game.printGameField()

    return render_template('index.html')
