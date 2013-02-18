from balda.model.game import Game
from flask import session
import binascii
import os


class GameInProgress(object):
    """
    This class contains the informations about a game in progress
    The 'model' attribute contains the Game model object representing the state of the game
    The 'users' attribute is an array containing the players currently following the game (players and spectator)
    """

    games = {}  # Static attribute containing all games currently in progress on the server

    @staticmethod
    def makeNewGame(dimension=None):
        """
        Helper method to make a new game of the specified size and add it to the current games in progress
        """

        # generate an ID that is not already used
        uniqueID = binascii.hexlify(os.urandom(8))
        while uniqueID in GameInProgress.games:
            uniqueID = binascii.hexlify(os.urandom(8))

        # create the game
        GameInProgress.games[uniqueID] = GameInProgress(dimension)

        return uniqueID

    def __init__(self, dimension):
        self.model = Game() if not dimension else Game(dimension=dimension)
        self.users = {}

    def getCurrentUser(self):
        """
        Gets the user object from the current session information
        """
        userId = session['userId']
        return self.users[userId] if userId in self.users else None
