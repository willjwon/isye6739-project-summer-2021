import random
import unittest
from typing import Optional
from pot import Pot
from unable_to_play_error import UnableToPlayError, PlayErrorCode


class Player:
    def __init__(self, id: int, coin: int, coin_put_amount: int, pot: Pot, verbose: bool):
        self.id = id
        self.coin = coin
        self.coin_put_amount = coin_put_amount
        self.pot = pot
        self.verbose = verbose
    
    def print_log(self, message = None) -> None:
        if self.verbose:
            print(message)

    def draw_all_coins(self) -> None:
        coins_count = self.pot.draw_all_coins()
        self.coin += coins_count

    def draw_half_coins(self) -> None:
        coins_count = self.pot.draw_half_coins()
        self.coin += coins_count

    def put_coin_in_pot(self, amount: int) -> None:
        assert amount >= 0, "Should put positive number of coins."

        if amount > self.coin:
            raise UnableToPlayError(error_code=PlayErrorCode.PLAYER_HAS_NOT_ENOUGH_COIN)

        self.coin -= amount
        self.pot.put_coin(amount=amount)

        assert self.coin >= 0, "Remaining coins should be positive."

    def play(self) -> None:
        self.print_log(f"[Player {self.id} plays]")
        self.print_log(f"\t[Current] Player {self.id} ({self.coin} coin) / pot ({self.pot.coin} coin).")

        dice_result = self.roll_dice()
        self.print_log(f"\tDice result: {dice_result}.")

        if dice_result == 1:
            # do nothing
            self.print_log(f"\tPlayer {self.id} does nothing.")
        elif dice_result == 2:
            self.print_log(f"\tPlayer {self.id} takes all coins from the pot.")
            self.draw_all_coins()
        elif dice_result == 3:
            self.print_log(f"\tPlayer {self.id} takes half coins from the pot.")
            self.draw_half_coins()
        elif 4 <= dice_result <= 6:
            self.print_log(f"\tPlayer {self.id} puts {self.coin_put_amount} coin to the pot.")
            self.put_coin_in_pot(amount=self.coin_put_amount)
        else:
            assert False, "Dice result should not reach here"

        # self.print_log(f"[Result]")
        self.print_log(f"\t[Result] Player {self.id} ({self.coin} coin) / pot ({self.pot.coin} coin).")
        self.print_log()

    @staticmethod
    def roll_dice() -> int:
        return random.randint(1, 6)


class PersonTest(unittest.TestCase):
    def setUp(self) -> None:
        self.pot = Pot()
        self.person = Player(coin=4, pot=self.pot)

    def test_roll_dice(self):
        dice_number = self.person.roll_dice()
        self.assertTrue(1 <= dice_number <= 6)

    # def test_draw_all_coins(self):
    # def test_draw_half_coins(self):