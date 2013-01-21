class Dictionary(object):
	DICTIONARY_FILE = 'anglais.txt'

	def __init__(self):
		with open(DICTIONARY_FILE) as f:
    		content = f.readlines()

	def isWordValid(self, word):
		if word in content:
			return True
		else:
			return False
