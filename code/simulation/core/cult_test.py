import unittest

from simulation.core import common
from simulation.core import cult
from simulation.core import faction
from simulation.core import player


class TestCultBoard(unittest.TestCase):
  def test_initialization_of_empty_cult_board(self) -> None:
    cultBoard = cult.CultBoard(factions=[])
    for _, order in cultBoard.occupied_orders.items():
      self.assertFalse(order)
    for _, track in cultBoard.positions.items():
      self.assertFalse(track)

  def test_initialization_single_faction(self) -> None:
    halfling = faction.Halflings()
    cultBoard = cult.CultBoard(factions=[halfling])
    for _, order in cultBoard.occupied_orders.items():
      self.assertFalse(order)
    # faction.Halflings should be on earth and air.
    self.assertEqual(cultBoard.positions[common.CultTrack.EARTH],
                     {common.Terrain.PLAIN: 1})
    self.assertEqual(cultBoard.positions[common.CultTrack.AIR],
                     {common.Terrain.PLAIN: 1})
    self.assertEqual(cultBoard.positions[common.CultTrack.FIRE],
                     {common.Terrain.PLAIN: 0})
    self.assertEqual(cultBoard.positions[common.CultTrack.WATER],
                     {common.Terrain.PLAIN: 0})

  def test_initialization_multiple_factions(self) -> None:

    halfling = faction.Halflings()
    engineer = faction.Engineers()
    cultBoard = cult.CultBoard(factions=[halfling, engineer])

    for _, order in cultBoard.occupied_orders.items():
      self.assertFalse(order)
    # faction.Halflings should be on earth and air.
    # faction.Engineers will be zero everywhere.
    self.assertEqual(cultBoard.positions[common.CultTrack.EARTH], {
        common.Terrain.PLAIN: 1,
        common.Terrain.MOUNTAIN: 0
    })
    self.assertEqual(cultBoard.positions[common.CultTrack.AIR], {
        common.Terrain.PLAIN: 1,
        common.Terrain.MOUNTAIN: 0
    })
    self.assertEqual(cultBoard.positions[common.CultTrack.FIRE], {
        common.Terrain.PLAIN: 0,
        common.Terrain.MOUNTAIN: 0
    })
    self.assertEqual(cultBoard.positions[common.CultTrack.WATER], {
        common.Terrain.PLAIN: 0,
        common.Terrain.MOUNTAIN: 0
    })

  def test_sacrifice_priest_to_order_overshoot_power(self) -> None:
    halfling = faction.Halflings()
    test_player = player.Player(name="test", player_faction=halfling)
    cultBoard = cult.CultBoard(factions=[halfling])

    # We move 3 spaces and gain 1 power, since we overshoot the 3 token.
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(test_player,
                                            common.CultTrack.EARTH), (3, 1))
    self.assertEqual(cultBoard.positions[common.CultTrack.EARTH],
                     {common.Terrain.PLAIN: 4})
    # We occupy the first place for the EARTH order.
    self.assertEqual(cultBoard.occupied_orders[common.CultTrack.EARTH],
                     {1: common.Terrain.PLAIN})

  def test_sacrifice_priest_to_order_land_on_power(self) -> None:
    halfling = faction.Halflings()
    test_player = player.Player(name="test", player_faction=halfling)
    cultBoard = cult.CultBoard(factions=[halfling])

    # We move 3 spaces and gain 1 power, since we land on 3.
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(test_player,
                                            common.CultTrack.FIRE), (3, 1))
    self.assertEqual(cultBoard.positions[common.CultTrack.FIRE],
                     {common.Terrain.PLAIN: 3})
    # We occupy the first place for the MOUNTAIN order.
    self.assertEqual(cultBoard.occupied_orders[common.CultTrack.FIRE],
                     {1: common.Terrain.PLAIN})

  def test_sacrifice_many_priests_town_keys(self) -> None:
    halfling = faction.Halflings()
    test_player = player.Player(name="test", player_faction=halfling)
    cultBoard = cult.CultBoard(factions=[halfling])

    # We move 3 spaces and gain 1 power, since we land on 4.
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(test_player,
                                            common.CultTrack.EARTH), (3, 1))
    # We move another 2 spaces and gain 2 power since we land on 6.
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(test_player,
                                            common.CultTrack.EARTH), (2, 2))
    # We move another 2 spaces and gain 2 power since we land on 8.
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(test_player,
                                            common.CultTrack.EARTH), (2, 2))

    # We move another 1 spaces and gain 0 power since we can't move past 9.
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(test_player,
                                            common.CultTrack.EARTH), (1, 0))

    # The cult orders are full by us.
    self.assertEqual(
        cultBoard.occupied_orders[common.CultTrack.EARTH], {
            1: common.Terrain.PLAIN,
            2: common.Terrain.PLAIN,
            3: common.Terrain.PLAIN,
            4: common.Terrain.PLAIN
        })

    # We can still try to move but fail.
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(test_player,
                                            common.CultTrack.EARTH), (0, 0))

    # We're at the 9th position.
    self.assertEqual(cultBoard.positions[common.CultTrack.EARTH],
                     {common.Terrain.PLAIN: 9})

    # We gain a town key and try to move (only 1) to 10.
    test_player.gain_town(common.TownKey.PRIEST)
    # Gain 3 power!
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(test_player,
                                            common.CultTrack.EARTH), (1, 3))
    # We're occupying the town! Woot!
    self.assertEqual(cultBoard.positions[common.CultTrack.EARTH],
                     {common.Terrain.PLAIN: 10})

  def test_cant_occupy_already_taken_town(self) -> None:
    factions = [faction.Halflings(), faction.Engineers()]
    player1 = player.Player(name="test", player_faction=factions[0])
    player2 = player.Player(name="test", player_faction=factions[1])
    cultBoard = cult.CultBoard(factions=factions)

    # Both players have town keys.
    player1.gain_town(common.TownKey.PRIEST)
    player2.gain_town(common.TownKey.CULT)

    # Halfling takes the earth track by 1 -> 4 -> 6 -> 8 -> 10
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(player1, common.CultTrack.EARTH),
        (3, 1))
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(player1, common.CultTrack.EARTH),
        (2, 2))
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(player1, common.CultTrack.EARTH),
        (2, 2))
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(player1, common.CultTrack.EARTH),
        (2, 3))

    # Now engineer tries by 0 -> 1 -> 2 -> ... -> 9 -> 9 ... -> 9.
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(player2, common.CultTrack.EARTH),
        (1, 0))
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(player2, common.CultTrack.EARTH),
        (1, 0))
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(player2, common.CultTrack.EARTH),
        (1, 1))
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(player2, common.CultTrack.EARTH),
        (1, 0))
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(player2, common.CultTrack.EARTH),
        (1, 2))
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(player2, common.CultTrack.EARTH),
        (1, 0))
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(player2, common.CultTrack.EARTH),
        (1, 2))
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(player2, common.CultTrack.EARTH),
        (1, 0))
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(player2, common.CultTrack.EARTH),
        (1, 0))

    # Try again, but even with the town-key, player will fail.
    self.assertEqual(
        cultBoard.sacrifice_priest_to_order(player2, common.CultTrack.EARTH),
        (0, 0))
    # Player still has town key.
    self.assertTrue(player2.use_town_key())

    # Positions of players.
    self.assertEqual(cultBoard.positions[common.CultTrack.EARTH], {
        common.Terrain.PLAIN: 10,
        common.Terrain.MOUNTAIN: 9
    })
