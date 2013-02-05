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
		for line in range(0, dimension):
			for col in range(0, dimension):
				self.gameField[line][col] = '.'
		self.setFirstWord()

	def setFirstWord(self):
		dictionary = Dictionary()
		word = list(dictionary.getWord(self.dimension))
		line = self.dimension/2
		for col in range(0, self.dimension):
			self.gameField[line][col] = word[col]

	def setTestWord(self):
		testWord = 'aahed'
		word = list(testWord)
		line = self.dimension/2
		for col in range(0, self.dimension):
			self.gameField[line][col] = word[col]

	def addWord(self, obj_word, obj_letter):
		dictionary = Dictionary()
		playerId = self.getCurrentPlayerId()
		word = self.getWord(obj_word)
		if not dictionary.isWordValid(word) or word in self.getAllUsedWords() or self.isWordNotValid(obj_word, obj_letter):
			return False
		else:
			self.players[playerId].words.append(word)
			self.gameField[obj_letter.posLine][obj_letter.posColumn] = obj_letter.letter
			self.players[playerId].score += len(word)

			self.setCurrentPlayer(self.getNextPlayerId())

			return True

	def isWordNotValid (self, obj_word, obj_letter):
		for x in range(0, len(obj_word)):
			if obj_word[x].letter != self.gameField[obj_word[x].posLine][obj_word[x].posColumn] and self.gameField[obj_word[x].posLine][obj_word[x].posColumn] != '.':
				return True
			elif  obj_letter.letter != obj_word[x].letter:
				return True
		return False


	def getWord(self, obj_word):
		word = ''
		for x in range(0, len(obj_word)):
			word += obj_word[x].letter
		return word


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

	def printGameField(self):
		for line in xrange(self.dimension):
			for col in xrange(self.dimension):
				print self.gameField[line][col]
			print '<br>'


	



	
