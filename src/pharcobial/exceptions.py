class GameException(Exception):
    """
    An exception raised in the game.
    Should be used infrequently.
    Opt for logging whenever possible.
    Only raise when critical functionality fails.
    """
