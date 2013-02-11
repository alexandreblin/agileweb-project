from balda.model.game import Game
from flask import session
import binascii
import os


class GameInProgress(object):
    games = {}

    @staticmethod
    def makeNewGame(dimension=None):
        # generate an ID that is not already used
        uniqueID = binascii.hexlify(os.urandom(8))
        while uniqueID in GameInProgress.games:
            uniqueID = binascii.hexlify(os.urandom(8))

        GameInProgress.games[uniqueID] = GameInProgress(dimension)

        return uniqueID

    def __init__(self, dimension):
        self.model = Game() if not dimension else Game(dimension=dimension)
        self.users = {}

    def getCurrentUser(self):
        userId = session['userId']
        return self.users[userId] if userId in self.users else None
