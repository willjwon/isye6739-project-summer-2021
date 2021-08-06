import json
import os
import pickle

from player import Player
from pot import Pot
from unable_to_play_error import UnableToPlayError


class GameSimulator:
    def __init__(self, players_count: int,
                 initial_player_coin: int, initial_pot_coin: int,
                 coin_put_amount: int,
                 allow_zero_coin_draw: bool = True, verbose: bool = True):
        # assertion
        assert players_count > 0, "There should be at least one player"
        assert initial_player_coin >= 0, "Initial coin should be positive"
        assert initial_pot_coin >= 0, "Initial coin should be positive"
        assert coin_put_amount >= 0, "Coin put amount should be positive"
        if allow_zero_coin_draw:
            assert coin_put_amount > 0, "The game must be stop."

        # initialize pot
        self.pot = Pot(coin=initial_pot_coin, allow_zero_coin_draw=allow_zero_coin_draw)

        # initialize players
        self.current_player_index = -1
        self.players = list()
        for id in range(players_count):
            self.players.append(Player(id=id, coin=initial_player_coin, coin_put_amount=coin_put_amount, pot=self.pot,
                                       verbose=verbose))

        self.players_count = players_count
        self.verbose = verbose

    def print_log(self, message=None) -> None:
        if self.verbose:
            print(message)

    def get_next_player(self) -> Player:
        self.current_player_index += 1
        if self.current_player_index >= self.players_count:
            self.current_player_index = 0

        return self.players[self.current_player_index]

    def simulate(self) -> (int, int, int, int):
        turns_count = 0

        while True:
            player = self.get_next_player()
            try:
                player.play()
                turns_count += 1
            except UnableToPlayError as error:
                self.print_log(f"\n[Play Ended] Reason: {error.error_code.name} (Player {player.id})\n")
                break

        cycles_count = turns_count // self.players_count
        winner_coins_count = max(map(lambda x: x.coin, self.players))

        self.print_log(f"[Turns] {turns_count} turns.")
        self.print_log(f"[Cycles] {cycles_count} cycles.")
        self.print_log(f"[Coins] Winner has {winner_coins_count} coin.")
        self.print_log(f"[Pot] Pot has {self.pot.coin} coin.")

        return turns_count, cycles_count, winner_coins_count, self.pot.coin


if __name__ == '__main__':
    # read configs
    with open('../configs.json', 'r') as f:
        configs = json.load(f)

    players_count = configs['player_configs']['players_count']
    initial_player_coin = configs['player_configs']['initial_player_coin']
    coin_put_amount = configs['player_configs']['coin_put_amount']

    initial_pot_coin = configs['pot_configs']['initial_pot_coin']
    allow_zero_coin_draw = configs['pot_configs']['allow_zero_coin_draw']

    simulation_repetition = configs['simulation_configs']['repetition']
    verbose_output = configs['simulation_configs']['verbose_output']

    # simulate
    turns = dict()
    cycles = dict()
    winner_coins = dict()
    pot_coins = dict()
    for _ in range(simulation_repetition):
        # run simulation
        game_simulator = GameSimulator(players_count=players_count,
                                       initial_player_coin=initial_player_coin,
                                       initial_pot_coin=initial_pot_coin,
                                       coin_put_amount=coin_put_amount,
                                       allow_zero_coin_draw=allow_zero_coin_draw,
                                       verbose=verbose_output)

        turns_count, cycles_count, winner_coins_count, pot_coins_count = game_simulator.simulate()

        turns[turns_count] = turns.get(turns_count, 0) + 1
        cycles[cycles_count] = cycles.get(cycles_count, 0) + 1
        winner_coins[winner_coins_count] = winner_coins.get(winner_coins_count, 0) + 1
        pot_coins[pot_coins_count] = pot_coins.get(pot_coins_count, 0) + 1

    # save result
    if not os.path.exists('../simulation_result/'):
        os.makedirs('../simulation_result/')

    with open(file='../simulation_result/simulation_result.pickle', mode='wb') as file:
        pickle.dump(obj=[configs, turns, cycles, winner_coins, pot_coins], file=file)
