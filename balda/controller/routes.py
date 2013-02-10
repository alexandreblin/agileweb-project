from flask import request, render_template, redirect, url_for, flash, session, Response
from balda import app
from balda.model.game import Game
from balda.model.letter import Letter
from balda.controller.user import User
from balda.controller.gameinprogress import GameInProgress
from google.appengine.api import channel
import binascii
import json
import os


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new')
def newgame():
    uniqueID = GameInProgress.makeNewGame()

    return redirect(url_for('gameview', gameId=uniqueID))


@app.route('/game/<gameId>')
def gameview(gameId):
    if gameId not in GameInProgress.games:
        return redirect(url_for('index'))

    if 'userId' not in session:
        session['userId'] = binascii.hexlify(os.urandom(8))

    game = GameInProgress.games[gameId]

    user = game.getCurrentUser()
    if not user:
        user = User(session['userId'])
        game.users[session['userId']] = user

    if game.model.getNumberOfPlayers() < game.model.maxPlayers and user.playerId is None:
        return render_template('setname.html', gameId=gameId)

    playerInfos = []

    for player in game.model.players:
        playerInfos.append({
            'name': player.name,
            'score': player.score,
            'words': player.words
        })

    if not user.channelId:
        user.channelId = gameId + user.id + binascii.hexlify(os.urandom(8))
        user.token = channel.create_channel(user.channelId)

    return render_template('game.html', gameId=gameId,
                                      playerId=user.playerId,
                                     gameField=game.model.gameField,
                                      gridSize=game.model.dimension,
                                   playerInfos=playerInfos,
                                 currentPlayer=game.model.getCurrentPlayerId(),
                                         token=user.token)


@app.route('/game/<gameId>/newPlayer', methods=['POST'])
def game_newPlayer(gameId):
    if gameId not in GameInProgress.games:
        return redirect(url_for('index'))

    game = GameInProgress.games[gameId]
    user = game.getCurrentUser()

    if not user or user.playerId is not None:
        return Response(status=400)

    playerId = game.model.addPlayer(request.form['name'])

    if playerId is False:
        return Response(status=400)

    user.playerId = playerId

    app.logger.warn(session)

    for u in game.users.values():
        if u.channelId and u is not user:
            channel.send_message(u.channelId, 'reload')

    return redirect(url_for('gameview', gameId=gameId))


@app.route('/game/<gameId>/move', methods=['POST'])
def game_doMove(gameId):
    if gameId not in GameInProgress.games:
        return redirect(url_for('index'))

    game = GameInProgress.games[gameId]
    user = game.getCurrentUser()

    if user.playerId == game.model.getCurrentPlayerId():
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
            res = game.model.addWord(word, addedLetter or word[0])

            if res == Game.State.SUCCESS:
                for u in game.users.values():
                    if u.channelId and u is not user:
                        channel.send_message(u.channelId, 'reload')
            elif res == Game.State.ERR_UNKNOWN_WORD:
                flash('Unknown word', 'error')
            elif res == Game.State.ERR_ALREADY_USED:
                flash('This word was already played', 'error')
            elif res == Game.State.ERR_WORD_IS_NOT_ON_FIELD:
                flash('Invalid word placement', 'error')
            else:
                flash('wut?', 'error')
    else:
        flash('This is not your turn', 'error')

    return redirect(url_for('gameview', gameId=gameId))
