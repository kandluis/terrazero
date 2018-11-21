import random

from typing import List

from simulation.core import common


class Game:
  NUM_ROUNDS = 6

  def __init__(self):
    self.scoring_tiles = random.sample(
        list(common.ScoringTile), Game.NUM_ROUNDS)
