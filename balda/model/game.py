from balda.model.dictionary import Dictionary
from balda.model.Player import Player
import math

class Game(object):
	class State:
		ERR_UNKNOWN_WORD = -1
		ERR_ALREADY_USED = -2
		ERR_WORD_IS_NOT_ON_FIELD = -3
		SUCCESS =  1
		END_OF_GAME = 2

	def __init__(self, dimension = 5, maxPlayers = 2, startPlayer = 0):
		self.maxPlayers = maxPlayers
		self.passedMovement = 0
		self.dimension = dimension
		self.startPlayer = startPlayer
		self.players = []
		self.usedWords = []
		self.gameField = [[0 for x in xrange(dimension)] for x in xrange(dimension)] 
		for line in range(0, dimension):
			for col in range(0, dimension):
				self.gameField[line][col] = ''
		self.setFirstWord()

	def setFirstWord(self):
		dictionary = Dictionary()
		word = dictionary.getWord(self.dimension)
		self.usedWords.append(word)
		wordAsList = list(word)
		line = self.dimension/2
		for col in range(0, self.dimension):
			self.gameField[line][col] = word[col]

	def setTestWord(self):
		testWord = 'aahed'
		self.usedWords.append(testWord)
		word = list(testWord)
		line = self.dimension/2
		for col in range(0, self.dimension):
			self.gameField[line][col] = word[col]

	def addWord(self, obj_word, obj_letter):
		dictionary = Dictionary()
		playerId = self.getCurrentPlayerId()
		word = self.getWord(obj_word)
		if not dictionary.isWordValid(word):
			return Game.State.ERR_UNKNOWN_WORD
		elif  word in self.usedWords:
			return Game.State.ERR_ALREADY_USED
		elif  self.isWordNotValid(obj_word, obj_letter):
			return Game.State.ERR_WORD_IS_NOT_ON_FIELD
		else:
			self.passedMovement = 0
			self.players[playerId].words.append(word)
			self.gameField[obj_letter.posLine][obj_letter.posColumn] = obj_letter.letter
			self.players[playerId].score += len(word)
			self.usedWords.append(word)

			if isGameFieldComplit():
				return Game.State.END_OF_GAME
			else:
				self.setCurrentPlayer(self.getNextPlayerId())
				return Game.State.SUCCESS

	def isGameFieldComplit(self):
		for line in range(0, self.dimension):
			for col in range(0, self.dimension):
				if self.gameField[line][col] == '':
					return False
		return True

	def getLastPlayedWord(self):
		return seld.usedWords[-1]
	
	def passMove(self):
		self.passedMovement += 1
		if self.passedMovement == 2*len(self.players):			
			return Game.State.END_OF_GAME
		else:
			self.setCurrentPlayer(self.getNextPlayerId())
			return Game.State.SUCCESS


	def isWordNotValid (self, obj_word, obj_letter):
		# check if the added letter is actually on a free spot
		if self.gameField[obj_letter.posLine][obj_letter.posColumn] != '':
			return True

		for i, l in enumerate(obj_word):
			# check if the other letters of the word actually are the correct letters on the grid
			if l != obj_letter and self.gameField[l.posLine][l.posColumn] != l.letter:
				return True

			# check if the letter is adjacent to the previous one
			if i > 0 and not l.isAdjacent(obj_word[i-1]):
				return True

		# check that we don't use the same letter twice
		for l1 in obj_word:
			for l2 in obj_word:
				if not l1 is l2 and l1.posColumn == l2.posColumn and l1.posLine == l2.posLine:
					return True

		return False

	def getWinners(self):
		maxScore = 0
		winners = []

		for x in xrange(len(self.players)):
			if self.players[x].score > maxScore:
				maxScore = self.players[x].score

		for x in xrange(len(self.players)):
			if self.players[x].score == maxScore:
				winners.append(self.players[x])

		return winners		


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
			if self.getNumberOfPlayers == self.maxPlayers:
				self.setCurrentPlayer(self.startPlayer)
			return self.getNumberOfPlayers()

	def getNumberOfPlayers(self):
		return len(self.players)

	def printGameField(self):
		for line in xrange(self.dimension):
			for col in xrange(self.dimension):
				print self.gameField[line][col]
			print '<br>'


	



	
