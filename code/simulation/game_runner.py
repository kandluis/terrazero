from typing import List

from simulation.core import common
from simulation.core import faction
from simulation.core import gameplay
from simulation.core import player
from simulation.interface import terminal
from simulation.interface import io

_NUM_ROUNDS = 6


class GameRunner:
  def __init__(self) -> None:
    self.game = self._init_game()

  def _init_game(self) -> gameplay.Game:
    interface: io.IO = terminal.CommandLine()
    interface.welcome_message()

    num_players: int = interface.request_number_of_players()
    player_names: List[str] = interface.request_player_names(num_players)

    scoring_tiles: List[
        common.ScoringTile] = gameplay.select_game_scoring_tiles()
    bonus_cards: List[common.BonusCard] = gameplay.select_game_bonus_cards(
        num_players=num_players)

    interface.display_scoring_tiles(scoring_tiles)
    interface.display_bonus_cards(bonus_cards)
    player_factions = interface.request_player_factions(
        player_names, available=faction.all_available())

    players = [
        player.Player(name=player_name, player_faction=selected_faction)
        for player_name, selected_faction in zip(player_names, player_factions)
    ]
    return gameplay.Game(players, scoring_tiles, bonus_cards, interface)

  def execute(self) -> None:
    self.game.initialize_dwellings()
    self.game.initialize_bonus_cards()
    for _ in range(_NUM_ROUNDS):
      self.game.income_phase()
