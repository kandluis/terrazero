import random

from typing import List

from simulation.core import common
from simulation.core import player
from simulation.core import cult
from simulation.interface import terminal


class Game:
  NUM_ROUNDS = 6
  MIN_PLAYERS = 2
  MAX_PLAYERS = 5

  def __init__(self, players: List[player.Player],
               scoring_tiles: List[common.ScoringTile],
               bonus_cards: List[common.BonusCard]) -> None:
    self.num_players = len(players)
    assert Game.MIN_PLAYERS <= self.num_players <= Game.MAX_PLAYERS
    # self.players[i] is the player which will go on turn i.
    self.players = players
    # self.scoring_tiles[i] is the scorling tile for the (i+1)-th round of gameplay.
    self.scoring_tiles: List[common.ScoringTile] = scoring_tiles
    # just a list of the currently available bonus tiles.
    self.available_bonus_cards: List[common.BonusCard] = bonus_cards

    # The index of the current round being played.
    self.round_index: int = 0

    self.cultboard = cult.CultBoard(
        factions=[player.faction for player in self.players])


def SelectGameScoringTiles() -> List[common.ScoringTile]:
  return random.sample(list(common.ScoringTile), Game.NUM_ROUNDS)


def SelectGameBonusCards(num_players: int) -> List[common.BonusCard]:
  return random.sample(list(common.BonusCard), num_players + 3)
