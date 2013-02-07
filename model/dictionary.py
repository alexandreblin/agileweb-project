import random
import os


class Dictionary(object):
    DICTFILE = os.path.join(os.path.dirname(__file__), '../resources/anglais.txt')

    def __init__(self):
        with open(Dictionary.DICTFILE) as f:
            self.content = f.read().splitlines()

    def isWordValid(self, word):
        if word.lower() in self.content:
            return True
        else:
            return False

    def getWord(self, length):
        words = [word for word in self.content if len(word) == length]
        ran = random.randint(0, len(words))
        return words[ran]
