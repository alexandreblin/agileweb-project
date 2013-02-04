from flask import Flask, request, render_template, redirect, url_for
from model.dictionary import Dictionary
from model.game import Game
import binascii
import os

app = Flask(__name__)

games = {}

@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/test_word', methods=['GET', 'POST'])
# def test_word():
#     word = None
#     isvalid = None
#     game.getCurrentPlayer()

#     if request.method == 'POST':
#         word = request.form['word']
#         isvalid = game.addWord(word, 'a', 0, 1)
#         print "Current "
#         print game.getCurrentPlayer().id
#         print '<br>'
#         print "0: "
#         print game.getPlayer(0).score
#         print '<br>'
#         print game.getPlayer(0).words
#         print '<br>'
#         print "1: "
#         print game.getPlayer(1).score
#         print '<br>'
#         print game.getPlayer(1).words
#         print '<br>'

#     return render_template('test_word.html', word=word, valid=isvalid)


# @app.route('/word')
# def word():
#     word = None

#     print ' huy <br>'
#     game.getNumberOfPlayers()
#     num = game.getCurrentPlayer()
#     game.getNextPlayer(num.id)

#     return render_template('index.html')


@app.route('/new')
def newgame():
    # generate an ID that is not already used
    uniqueID = binascii.hexlify(os.urandom(8))
    while uniqueID in games:
        uniqueID = binascii.hexlify(os.urandom(8))

    game = Game()

    game.addPlayer("Alex")
    game.addPlayer("Tanya")

    games[uniqueID] = game

    return redirect(url_for('gameview', gameId=uniqueID))


@app.route('/game/<gameId>')
def gameview(gameId):
    if gameId not in games:
        return redirect(url_for('index'))

    game = games[gameId]

    playerInfos = []

    for player in game.players:
        playerInfos.append({
            'name': player.name,
            'score': player.score,
            'words': player.words
        })

    return render_template('game.html', gameField=game.gameField, gridSize=game.dimension, playerInfos=playerInfos)
