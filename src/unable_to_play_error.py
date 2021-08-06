from enum import IntEnum


class PlayErrorCode(IntEnum):
    PLAYER_HAS_NOT_ENOUGH_COIN = 1
    POT_HAS_NOT_ENOUGH_COIN = 2


class UnableToPlayError(Exception):
    def __init__(self, error_code: PlayErrorCode):
        self.error_code = error_code
