import unittest

from simulation.core import common
from simulation.core import faction
from simulation.core import player

class TestPlayer(unittest.TestCase):
  def testPlayerGainingSinglePower(self):
    halfling = faction.Halflings()
    test_player = player.Player(halfling)

    # Starting configuration for the given class.
    self.assertEqual(test_player.power, {
      common.PowerBowl.I : 3, common.PowerBowl.II: 9, common.PowerBowl.III: 0
      })
    self.assertEqual(test_player.coins, 15)

    self.assertIsNone(test_player.GainPower(1))
    self.assertEqual(test_player.power, {
      common.PowerBowl.I: 2, common.PowerBowl.II: 10, common.PowerBowl.III: 0
      })
    self.assertEqual(test_player.coins, 15)

  def testPlayerGainingRolloverPower(self):
    halfling = faction.Halflings()
    test_player = player.Player(halfling)

    # Starting configuration for the given class.
    self.assertEqual(test_player.power, {
      common.PowerBowl.I: 3, common.PowerBowl.II: 9, common.PowerBowl.III: 0
      })
    self.assertEqual(test_player.coins, 15)

    self.assertIsNone(test_player.GainPower(4))
    self.assertEqual(test_player.power, {
      common.PowerBowl.I: 0, common.PowerBowl.II: 11, common.PowerBowl.III: 1
      })
    self.assertEqual(test_player.coins, 15)

  def testPlayerGainingMaxPower(self):
    halfling = faction.Halflings()
    test_player = player.Player(halfling)

    # Starting configuration for the given class.
    self.assertEqual(test_player.power, {
      common.PowerBowl.I : 3, common.PowerBowl.II: 9, common.PowerBowl.III: 0
      })
    self.assertEqual(test_player.coins, 15)

    self.assertIsNone(test_player.GainPower(15))
    self.assertEqual(test_player.power, {
      common.PowerBowl.I: 0, common.PowerBowl.II: 0, common.PowerBowl.III: 12
      })
    self.assertEqual(test_player.coins, 15)

  def testPlayerGainingMaxPowerPlusEvenValue(self):
    halfling = faction.Halflings()
    test_player = player.Player(halfling)

    # Starting configuration for the given class.
    self.assertEqual(test_player.power, {
      common.PowerBowl.I : 3, common.PowerBowl.II: 9, common.PowerBowl.III: 0
      })
    self.assertEqual(test_player.coins, 15)

    # 15 gets us to max, the extra 4 power is converted into 2 coins.
    self.assertIsNone(test_player.GainPower(19))
    self.assertEqual(test_player.power, {
      common.PowerBowl.I: 0, common.PowerBowl.II: 0, common.PowerBowl.III: 12
      })
    self.assertEqual(test_player.coins, 17)

  def testPlayerGainingMaxPowerPlusOddValue(self):
    halfling = faction.Halflings()
    test_player = player.Player(halfling)

    # Starting configuration for the given class.
    self.assertEqual(test_player.power, {
      common.PowerBowl.I : 3, common.PowerBowl.II: 9, common.PowerBowl.III: 0
      })
    self.assertEqual(test_player.coins, 15)

    # 15 gets us to max, the extra 3 power is converted into 2 coins.
    # Even though this may not be optimal.
    self.assertIsNone(test_player.GainPower(18))
    self.assertEqual(test_player.power, {
      common.PowerBowl.I: 0, common.PowerBowl.II: 1, common.PowerBowl.III: 11
      })
    self.assertEqual(test_player.coins, 17)