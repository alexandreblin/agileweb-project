class User(object):
    """
    Class representing a user (playing or not, if a game has reached it's maximum amount of players, the other will spectate)
    """

    def __init__(self, userId):
        self.id = userId  # user's unique ID
        self.channelId = None  # the channel ID used by the Channel API to send real time information to the client
        self.token = None  # the user's JS token used by the Channel API
        self.playerId = None  # if the user is playing, used to store its ID in the game object
