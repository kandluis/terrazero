import unittest

from simulation.core import common
from simulation.core import faction
from simulation.core import player
from simulation import utils


class TestPlayer(unittest.TestCase):
  def test_halfling_player(self) -> None:
    test_player = player.Player(name="test",
                                player_faction=faction.Halflings())

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

  def test_engineer_player(self) -> None:
    test_player = player.Player(name="test",
                                player_faction=faction.Engineers())

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

  def test_player_gaining_single_power(self) -> None:
    halfling = faction.Halflings()
    test_player = player.Player("test", halfling)

    # Starting configuration for the given class.
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 3,
        common.PowerBowl.II: 9,
        common.PowerBowl.III: 0
    })
    self.assertEqual(test_player.resources.coins, 15)

    test_player.gain_power(1)
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 2,
        common.PowerBowl.II: 10,
        common.PowerBowl.III: 0
    })
    self.assertEqual(test_player.resources.coins, 15)

  def test_player_gaining_rollover_power(self) -> None:
    halfling = faction.Halflings()
    test_player = player.Player("test", halfling)

    # Starting configuration for the given class.
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 3,
        common.PowerBowl.II: 9,
        common.PowerBowl.III: 0
    })
    self.assertEqual(test_player.resources.coins, 15)

    test_player.gain_power(4)
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 0,
        common.PowerBowl.II: 11,
        common.PowerBowl.III: 1
    })
    self.assertEqual(test_player.resources.coins, 15)

  def test_player_gaining_max_power(self) -> None:
    halfling = faction.Halflings()
    test_player = player.Player("test", halfling)

    # Starting configuration for the given class.
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 3,
        common.PowerBowl.II: 9,
        common.PowerBowl.III: 0
    })
    self.assertEqual(test_player.resources.coins, 15)

    test_player.gain_power(15)
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 0,
        common.PowerBowl.II: 0,
        common.PowerBowl.III: 12
    })
    self.assertEqual(test_player.resources.coins, 15)

  def test_player_gaining_max_power_plus_even_value(self) -> None:
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
    test_player.gain_power(19)
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 0,
        common.PowerBowl.II: 0,
        common.PowerBowl.III: 12
    })
    self.assertEqual(test_player.resources.coins, 17)

  def test_player_gaining_max_power_plus_odd_value(self) -> None:
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
    test_player.gain_power(18)
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 0,
        common.PowerBowl.II: 1,
        common.PowerBowl.III: 11
    })
    self.assertEqual(test_player.resources.coins, 17)

  def test_player_gain_power_but_not_tokens_left(self) -> None:
    test_player = player.Player("test", player_faction=faction.Halflings())
    # Manually set to only a single token left.
    test_player.power = {
        common.PowerBowl.I: 1,
        common.PowerBowl.II: 0,
        common.PowerBowl.III: 0
    }
    # Gain 2 power.
    test_player.gain_power(2)
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 0,
        common.PowerBowl.II: 0,
        common.PowerBowl.III: 1
    })

    # Gain one more power. This should become a coin.
    test_player.gain_power(1)
    self.assertEqual(test_player.resources.coins, 16)
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 0,
        common.PowerBowl.II: 1,
        common.PowerBowl.III: 0
    })

    # Manually get rid of last power to see what happens when all power is
    # burned (even though this is not possible in real game)
    test_player.power = {
        common.PowerBowl.I: 0,
        common.PowerBowl.II: 0,
        common.PowerBowl.III: 0
    }
    emptyPower = test_player.power.copy()
    test_player.gain_power(2)
    self.assertEqual(test_player.power, emptyPower)

  def test_player_town_key(self) -> None:
    test_player = player.Player(name="test",
                                player_faction=faction.Halflings())
    self.assertEqual(test_player.used_town_keys, {})

    # Gain a town key and use it.
    test_player.gain_town(common.TownKey.CULT)
    self.assertEqual(test_player.used_town_keys, {common.TownKey.CULT: False})

    self.assertTrue(test_player.use_town_key())
    self.assertEqual(test_player.used_town_keys, {common.TownKey.CULT: True})
    self.assertFalse(test_player.use_town_key())
    self.assertEqual(test_player.used_town_keys, {common.TownKey.CULT: True})

  def test_sacrifice_priest_to_order(self) -> None:
    test_player = player.Player(name="test",
                                player_faction=faction.Halflings())

    test_player.sacrifice_priest_to_order()
    self.assertEqual(test_player.priests_still_in_play,
                     player.Player.MAX_PRIESTS - 1)

  def test_player_can_build(self) -> None:
    test_player = player.Player(name="test",
                                player_faction=faction.Halflings())

    # Halflings start with 15 coins and 3 workers, as well as 9
    # power in Bowl II and 3 power in Bowl I.

    # They can afford dwellings.
    self.assertTrue(
        test_player.can_build(common.Structure.DWELLING, adjacentEnemies=True))
    self.assertTrue(
        test_player.can_build(common.Structure.DWELLING,
                              adjacentEnemies=False))

    # They can also afford TPs which are adjacent or not.
    self.assertTrue(
        test_player.can_build(common.Structure.TRADING_POST,
                              adjacentEnemies=True))
    self.assertTrue(
        test_player.can_build(common.Structure.TRADING_POST,
                              adjacentEnemies=False))

    # They can afford temples.
    self.assertTrue(
        test_player.can_build(common.Structure.TEMPLE, adjacentEnemies=True))
    self.assertTrue(
        test_player.can_build(common.Structure.TEMPLE, adjacentEnemies=False))

    # But not strongholds or santuaries, even by burning power, if they only
    # have 2 workers.
    test_player.resources.workers = 2
    self.assertFalse(
        test_player.can_build(common.Structure.SANCTUARY,
                              adjacentEnemies=True))
    self.assertFalse(
        test_player.can_build(common.Structure.SANCTUARY,
                              adjacentEnemies=False))
    self.assertFalse(
        test_player.can_build(common.Structure.STRONGHOLD,
                              adjacentEnemies=True))
    self.assertFalse(
        test_player.can_build(common.Structure.STRONGHOLD,
                              adjacentEnemies=False))

  def test_player_build_dwellings(self) -> None:
    test_player = player.Player(name="test",
                                player_faction=faction.Halflings())
    old_power = test_player.power.copy()

    # Halflings start with 15 coins and 3 workers, as well as 9
    # power in Bowl II and 3 power in Bowl I.
    test_player.build(common.Structure.DWELLING, adjacentEnemies=True)
    test_player.build(common.Structure.DWELLING, adjacentEnemies=True)
    # After building 2 dwellings, they should have 11 coin, 1 worker.
    self.assertEqual(test_player.resources,
                     common.Resources(coins=11, workers=1))
    # And they did not burn any power.
    self.assertEqual(test_player.power, old_power)
    # But they have two less Dwellings.
    self.assertEqual(
        test_player.structures[common.Structure.DWELLING],
        faction.Faction.TOTAL_STRUCTURES[common.Structure.DWELLING] - 2)
    self.assertEqual(test_player.built_structures[common.Structure.DWELLING],
                     2)

  def test_player_burn_to_build(self) -> None:
    test_player = player.Player(name="test",
                                player_faction=faction.Halflings())

    # Halflings start with 15 coins and 3 workers, as well as 9
    # power in Bowl II and 3 power in Bowl I.
    test_player.build(common.Structure.TRADING_POST, adjacentEnemies=False)
    # After building 1 TP (not adjacent), it costs 6 coins and 2 workers.
    self.assertEqual(test_player.resources, common.Resources(coins=9,
                                                             workers=1))
    # The next TP can be built that is adjacent, costs 3 coins and 2 workers.
    # Player must burn 3 power to get the extra worker.
    test_player.build(common.Structure.TRADING_POST, adjacentEnemies=True)
    self.assertEqual(test_player.resources, common.Resources(coins=6,
                                                             workers=0))
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 6,
        common.PowerBowl.II: 3,
        common.PowerBowl.III: 0
    })

  def test_player_build_failure_if_cannot_build(self) -> None:
    test_player = player.Player(name="test",
                                player_faction=faction.Halflings())
    test_player.resources.workers = 2
    # Cannot build a stronghold.
    self.assertFalse(
        test_player.can_build(common.Structure.STRONGHOLD,
                              adjacentEnemies=False))
    with self.assertRaises(utils.InternalError):
      test_player.build(common.Structure.STRONGHOLD, adjacentEnemies=False)

    # Alternatively, if we've already built it.
    test_player.build(common.Structure.STRONGHOLD,
                      adjacentEnemies=False,
                      free=True)

    self.assertFalse(
        test_player.can_build(common.Structure.STRONGHOLD,
                              adjacentEnemies=False))
    with self.assertRaises(utils.InternalError):
      test_player.build(common.Structure.STRONGHOLD, adjacentEnemies=False)

  def test_player_collect_income_phase(self) -> None:
    # Halflings start with 3 workers and 15 coins, 3/9/0 power.
    test_player = player.Player(name="test",
                                player_faction=faction.Halflings())
    oldPower = test_player.power.copy()

    # Player has not structures. Bonus card is manually set.
    test_player.bonus_card = common.BonusCard.TRADING_POST_WORKER
    test_player.collect_phase_ii_income()
    self.assertEqual(test_player.power, oldPower)
    self.assertEqual(test_player.resources,
                     common.Resources(workers=5, coins=15))

    # Let player build dweling one of each, all for free.
    test_player.build(common.Structure.DWELLING,
                      adjacentEnemies=False,
                      free=True)
    test_player.build(common.Structure.TRADING_POST,
                      adjacentEnemies=False,
                      free=True)
    test_player.build(common.Structure.STRONGHOLD,
                      adjacentEnemies=False,
                      free=True)
    test_player.build(common.Structure.TEMPLE,
                      adjacentEnemies=False,
                      free=True)
    test_player.build(common.Structure.SANCTUARY,
                      adjacentEnemies=False,
                      free=True)

    # Collect income. Structures will provide 2 priest, 1 worker, 2 coins,
    # 3 power. An additional 1 worker is provided by default.
    # Bonus card provides additional 1 worker.
    test_player.collect_phase_ii_income()
    self.assertEqual(test_player.resources,
                     common.Resources(workers=8, priests=2, coins=17),
                     "Player resources: %s" % test_player.resources)
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 0,
        common.PowerBowl.II: 12,
        common.PowerBowl.III: 0
    })

  def test_player_collect_income_from_favorite_tiles(self) -> None:
    test_player = player.Player(name="test",
                                player_faction=faction.Halflings())
    # Set bonus card and favor tiles.
    test_player.bonus_card = common.BonusCard.PRIEST
    test_player.favor_tiles = [
        common.FavorTile.POWER4_AIR2, common.FavorTile.COIN3_FIRE
    ]

    # Player receives 1 worker income (default for no structures).
    # Player receives 1 priest for bonus card.
    # Player receives 4 power and 3 coin for favor tiles.
    # New income should be 4 worker, 1 priest, 18 coin, 0/11/1
    test_player.collect_phase_ii_income()
    self.assertEqual(test_player.resources,
                     common.Resources(workers=4, priests=1, coins=18),
                     "Player resources %s. " % test_player.resources)
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 0,
        common.PowerBowl.II: 11,
        common.PowerBowl.III: 1
    })

  def testPlayerBoundNumberOfPriests(self) -> None:
    test_player = player.Player(name="test",
                                player_faction=faction.Halflings())
    # Set bonus card to a priest.
    test_player.bonus_card = common.BonusCard.PRIEST
    # Manually increase the resources owned by this player to maximum
    # number of allowed priests.
    self.assertTrue(test_player.priests_still_in_play > 0)
    test_player.resources.priests = test_player.priests_still_in_play

    # Try to collect income. In this case, we will still have the same number
    # of priests.
    oldPriests = test_player.resources.priests
    test_player.collect_phase_ii_income()
    self.assertEqual(test_player.resources.priests, oldPriests)

  def test_player_can_use_power(self) -> None:
    test_player = player.Player(name="test",
                                player_faction=faction.Halflings())

    # For starting 3/9/0, we can always use power up to 4 (by burning)
    for power in range(5):
      self.assertTrue(test_player.can_use_power(power))

    # Can't even burn to get this much.
    self.assertFalse(test_player.can_use_power(5))
    with self.assertRaises(utils.InternalError):
      test_player.use_power(5)

    # But we can use 3 power by burning.
    test_player.use_power(3)
    self.assertEqual(test_player.power, {
        common.PowerBowl.I: 6,
        common.PowerBowl.II: 3,
        common.PowerBowl.III: 0
    })

  def test_player_take_bonus_cards(self) -> None:
    test_player = player.Player(name="test",
                                player_faction=faction.Halflings())

    # Return None card.
    self.assertIsNone(test_player.take_bonus_card(common.BonusCard.PRIEST))

    # Now take the shipping card, which is special.
    self.assertEqual(
        test_player.take_bonus_card(common.BonusCard.POWER3_SHIPPING),
        common.BonusCard.PRIEST)
    self.assertEqual(test_player.shipping, 1)

    # Now take another card, givign back the shipping.
    self.assertEqual(test_player.take_bonus_card(common.BonusCard.CULT_COIN4),
                     common.BonusCard.POWER3_SHIPPING)
    self.assertEqual(test_player.shipping, 0)
