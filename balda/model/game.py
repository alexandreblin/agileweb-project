from balda.model.dictionary import Dictionary
from balda.model.Player import Player
import math

# Class which contains logic of game
class Game(object):
	class State:
		ERR_UNKNOWN_WORD = -1
		ERR_ALREADY_USED = -2
		ERR_WORD_IS_NOT_ON_FIELD = -3
		SUCCESS =  1
		END_OF_GAME = 2

	def __init__(self, dimension = 5, maxPlayers = 2, startPlayer = 0):
		self.maxPlayers = maxPlayers # number of players
		self.passedMovement = 0 # counter of passed movement (one for all players)
		self.dimension = dimension # size of the field
		self.startPlayer = startPlayer # id og player which start game 
		self.players = [] # table of players
		self.usedWords = [] # table of used words
		self.lastWord = None # last played word
		self.gameEnded = False # true if game is finished 
		# initialise game field
		self.gameField = [[0 for x in xrange(dimension)] for x in xrange(dimension)] 
		for line in range(0, dimension):
			for col in range(0, dimension):
				self.gameField[line][col] = ''
		self.setFirstWord()

	# initialize first word 
	def setFirstWord(self):
		dictionary = Dictionary()
		# length of word is same as field size
		word = dictionary.getWord(self.dimension)
		# this word cant be used again in the game
		self.usedWords.append(word)
		wordAsList = list(word)
		line = self.dimension/2
		# put it in the middle of gamefield
		for col in range(0, self.dimension):
			self.gameField[line][col] = word[col]


	# Main function of the Game. Add played word in field.
	# Takes as argument: word as list of letters with their possitions
	# Takes as argument: new added letter with possition
	def addWord(self, obj_word, obj_letter):
		dictionary = Dictionary()
		# find out who's turn it is
		playerId = self.getCurrentPlayerId()
		word = self.getWord(obj_word)
		# Check if word is in Dictionary
		if not dictionary.isWordValid(word):
			return Game.State.ERR_UNKNOWN_WORD
		# Check if word is not used yet
		elif  word in self.usedWords:
			return Game.State.ERR_ALREADY_USED
		# Check if word contains new added letter and allowed on the field
		elif  self.isWordNotValid(obj_word, obj_letter):
			return Game.State.ERR_WORD_IS_NOT_ON_FIELD
		# if word is valid
		else:
			self.passedMovement = 0
			self.players[playerId].words.append(word)
			self.gameField[obj_letter.posLine][obj_letter.posColumn] = obj_letter.letter
			# Increase score
			self.players[playerId].score += len(word)
			self.usedWords.append(word)
			self.lastWord = obj_word
			# Verify if there is no free spots in game field, end up the game
			if self.isGameFieldComplit():
				self.endGame()
				return Game.State.END_OF_GAME
			else:
				# Pass turn to next player
				self.setCurrentPlayer(self.getNextPlayerId())
				return Game.State.SUCCESS

	# Check if there is any free spots on the field
	def isGameFieldComplit(self):
		for line in range(0, self.dimension):
			for col in range(0, self.dimension):
				if self.gameField[line][col] == '':
					return False
		return True

	# Returns Last Played Word
	def getLastPlayedWord(self):
		return self.lastWord or []

	# End up the Game
	def endGame(self):
		self.gameEnded = True
		# Set for all players isPlaying as False
		for x in range(0, self.getNumberOfPlayers()):
			self.players[x].isPlaying = False

	
	def passMove(self):
		self.passedMovement += 1
		self.lastWord = None
		# if every player passed the turs twice, game ends
		if self.passedMovement == 2*len(self.players):			
			self.endGame()
			return Game.State.END_OF_GAME
		else:
			# Pass turn to next palyer
			self.setCurrentPlayer(self.getNextPlayerId())
			return Game.State.SUCCESS


	# Verify if word contains new letter and allowed on the field
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

	# Return players who won
	def getWinners(self):
		maxScore = 0
		winners = []

		# Find out what is the best score
		for x in xrange(len(self.players)):
			if self.players[x].score > maxScore:
				maxScore = self.players[x].score

		# Find all players who has such score
		for x in xrange(len(self.players)):
			if self.players[x].score == maxScore:
				winners.append(self.players[x])

		return winners		


	# Extract String word from Object word
	def getWord(self, obj_word):
		word = ''
		for x in range(0, len(obj_word)):
			word += obj_word[x].letter
		return word

	def getCurrentPlayer(self):
		for x in range(0, self.getNumberOfPlayers()):
			if self.players[x].isPlaying == True:
				return self.players[x]

	def getCurrentPlayerId(self):
		player = self.getCurrentPlayer()
		return player.id if player else None

	def setCurrentPlayer(self, playerId):
		for x in range(0, self.getNumberOfPlayers()):
			self.players[x].isPlaying = False
		self.players[playerId].isPlaying = True

	# Find the player who is palying next
	def getNextPlayerId(self):
		playerId = self.getCurrentPlayerId()
		return (playerId+1) % self.getNumberOfPlayers()

	# Return the player by ID
	def getPlayer(self, playerId):
		return self.players[playerId]

	# Add a new Player
	def addPlayer(self, name):
		# if players table is complit 
		if self.getNumberOfPlayers == self.maxPlayers:
			return False
		else:
			player = Player(name)
			# Players id is his index number
			player.id = self.getNumberOfPlayers()
			self.players.append(player)
			# If all players joined the game set up Current player
			if self.getNumberOfPlayers() == self.maxPlayers:
				self.setCurrentPlayer(self.startPlayer)
			return player.id

	# Returns number of players who alredy joint the game
	def getNumberOfPlayers(self):
		return len(self.players)



	



	
