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
    """
    Default route, render the index page which shows a welcome message and button to create a new game
    """
    return render_template('index.html')


@app.route('/new', methods=['POST'])
def newgame():
    """
    POST action when the user clicks New game
    """

    # create a new game of the chosen dimension
    uniqueID = GameInProgress.makeNewGame(int(request.form['dimension']))

    # redirect to the game view corresponding to the newly created game
    return redirect(url_for('gameview', gameId=uniqueID))


@app.route('/game/<gameId>')
def gameview(gameId):
    """
    The main route, used to display the game to the player
    """

    if gameId not in GameInProgress.games:
        return redirect(url_for('index'))

    if 'userId' not in session:
        session['userId'] = binascii.hexlify(os.urandom(8))

    # get the GameInProgress object containing the game model and connected users
    game = GameInProgress.games[gameId]

    user = game.getCurrentUser()
    if not user:
        user = User(session['userId'])
        game.users[session['userId']] = user

    if game.model.getNumberOfPlayers() < game.model.maxPlayers and user.playerId is None:
        # if there is not yet enough player, present the Nickname choice page to the user so he can join the game
        return render_template('setname.html', gameId=gameId)

    # get the players informations from the game model
    playerInfos = []

    for player in game.model.players:
        playerInfos.append({
            'name': player.name,
            'score': player.score,
            'words': player.words
        })

    # get the last played word so we can highlight it on the board
    # it's a two dimensional array representing the grid, True values are the highlighted letters
    lastPlayed = [[False for col in row] for row in game.model.gameField]
    for letter in game.model.getLastPlayedWord():
        lastPlayed[letter.posLine][letter.posColumn] = True

    # if the game has ended, fetch the winner(s)
    if game.model.gameEnded:
        winners = [player.id for player in game.model.getWinners()]
    else:
        winners = None

    # if the user doesn't as a channel ID yet, create it
    # (it is used to dynamically send the Refresh message to the users so the game refreshes when a move is made)
    if not user.channelId:
        user.channelId = gameId + user.id + binascii.hexlify(os.urandom(8))
        user.token = channel.create_channel(user.channelId)

    # render the template with the informations
    return render_template('game.html', gameId=gameId,
                                      playerId=user.playerId,
                                     gameField=game.model.gameField,
                                    lastPlayed=lastPlayed,
                                      gridSize=game.model.dimension,
                                   playerInfos=playerInfos,
                                 currentPlayer=game.model.getCurrentPlayerId(),
                                     gameEnded=game.model.gameEnded,
                                       winners=winners,
                                         token=user.token)


@app.route('/game/<gameId>/newPlayer', methods=['POST'])
def game_newPlayer(gameId):
    """
    POST action of the Choose nickname form (presented when a user joins a game, if it's not full already)
    """

    if gameId not in GameInProgress.games:
        return redirect(url_for('index'))

    # fetch game informations
    game = GameInProgress.games[gameId]
    user = game.getCurrentUser()

    if not user or user.playerId is not None:
        return Response(status=400)

    # add the player to the game model
    playerId = game.model.addPlayer(request.form['name'])

    if playerId is False:
        # the game is full, return an error
        return Response(status=400)

    # store the player ID in the user object
    user.playerId = playerId

    # refresh the game for everyone else to show the new player
    for u in game.users.values():
        if u.channelId and u is not user:
            channel.send_message(u.channelId, 'reload')

    return redirect(url_for('gameview', gameId=gameId))


@app.route('/game/<gameId>/move', methods=['POST'])
def game_doMove(gameId):
    '''
    POST action called when a word is submitted
    '''

    if gameId not in GameInProgress.games:
        return redirect(url_for('index'))

    # get the game information
    game = GameInProgress.games[gameId]
    user = game.getCurrentUser()

    # make sure this is our turn to play
    if user.playerId == game.model.getCurrentPlayerId():
        result = None  # will contain the response code of the model

        if 'pass' in request.form:
            # player chose to pass its turn
            result = game.model.passMove()
        else:
            # player chose to add a word

            # the word is submitted as a JSON object
            # it's an array of objects representing letters
            # each object has a 'letter' attribute containing the actual letter,
            # 'x' and 'y' attributes coresponding the position on the grid

            wordJSON = json.loads(request.form['word'])

            word = []
            addedLetter = None
            for l in wordJSON:
                # convert the json word to an array of Letter object for the model
                letter = Letter(l['letter'], l['x'], l['y'])
                word.append(letter)
                if l['isAddedLetter']:
                    # this is the letter the player added
                    addedLetter = letter

            if len(word) < 2:
                flash('You must make a word', 'error')
            elif not addedLetter:
                flash('The word must contain a new letter', 'error')
            else:
                # try to add the word to the game
                result = game.model.addWord(word, addedLetter or word[0])

        if result == Game.State.SUCCESS or result == Game.State.END_OF_GAME:
            # move successful and/or game ended, refresh everyone else
            for u in game.users.values():
                if u.channelId and u is not user:
                    channel.send_message(u.channelId, 'reload')
        elif result == Game.State.ERR_UNKNOWN_WORD:
            # word not in dictionary
            flash('Unknown word', 'error')
        elif result == Game.State.ERR_ALREADY_USED:
            # word already used by another player
            flash('This word was already played', 'error')
        elif result == Game.State.ERR_WORD_IS_NOT_ON_FIELD:
            # invalid word on the grid
            flash('Invalid word placement', 'error')
    else:
        flash('This is not your turn', 'error')

    return redirect(url_for('gameview', gameId=gameId))
