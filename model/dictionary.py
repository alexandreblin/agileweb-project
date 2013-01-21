class Dictionary(object):
    DICTFILE = 'resources/anglais.txt'

    def __init__(self):
        with open(Dictionary.DICTFILE) as f:
            self.content = f.read().splitlines()

    def isWordValid(self, word):
        if word in self.content:
            return True
        else:
            return False
