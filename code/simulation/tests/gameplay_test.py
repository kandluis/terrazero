import unittest
import random

from simulation.core import gameplay
from simulation.core import common
from simulation.core import player


class MockPlayer(player.Player):
  def __init__(self):
    pass


class TestGameObject(unittest.TestCase):
  def testSelectingGameScoringTiles(self):
    random.seed(1)
    self.assertCountEqual(gameplay.SelectGameScoringTiles(), [
        common.ScoringTile.TP_WATER4_SPADE,
        common.ScoringTile.STRONGHOLD_AIR2_WORKER,
        common.ScoringTile.TP_AIR4_SPADE,
        common.ScoringTile.STRONGHOLD_FIRE2_WORKER,
        common.ScoringTile.SPADE_EARTH_COIN,
        common.ScoringTile.DWELLING_WATER4_PRIEST,
    ])

    random.seed(2)
    self.assertCountEqual(gameplay.SelectGameScoringTiles(), [
        common.ScoringTile.TP_AIR4_SPADE,
        common.ScoringTile.STRONGHOLD_FIRE2_WORKER,
        common.ScoringTile.DWELLING_FIRE4_POWER4,
        common.ScoringTile.TP_WATER4_SPADE,
        common.ScoringTile.DWELLING_WATER4_PRIEST,
        common.ScoringTile.STRONGHOLD_AIR2_WORKER,
    ])

    random.seed(3)
    self.assertCountEqual(gameplay.SelectGameScoringTiles(), [
        common.ScoringTile.TOWN_EARTH4_SPADE,
        common.ScoringTile.STRONGHOLD_AIR2_WORKER,
        common.ScoringTile.DWELLING_FIRE4_POWER4,
        common.ScoringTile.DWELLING_WATER4_PRIEST,
        common.ScoringTile.TP_WATER4_SPADE,
        common.ScoringTile.STRONGHOLD_FIRE2_WORKER,
    ])

  def testSelectingBonusCardsForPlayer(self):
    self.assertEqual(len(gameplay.SelectGameBonusCards(num_players=3)), 3 + 3)
    self.assertEqual(len(gameplay.SelectGameBonusCards(num_players=5)), 5 + 3)

  def testPlayerLimits(self):
    with self.assertRaises(AssertionError):
      gameplay.Game(players=[MockPlayer()], scoring_tiles=[], bonus_cards=[])

    with self.assertRaises(AssertionError):
      gameplay.Game(
          players=[MockPlayer() for _ in range(6)],
          scoring_tiles=[],
          bonus_cards=[])