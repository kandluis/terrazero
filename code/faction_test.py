import unittest

from faction import Terrain, GameBoard

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

if __name__ == '__main__':
  unittest.main()