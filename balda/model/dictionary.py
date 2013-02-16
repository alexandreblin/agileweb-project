import random
import os

# Class containt all interaction with a dictionary
class Dictionary(object):
    DICTFILE = os.path.join(os.path.dirname(__file__), '../resources/anglais.txt')

    def __init__(self):
        # Upload all content of dictionary to table variable
        with open(Dictionary.DICTFILE) as f:
            self.content = f.read().splitlines()

    # Verufy id dictionary contains certain word
    def isWordValid(self, word):
        if word.lower() in self.content:
            return True
        else:
            return False

    # Gets a random word from dictionary with certain length 
    def getWord(self, length):
        words = [word for word in self.content if len(word) == length]
        ran = random.randint(0, len(words))
        return words[ran]
