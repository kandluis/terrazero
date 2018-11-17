import unittest

from faction import *

class TestModule(unittest.TestCase):
  def testEmptyLinesToMap(self):
    self.assertEqual(GameBoard.LinesToMap([]), {})

  def testSingleLinesToMap(self):
    self.assertEqual(GameBoard.LinesToMap(["WATER, SWAMP, DESERT, WATER, PLAIN"]),
      {(0,0): Terrain.WATER, (0,1) : Terrain.WATER, (0,2): Terrain.SWAMP, (0,3): Terrain.SWAMP,
       (0,4): Terrain.DESERT, (0,5): Terrain.DESERT, (0,6): Terrain.WATER, (0,7): Terrain.WATER.WATER,
       (0,8): Terrain.PLAIN, (0,9) : Terrain.PLAIN})

  def testMultiLinesToMap(self):
    firstRow = "SWAMP, DESERT, LAKE"
    # Note that the second row is "interleaved" with the top row.
    secondRow =  "WASTELAND, FOREST"
    self.assertEqual(GameBoard.LinesToMap([firstRow, secondRow]), {
      (0,0) : Terrain.SWAMP, (0,1): Terrain.SWAMP, (0,2): Terrain.DESERT, (0,3): Terrain.DESERT, (0,4) : Terrain.LAKE, (0,5): Terrain.LAKE, 
      (1,0) : Terrain.WATER, (1,1): Terrain.WASTELAND, (1,2): Terrain.WASTELAND, (1,3): Terrain.FOREST, (1,4): Terrain.FOREST, (1,5): Terrain.WATER,
    })

class TestGameBoard(unittest.TestCase):
  def setUp(self):
    # The default gameboard. No test should make modifications to this. We do this only once
    # during set-up since we have to read from a file.
    self.default_board = GameBoard()

  def testDefaultGameTerrainEdgeCases(self):
    board = self.default_board
    # First row.
    self.assertEqual(board.GetTerrain("A", 1), Terrain.PLAIN) # First.
    self.assertEqual(board.GetTerrain("A", 2), Terrain.MOUNTAIN) # Second.
    self.assertEqual(board.GetTerrain("A", 12), Terrain.WASTELAND) # Second to last.
    self.assertEqual(board.GetTerrain("A", 13), Terrain.SWAMP) # Last.

    # Second row.
    self.assertEqual(board.GetTerrain("B", 1), Terrain.DESERT) # First.
    self.assertEqual(board.GetTerrain("B", 2), Terrain.WATER) # Second.
    self.assertEqual(board.GetTerrain("B", 11), Terrain.WATER) # Second to last.
    self.assertEqual(board.GetTerrain("B", 12), Terrain.DESERT) # Last

  def testDefaultGameBoardTerrainRandom(self):
    board = self.default_board

    # Random checks.
    self.assertEqual(board.GetTerrain("F", 4), Terrain.WATER)
    self.assertEqual(board.GetTerrain("F", 5), Terrain.DESERT)
    self.assertEqual(board.GetTerrain("F", 6), Terrain.FOREST)
    self.assertEqual(board.GetTerrain("D", 7), Terrain.LAKE)
    self.assertEqual(board.GetTerrain("I", 7), Terrain.DESERT)
    self.assertEqual(board.GetTerrain("I", 8), Terrain.WASTELAND)
    self.assertEqual(board.GetTerrain("I", 9), Terrain.MOUNTAIN)

  def testExtraWaterTileForEvenRows(self):
    board = self.default_board

    # We allow requesting the 13th column for these rows, but it's always water.
    self.assertEqual(board.GetTerrain('B', 13), Terrain.WATER)
    self.assertEqual(board.GetTerrain('D', 13), Terrain.WATER)
    self.assertEqual(board.GetTerrain('F', 13), Terrain.WATER)
    self.assertEqual(board.GetTerrain('H', 13), Terrain.WATER)


  def testDefaultGameBoardTerrainFailureCases(self):
    board = self.default_board

    with self.assertRaises(KeyError):
      board.GetTerrain(chr(ord("A") - 1), 1) # No such row.
    with self.assertRaises(KeyError):
      board.GetTerrain("J", 1) # No such row.
    with self.assertRaises(KeyError):
      board.GetTerrain("A", 0) # No such column.
    with self.assertRaises(KeyError):
      board.GetTerrain("I", 14) # No such column.

  def testDefaultGameBoardNeighborsCorners(self):
    board = self.default_board

    self.assertCountEqual(board.GetNeighborTiles("A", 1), {
      ("A", 2), ("B", 1) })
    # We technically allow a fictional water tile at B13 to be a neighbor.
    self.assertCountEqual(board.GetNeighborTiles("A", 13), {
      ("A", 12), ("B", 12), ("B", 13) })
    self.assertCountEqual(board.GetNeighborTiles("I", 1), {
      ("I", 2), ("H", 1) })
    # We technically allow a fictional water tile at G13 to be a neighbor.
    self.assertCountEqual(board.GetNeighborTiles("I", 13), {
      ("I", 12), ("H", 12), ("H", 13)})

  def testDefaultGameBoardNeighborsEdge(self):
    board = self.default_board

  def testDefaultGameBoardNeighborsMiddle(self):
    boad = self.default_board

class TestHalflingFaction(unittest.TestCase):
  def testCreation(self):
    halfing = Halflings()

class TestPlayer(unittest.TestCase):
  def testPlayerGainingSinglePower(self):
    faction = Halflings()
    player = Player(faction)

    # Starting configuration for the given class.
    self.assertEqual(player.power, {
      PowerBowl.I : 3, PowerBowl.II: 9, PowerBowl.III: 0
      })
    self.assertEqual(player.coins, 15)

    self.assertIsNone(player.GainPower(1))
    self.assertEqual(player.power, {
      PowerBowl.I: 2, PowerBowl.II: 10, PowerBowl.III: 0
      })
    self.assertEqual(player.coins, 15)

  def testPlayerGainingRolloverPower(self):
    faction = Halflings()
    player = Player(faction)

    # Starting configuration for the given class.
    self.assertEqual(player.power, {
      PowerBowl.I: 3, PowerBowl.II: 9, PowerBowl.III: 0
      })
    self.assertEqual(player.coins, 15)

    self.assertIsNone(player.GainPower(4))
    self.assertEqual(player.power, {
      PowerBowl.I: 0, PowerBowl.II: 11, PowerBowl.III: 1
      })
    self.assertEqual(player.coins, 15)

  def testPlayerGainingMaxPower(self):
    faction = Halflings()
    player = Player(faction)

    # Starting configuration for the given class.
    self.assertEqual(player.power, {
      PowerBowl.I : 3, PowerBowl.II: 9, PowerBowl.III: 0
      })
    self.assertEqual(player.coins, 15)

    self.assertIsNone(player.GainPower(15))
    self.assertEqual(player.power, {
      PowerBowl.I: 0, PowerBowl.II: 0, PowerBowl.III: 12
      })
    self.assertEqual(player.coins, 15)

  def testPlayerGainingMaxPowerPlusEvenValue(self):
    faction = Halflings()
    player = Player(faction)

    # Starting configuration for the given class.
    self.assertEqual(player.power, {
      PowerBowl.I : 3, PowerBowl.II: 9, PowerBowl.III: 0
      })
    self.assertEqual(player.coins, 15)

    # 15 gets us to max, the extra 4 power is converted into 2 coins.
    self.assertIsNone(player.GainPower(19))
    self.assertEqual(player.power, {
      PowerBowl.I: 0, PowerBowl.II: 0, PowerBowl.III: 12
      })
    self.assertEqual(player.coins, 17)

  def testPlayerGainingMaxPowerPlusOddValue(self):
    faction = Halflings()
    player = Player(faction)

    # Starting configuration for the given class.
    self.assertEqual(player.power, {
      PowerBowl.I : 3, PowerBowl.II: 9, PowerBowl.III: 0
      })
    self.assertEqual(player.coins, 15)

    # 15 gets us to max, the extra 3 power is converted into 2 coins.
    # Even though this may not be optimal.
    self.assertIsNone(player.GainPower(18))
    self.assertEqual(player.power, {
      PowerBowl.I: 0, PowerBowl.II: 1, PowerBowl.III: 11
      })
    self.assertEqual(player.coins, 17)

class TestCultBoard(unittest.TestCase):
  def testInitializationOfEmptyCultBoard(self):
    cult = CultBoard(factions=[])
    for _, order in cult.occupied_orders.items():
      self.assertFalse(order)
    for _, track in cult.positions.items():
      self.assertFalse(track)

  def testInitializationSingleFaction(self):
    halfling = Halflings()
    cultBoard = CultBoard(factions=[halfling])
    for _, order in cultBoard.occupied_orders.items():
      self.assertFalse(order)
    # Halflings should be on earth and air.
    self.assertEqual(cultBoard.positions[CultTrack.EARTH], {
      Terrain.PLAIN: 1
      })
    self.assertEqual(cultBoard.positions[CultTrack.AIR], {
      Terrain.PLAIN: 1
    })
    self.assertEqual(cultBoard.positions[CultTrack.FIRE], {
      Terrain.PLAIN: 0
      })
    self.assertEqual(cultBoard.positions[CultTrack.WATER], {
      Terrain.PLAIN: 0
      })


  def testInitializationMultipleFactions(self):
    
    halfling = Halflings()
    engineer = Engineers()
    cultBoard = CultBoard(factions=[halfling, engineer])

    for _, order in cultBoard.occupied_orders.items():
      self.assertFalse(order)
    # Halflings should be on earth and air.
    # Engineers will be zero everywhere.
    self.assertEqual(cultBoard.positions[CultTrack.EARTH], {
      Terrain.PLAIN: 1,
      Terrain.MOUNTAIN: 0
      })
    self.assertEqual(cultBoard.positions[CultTrack.AIR], {
      Terrain.PLAIN: 1,
      Terrain.MOUNTAIN: 0
    })
    self.assertEqual(cultBoard.positions[CultTrack.FIRE], {
      Terrain.PLAIN: 0,
      Terrain.MOUNTAIN: 0
      })
    self.assertEqual(cultBoard.positions[CultTrack.WATER], {
      Terrain.PLAIN: 0,
      Terrain.MOUNTAIN: 0
      })

  def testSacrificePriestToOrderOvershootPower(self):
    halfling = Halflings()
    player = Player(faction=halfling)
    cultBoard = CultBoard(factions=[halfling])

    # We move 3 spaces and gain 1 power, since we overshoot the 3 token.
    self.assertEqual(cultBoard.SacrificePriestToOrder(player, CultTrack.EARTH),
      (3, 1))
    self.assertEqual(cultBoard.positions[CultTrack.EARTH], {
        Terrain.PLAIN: 4
      })
    # We occupy the first place for the EARTH order.
    self.assertEqual(cultBoard.occupied_orders[CultTrack.EARTH], {
      1: Terrain.PLAIN
      })

  def testSacrificePriestToOrderLandOnPower(self):
    halfling = Halflings()
    player = Player(faction=halfling)
    cultBoard = CultBoard(factions=[halfling])

    # We move 3 spaces and gain 1 power, since we land on 3.
    self.assertEqual(cultBoard.SacrificePriestToOrder(player, CultTrack.FIRE),
      (3, 1))
    self.assertEqual(cultBoard.positions[CultTrack.FIRE], {
        Terrain.PLAIN: 3
      })
    # We occupy the first place for the MOUNTAIN order.
    self.assertEqual(cultBoard.occupied_orders[CultTrack.FIRE], {
      1: Terrain.PLAIN
      })

  def testSacrificeManyPriestsTownKeys(self):
    halfling = Halflings()
    player = Player(faction=halfling)
    cultBoard = CultBoard(factions=[halfling])

    # We move 3 spaces and gain 1 power, since we land on 4.
    self.assertEqual(cultBoard.SacrificePriestToOrder(player, CultTrack.EARTH),
      (3, 1))
    # We move another 2 spaces and gain 2 power since we land on 6. 
    self.assertEqual(cultBoard.SacrificePriestToOrder(player, CultTrack.EARTH),
      (2, 2))
    # We move another 2 spaces and gain 2 power since we land on 8. 
    self.assertEqual(cultBoard.SacrificePriestToOrder(player, CultTrack.EARTH),
      (2, 2))

    # We move another 1 spaces and gain 0 power since we can't move past 9.
    self.assertEqual(cultBoard.SacrificePriestToOrder(player, CultTrack.EARTH),
      (1, 0))

    # The cult orders are full by us. 
    self.assertEqual(cultBoard.occupied_orders[CultTrack.EARTH], {
      1: Terrain.PLAIN, 2: Terrain.PLAIN, 3: Terrain.PLAIN, 4: Terrain.PLAIN
      })

    # We can still try to move but fail.
    self.assertEqual(cultBoard.SacrificePriestToOrder(player, CultTrack.EARTH),
      (0, 0))

    # We're at the 9th position.
    self.assertEqual(cultBoard.positions[CultTrack.EARTH], {
      Terrain.PLAIN: 9
      })

    # We gain a town key and try to move (only 1) to 10.
    self.assertIsNone(player.GainTown(TownKey.PRIEST))
    # Gain 3 power!
    self.assertEqual(cultBoard.SacrificePriestToOrder(player, CultTrack.EARTH),
      (1, 3))
    # We're occupying the town! Woot!
    self.assertEqual(cultBoard.positions[CultTrack.EARTH], {
        Terrain.PLAIN: 10
      })

  def testCantOccupyAlreadyTakenTown(self):
    factions = [Halflings(), Engineers()]
    player1 = Player(faction=factions[0])
    player2 = Player(faction=factions[1])
    cultBoard = CultBoard(factions=factions)

    # Both players have town keys.
    self.assertIsNone(player1.GainTown(TownKey.PRIEST))
    self.assertIsNone(player2.GainTown(TownKey.CULT))

    # Halfling takes the earth track by 1 -> 4 -> 6 -> 8 -> 10
    self.assertEqual(cultBoard.SacrificePriestToOrder(player1, CultTrack.EARTH),
      (3, 1))
    self.assertEqual(cultBoard.SacrificePriestToOrder(player1, CultTrack.EARTH),
      (2, 2))
    self.assertEqual(cultBoard.SacrificePriestToOrder(player1, CultTrack.EARTH),
      (2, 2))
    self.assertEqual(cultBoard.SacrificePriestToOrder(player1, CultTrack.EARTH),
      (2, 3))

    # Now engineer tries by 0 -> 1 -> 2 -> ... -> 9 -> 9 ... -> 9.
    self.assertEqual(cultBoard.SacrificePriestToOrder(player2, CultTrack.EARTH), 
      (1,0))
    self.assertEqual(cultBoard.SacrificePriestToOrder(player2, CultTrack.EARTH), 
      (1,0))
    self.assertEqual(cultBoard.SacrificePriestToOrder(player2, CultTrack.EARTH), 
      (1,1))
    self.assertEqual(cultBoard.SacrificePriestToOrder(player2, CultTrack.EARTH), 
      (1,0))
    self.assertEqual(cultBoard.SacrificePriestToOrder(player2, CultTrack.EARTH), 
      (1,2))
    self.assertEqual(cultBoard.SacrificePriestToOrder(player2, CultTrack.EARTH), 
      (1,0))
    self.assertEqual(cultBoard.SacrificePriestToOrder(player2, CultTrack.EARTH), 
      (1,2))
    self.assertEqual(cultBoard.SacrificePriestToOrder(player2, CultTrack.EARTH), 
      (1,0))
    self.assertEqual(cultBoard.SacrificePriestToOrder(player2, CultTrack.EARTH), 
      (1,0))

    # Try again, but even with the town-key, player will fail.
    self.assertEqual(cultBoard.SacrificePriestToOrder(player2, CultTrack.EARTH), 
      (0,0))
    # Player still has town key.
    self.assertTrue(player2.UseTownKey())

    # Positions of players. 
    self.assertEqual(cultBoard.positions[CultTrack.EARTH], {
      Terrain.PLAIN: 10,
      Terrain.MOUNTAIN: 9
      })



if __name__ == '__main__':
  unittest.main()