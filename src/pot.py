import unittest
from unable_to_play_error import UnableToPlayError, PlayErrorCode


class Pot:
    """
    Pot class to simulate pot.
    """
    def __init__(self, coin: int = 2, allow_zero_coin_draw: bool = True):
        """
        Initialize a pot.
        :param coin: initial number of coins in a pot
        """
        assert coin >= 0, "Initial amount of coins should be positive"

        self.coin = coin
        self.allow_zero_coin_draw = allow_zero_coin_draw

    def put_coin(self, amount: int):
        """
        Put coins in the pot.
        :param amount: the number of coins to put
        """
        assert amount >= 0, "Should put positive number of coins."

        self.coin += amount

    def draw_coin(self, amount: int):
        """
        Draw coins from the pot.
        :param amount: the number of coins to draw
        """
        assert amount >= 0, "Should draw positive number of coins."

        if amount == 0 and not self.allow_zero_coin_draw:
            raise UnableToPlayError(error_code=PlayErrorCode.POT_HAS_NOT_ENOUGH_COIN)

        if amount > self.coin:
            raise UnableToPlayError(error_code=PlayErrorCode.POT_HAS_NOT_ENOUGH_COIN)

        self.coin -= amount
        assert self.coin >= 0, "Remaining coins should be positive."

    def draw_half_coins(self) -> int:
        half_coins_count = self.coin // 2
        self.draw_coin(amount=half_coins_count)

        return half_coins_count

    def draw_all_coins(self) -> int:
        all_coins_count = self.coin
        self.draw_coin(amount=all_coins_count)

        return all_coins_count


class PotTest(unittest.TestCase):
    def setUp(self) -> None:
        self.pot = Pot(coin=8)

    def test_put_coin(self):
        self.pot.put_coin(amount=2)
        self.assertEqual(self.pot.coin, 10)

    def test_draw_coin(self):
        self.pot.draw_coin(amount=3)
        self.assertEqual(self.pot.coin, 5)

    def test_draw_all_coins(self):
        coins_count = self.pot.draw_all_coins()
        self.assertEqual(self.pot.coin, 0)
        self.assertEqual(coins_count, 8)

    def test_draw_half_coins(self):
        coins_count = self.pot.draw_half_coins()
        self.assertEqual(self.pot.coin, 4)
        self.assertEqual(coins_count, 4)
