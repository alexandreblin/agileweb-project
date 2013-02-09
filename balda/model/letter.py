class Letter(object):

    def __init__(self, letter, posLine, posColumn):
        self.letter = letter
        self.posLine = posLine
        self.posColumn = posColumn

    def isAdjacent(self, other):
        return abs(self.posLine - other.posLine) <= 1 and abs(self.posColumn - other.posColumn) <= 1

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__

        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)

        if result is NotImplemented:
            return result

        return not result

    def __str__(self):
        return 'Letter "%s" (%d, %d)' % (self.letter, self.posLine, self.posColumn)
