from model.dictionary import Dictionary
from model.Player import Player
import math

class Game(object):

	def __init__(self, dimension = 5, maxPlayers = 2):
		self.maxPlayers = maxPlayers
		self.dimension = dimension
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

	# not finished
	def addWord(self, player, word):
		dictionary = Dictionary()
		if word in self.players[player].words:
			return False
		else:
			self.players[player].words.append(word)
			print self.players[player].words
			return True

	def addPlayer(self, name):
		if self.getNumberOfPlayers == self.maxPlayers:
			return False
		else:
			player = Player(name)
			self.players.append(player)
			return self.getNumberOfPlayers()

	def getNumberOfPlayers(self):
		return len(self.players)

	def printGameField(self):
		for x in range(0, self.dimension):
			for y in range(0, self.dimension):
				print self.gameField[x][y] + ", "
			print '<br>'		

	



	
