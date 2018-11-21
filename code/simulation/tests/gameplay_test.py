import unittest
import random

from simulation.core import gameplay


class TestGameObject(unittest.TestCase):
  def testInitialization(self):
    random.seed(42)  # To make test deterministic.
    game = gameplay.Game()
    self.assertCountEqual(game.scoring_tiles, [
        common.ScoringTile.DWELLING_WATER4_PRIEST,
        common.ScoringTile.TP_AIR4_SPADE, common.ScoringTile.SPADE_EARTH_COIN,
        common.ScoringTile.TP_WATER4_SPADE,
        common.ScoringTile.STRONGHOLD_FIRE2_WORKER,
        common.ScoringTile.DWELLING_FIRE4_POWER4
    ])

  def testScoreShuffleInitialization(self):
    random.seed(1)
    game_seed1 = gameplay.Game()
    self.assertCountEqual(game_seed1.scoring_tiles, [
        common.ScoringTile.TP_WATER4_SPADE,
        common.ScoringTile.STRONGHOLD_AIR2_WORKER,
        common.ScoringTile.TP_AIR4_SPADE,
        common.ScoringTile.STRONGHOLD_FIRE2_WORKER,
        common.ScoringTile.SPADE_EARTH_COIN,
        common.ScoringTile.DWELLING_WATER4_PRIEST,
    ])

    random.seed(2)
    game_seed2 = gameplay.Game()
    self.assertCountEqual(game_seed2.scoring_tiles, [])

    random.seed(3)
    game_seed3 = gameplay.Game()
    self.assertCountEqual(game_seed3.scoring_tiles, [])
