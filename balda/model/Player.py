class Player(object):

	def __init__(self, name):

		self.name = name
		self.words = [] # Table of words used by player
		self.score = 0 
		self.isPlaying = False # if this player set up as current player
		self.id = 0
