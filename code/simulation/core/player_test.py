import unittest

from simulation.core import common
from simulation.core import faction
from simulation.core import player
from simulation import utils


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

  def testSacrificePriestToOrder(self):
    test_player = player.Player(
        name="test", player_faction=faction.Halflings())

    test_player.SacrificePriestToOrder()
    self.assertEqual(test_player.priests_still_in_play,
                     player.Player.MAX_PRIESTS - 1)

  def testPlayerCanBuild(self):
    test_player = player.Player(
        name="test", player_faction=faction.Halflings())

    # Halflings start with 15 coins and 3 workers, as well as 9
    # power in Bowl II and 3 power in Bowl I.

    # They can afford dwellings.
    self.assertTrue(
        test_player.CanBuild(common.Structure.DWELLING, adjacentEnemies=True))
    self.assertTrue(
        test_player.CanBuild(common.Structure.DWELLING, adjacentEnemies=False))

    # They can also afford TPs which are adjacent or not.
    self.assertTrue(
        test_player.CanBuild(
            common.Structure.TRADING_POST, adjacentEnemies=True))
    self.assertTrue(
        test_player.CanBuild(
            common.Structure.TRADING_POST, adjacentEnemies=False))

    # They can afford temples.
    self.assertTrue(
        test_player.CanBuild(common.Structure.TEMPLE, adjacentEnemies=True))
    self.assertTrue(
        test_player.CanBuild(common.Structure.TEMPLE, adjacentEnemies=False))

    # But not strongholds or santuaries, even by burning power, if they only
    # have 2 workers.
    test_player.resources.workers = 2
    self.assertFalse(
        test_player.CanBuild(common.Structure.SANCTUARY, adjacentEnemies=True))
    self.assertFalse(
        test_player.CanBuild(
            common.Structure.SANCTUARY, adjacentEnemies=False))
    self.assertFalse(
        test_player.CanBuild(
            common.Structure.STRONGHOLD, adjacentEnemies=True))
    self.assertFalse(
        test_player.CanBuild(
            common.Structure.STRONGHOLD, adjacentEnemies=False))

  def testPlayerBuildDwellings(self):
    test_player = player.Player(
        name="test", player_faction=faction.Halflings())
    oldPower = test_player.power.copy()

    # Halflings start with 15 coins and 3 workers, as well as 9
    # power in Bowl II and 3 power in Bowl I.
    test_player.Build(common.Structure.DWELLING, adjacentEnemies=True)
    test_player.Build(common.Structure.DWELLING, adjacentEnemies=True)
    # After building 2 dwellings, they should have 11 coin, 1 worker.
    self.assertEqual(test_player.resources,
                     common.Resources(coins=11, workers=1))
    # And they did not burn any power.
    self.assertEqual(test_player.power, oldPower)
    # But they have two less Dwellings.
    self.assertEqual(
        test_player.structures[common.Structure.DWELLING],
        faction.Faction.TOTAL_STRUCTURES[common.Structure.DWELLING] - 2)
    self.assertEqual(test_player.built_structures[common.Structure.DWELLING],
                     2)

  def testPlayerBurnToBuild(self):
    test_player = player.Player(
        name="test", player_faction=faction.Halflings())

    # Halflings start with 15 coins and 3 workers, as well as 9
    # power in Bowl II and 3 power in Bowl I.
    test_player.Build(common.Structure.TRADING_POST, adjacentEnemies=False)
    # After building 1 TP (not adjacent), it costs 6 coins and 2 workers.
    self.assertEqual(test_player.resources, common.Resources(
        coins=9, workers=1))
    # The next TP can be built that is adjacent, costs 3 coins and 2 workers.
    # Player must burn 3 power to get the extra worker.
    test_player.Build(common.Structure.TRADING_POST, adjacentEnemies=True)
    self.assertEqual(test_player.resources, common.Resources(
        coins=6, workers=0))
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 6,
        common.PowerBowl.II: 3,
        common.PowerBowl.III: 0
    })

  def testBuildFailureIfCanNotBuild(self):
    test_player = player.Player(
        name="test", player_faction=faction.Halflings())
    test_player.resources.workers = 2
    # Cannot build a stronghold.
    self.assertFalse(
        test_player.CanBuild(
            common.Structure.STRONGHOLD, adjacentEnemies=False))
    with self.assertRaises(utils.InternalError):
      test_player.Build(common.Structure.STRONGHOLD, adjacentEnemies=False)

    # Alternatively, if we've already built it.
    test_player.Build(
        common.Structure.STRONGHOLD, adjacentEnemies=False, free=True)

    self.assertFalse(
        test_player.CanBuild(
            common.Structure.STRONGHOLD, adjacentEnemies=False))
    with self.assertRaises(utils.InternalError):
      test_player.Build(common.Structure.STRONGHOLD, adjacentEnemies=False)

  def testPlayerCollectIncomePhase(self):
    # Halflings start with 3 workers and 15 coins, 3/9/0 power.
    test_player = player.Player(
        name="test", player_faction=faction.Halflings())
    oldPower = test_player.power.copy()

    # Player has not structures. Bonus card is manually set.
    test_player.bonus_card = common.BonusCard.TRADING_POST_WORKER
    test_player.CollectPhaseIIncome()
    self.assertEqual(test_player.power, oldPower)
    self.assertEqual(test_player.resources,
                     common.Resources(workers=5, coins=15))

    # Let player build dweling one of each, all for free.
    test_player.Build(
        common.Structure.DWELLING, adjacentEnemies=False, free=True)
    test_player.Build(
        common.Structure.TRADING_POST, adjacentEnemies=False, free=True)
    test_player.Build(
        common.Structure.STRONGHOLD, adjacentEnemies=False, free=True)
    test_player.Build(
        common.Structure.TEMPLE, adjacentEnemies=False, free=True)
    test_player.Build(
        common.Structure.SANCTUARY, adjacentEnemies=False, free=True)

    # Collect income. Structures will provide 2 priest, 1 worker, 2 coins, 3 power.
    # An additional 1 worker is provided by default.
    # Bonus card provides additional 1 worker.
    test_player.CollectPhaseIIncome()
    self.assertEqual(test_player.resources,
                     common.Resources(workers=8, priests=2, coins=17),
                     "Player resources: %s" % test_player.resources)
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 0,
        common.PowerBowl.II: 12,
        common.PowerBowl.III: 0
    })

  def testPlayerCanUsePowerAndUsePower(self):
    pass
