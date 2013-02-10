from balda.model.game import Game
from flask import session
import binascii
import os


class GameInProgress(object):
    games = {}

    @staticmethod
    def makeNewGame():
        # generate an ID that is not already used
        uniqueID = binascii.hexlify(os.urandom(8))
        while uniqueID in GameInProgress.games:
            uniqueID = binascii.hexlify(os.urandom(8))

        GameInProgress.games[uniqueID] = GameInProgress()

        return uniqueID

    def __init__(self):
        self.model = Game()
        self.users = {}

    def getCurrentUser(self):
        userId = session['userId']
        return self.users[userId] if userId in self.users else None
