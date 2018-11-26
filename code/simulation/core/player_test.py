import unittest

from simulation.core import common
from simulation.core import faction
from simulation.core import player


class TestPlayer(unittest.TestCase):
  def testHalflingPlayer(self):
    test_player = player.Player(
        name="test", player_faction=faction.Halflings())

    # Halfling configuration.
    self.assertEqual(test_player.name, "test")
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 3,
        common.PowerBowl.II: 9,
        common.PowerBowl.III: 0
    })
    self.assertEqual(test_player.resources,
                     common.Resources(coins=15, workers=3))
    self.assertEqual(test_player.used_town_keys, {})
    self.assertEqual(test_player.victory_points, 20)

  def testEngineerPlayer(self):
    test_player = player.Player(
        name="test", player_faction=faction.Engineers())

    # Halfling configuration.
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 3,
        common.PowerBowl.II: 9,
        common.PowerBowl.III: 0
    })
    self.assertEqual(test_player.resources,
                     common.Resources(coins=10, workers=2))
    self.assertEqual(test_player.used_town_keys, {})
    self.assertEqual(test_player.victory_points, 20)

  def testPlayerGainingSinglePower(self):
    halfling = faction.Halflings()
    test_player = player.Player("test", halfling)

    # Starting configuration for the given class.
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 3,
        common.PowerBowl.II: 9,
        common.PowerBowl.III: 0
    })
    self.assertEqual(test_player.resources.coins, 15)

    test_player.GainPower(1)
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 2,
        common.PowerBowl.II: 10,
        common.PowerBowl.III: 0
    })
    self.assertEqual(test_player.resources.coins, 15)

  def testPlayerGainingRolloverPower(self):
    halfling = faction.Halflings()
    test_player = player.Player("test", halfling)

    # Starting configuration for the given class.
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 3,
        common.PowerBowl.II: 9,
        common.PowerBowl.III: 0
    })
    self.assertEqual(test_player.resources.coins, 15)

    test_player.GainPower(4)
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 0,
        common.PowerBowl.II: 11,
        common.PowerBowl.III: 1
    })
    self.assertEqual(test_player.resources.coins, 15)

  def testPlayerGainingMaxPower(self):
    halfling = faction.Halflings()
    test_player = player.Player("test", halfling)

    # Starting configuration for the given class.
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 3,
        common.PowerBowl.II: 9,
        common.PowerBowl.III: 0
    })
    self.assertEqual(test_player.resources.coins, 15)

    test_player.GainPower(15)
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 0,
        common.PowerBowl.II: 0,
        common.PowerBowl.III: 12
    })
    self.assertEqual(test_player.resources.coins, 15)

  def testPlayerGainingMaxPowerPlusEvenValue(self):
    halfling = faction.Halflings()
    test_player = player.Player("test", halfling)

    # Starting configuration for the given class.
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 3,
        common.PowerBowl.II: 9,
        common.PowerBowl.III: 0
    })
    self.assertEqual(test_player.resources.coins, 15)

    # 15 gets us to max, the extra 4 power is converted into 2 coins.
    test_player.GainPower(19)
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 0,
        common.PowerBowl.II: 0,
        common.PowerBowl.III: 12
    })
    self.assertEqual(test_player.resources.coins, 17)

  def testPlayerGainingMaxPowerPlusOddValue(self):
    halfling = faction.Halflings()
    test_player = player.Player("test", halfling)

    # Starting configuration for the given class.
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 3,
        common.PowerBowl.II: 9,
        common.PowerBowl.III: 0
    })
    self.assertEqual(test_player.resources.coins, 15)

    # 15 gets us to max, the extra 3 power is converted into 2 coins.
    # Even though this may not be optimal.
    test_player.GainPower(18)
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 0,
        common.PowerBowl.II: 1,
        common.PowerBowl.III: 11
    })
    self.assertEqual(test_player.resources.coins, 17)

  def testPlayerTownKeys(self):
    test_player = player.Player(
        name="test", player_faction=faction.Halflings())
    self.assertEqual(test_player.used_town_keys, {})

    # Gain a town key and use it.
    test_player.GainTown(common.TownKey.CULT)
    self.assertEqual(test_player.used_town_keys, {common.TownKey.CULT: False})

    self.assertTrue(test_player.UseTownKey())
    self.assertEqual(test_player.used_town_keys, {common.TownKey.CULT: True})
    self.assertFalse(test_player.UseTownKey())
    self.assertEqual(test_player.used_town_keys, {common.TownKey.CULT: True})
