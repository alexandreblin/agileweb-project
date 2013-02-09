from flask import Flask, request, render_template, redirect, url_for, flash
from model.game import Game
from model.letter import Letter
import binascii
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

games = {}


@app.route('/')
def index():
    return render_template('index.html')





# @app.route('/word')
# def word():
#     word = None

#     print ' huy <br>'
#     game.getNumberOfPlayers()
#     num = game.getCurrentPlayer()
#     game.getNextPlayer(num.id)

#     return render_template('index.html')


#@app.route('/test')
#def test_word():
#    game = Game()
#    game.setTestWord();
#    game.addPlayer("Alex")
#    game.addPlayer("Tanya")
#    letter1 = Letter('a', 1, 0)
#    letter2 = Letter('r', 2, 0)
#    word = []
#    word.append(letter1)
#    word.append(letter2)
#    res = game.addWord(word, letter1)
#    print res
#    print '<br>'

#    return render_template('index.html')




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


@app.route('/game/<gameId>', methods=['GET', 'POST'])
def gameview(gameId):
    if gameId not in games:
        return redirect(url_for('index'))

    game = games[gameId]

    if request.method == 'POST':
        letter = request.form['letter']
        word = request.form['word']
        x, y = int(request.form['x']), int(request.form['y'])

        if not letter:
            flash('You must put a letter', 'error')
        elif not word:
            flash('You must type a word', 'error')
        elif x < 0 or x >= game.dimension or y < 0 or y >= game.dimension:
            flash('Invalid letter position', 'error')
        else:
            if not game.addWord(word, letter, x, y):
                flash('Unknown word, or already used')

        return redirect(url_for('gameview', gameId=gameId))

    playerInfos = []

    for player in game.players:
        playerInfos.append({
            'name': player.name,
            'score': player.score,
            'words': player.words
        })

    currentPlayer = playerInfos[game.getCurrentPlayer().id]

    return render_template('game.html', gameField=game.gameField, gridSize=game.dimension, playerInfos=playerInfos, currentPlayer=currentPlayer)
