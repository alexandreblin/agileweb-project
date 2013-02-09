from flask import request, render_template, redirect, url_for, flash
from balda import app
from balda.model.game import Game
from balda.model.letter import Letter
import binascii
import json
import os

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
        wordJSON = json.loads(request.form['word'])

        word = []
        addedLetter = None
        for l in wordJSON:
            letter = Letter(l['letter'], l['x'], l['y'])
            word.append(letter)
            if l['isAddedLetter']:
                addedLetter = letter

        if len(word) < 2:
            flash('You must make a word', 'error')
        elif not addedLetter:
            flash('The word must contain a new letter', 'error')
        else:
            res = game.addWord(word, addedLetter or word[0])

            if res == Game.State.SUCCESS:
                flash('Yay', 'success')
            elif res == Game.State.ERR_UNKNOWN_WORD:
                flash('Unknown word', 'error')
            elif res == Game.State.ERR_ALREADY_USED:
                flash('This word was already played', 'error')
            elif res == Game.State.ERR_WORD_IS_NOT_ON_FIELD:
                flash('Invalid word placement', 'error')
            else:
                flash('wut?', 'error')

        return redirect(url_for('gameview', gameId=gameId))

    playerInfos = []

    for player in game.players:
        playerInfos.append({
            'name': player.name,
            'score': player.score,
            'words': player.words
        })

    currentPlayer = playerInfos[game.getCurrentPlayer().id] if len(playerInfos) > 0 else None

    return render_template('game.html', gameField=game.gameField, gridSize=game.dimension, playerInfos=playerInfos, currentPlayer=currentPlayer)
