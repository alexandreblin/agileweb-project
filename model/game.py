from model.dictionary import Dictionary
from model.Player import Player
import math

class Game(object):

	def __init__(self, dimension = 5, maxPlayers = 2, startPlayer = 0):
		self.maxPlayers = maxPlayers
		self.dimension = dimension
		self.startPlayer = startPlayer
		self.players = []
		self.gameField = [[0 for x in xrange(dimension)] for x in xrange(dimension)] 
		for x in range(0, dimension):
			for y in range(0, dimension):
				self.gameField[x][y] = ''
		self.setFirstWord()

	def setFirstWord(self):
		dictionary = Dictionary()
		word = list(dictionary.getWord(self.dimension))
		line = self.dimension/2
		for x in range(0, self.dimension):
			self.gameField[line][x] = word[x]

	def addWord(self, word, letter, posX, posY):
		dictionary = Dictionary()
		playerId = self.getCurrentPlayerId()
		if not dictionary.isWordValid(word) or word in self.getAllUsedWords():
			return False
		else:
			self.players[playerId].words.append(word)
			self.gameField[posY][posX] = letter
			self.players[playerId].score += len(word)

			self.setCurrentPlayer(self.getNextPlayerId())

			return True

	def getAllUsedWords(self):
		words = []
		for x in range(0, self.getNumberOfPlayers()):
			for y in range(0, len(self.players[x].words)):
				words.append(self.players[x].words[y])
		return words

	def getCurrentPlayer(self):
		for x in range(0, self.getNumberOfPlayers()):
			if self.players[x].isPlaying == True:
				return self.players[x]

	def getCurrentPlayerId(self):
			return self.getCurrentPlayer().id

	def setCurrentPlayer(self, playerId):
		for x in range(0, self.getNumberOfPlayers()):
			self.players[x].isPlaying = False
		self.players[playerId].isPlaying = True

	def getNextPlayerId(self):
		playerId = self.getCurrentPlayerId()
		return (playerId+1) % self.getNumberOfPlayers()

	def getPlayer(self, playerId):
		return self.players[playerId]

	def addPlayer(self, name):
		if self.getNumberOfPlayers == self.maxPlayers:
			return False
		else:
			player = Player(name)
			player.id = self.getNumberOfPlayers()
			self.players.append(player)
			self.setCurrentPlayer(self.startPlayer)
			return self.getNumberOfPlayers()

	def getNumberOfPlayers(self):
		return len(self.players)


	



	
