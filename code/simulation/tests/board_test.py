import unittest

from simulation.core import board
from simulation.core import common


class TestGameBoardModule(unittest.TestCase):
  def testEmptyLinesToMap(self):
    self.assertEqual(board.GameBoard.LinesToMap([]), {})

  def testSingleLinesToMap(self):
    self.assertEqual(
        board.GameBoard.LinesToMap(["WATER, SWAMP, DESERT, WATER, PLAIN"]), {
            (0, 0): common.Terrain.WATER,
            (0, 1): common.Terrain.WATER,
            (0, 2): common.Terrain.SWAMP,
            (0, 3): common.Terrain.SWAMP,
            (0, 4): common.Terrain.DESERT,
            (0, 5): common.Terrain.DESERT,
            (0, 6): common.Terrain.WATER,
            (0, 7): common.Terrain.WATER.WATER,
            (0, 8): common.Terrain.PLAIN,
            (0, 9): common.Terrain.PLAIN
        })

  def testMultiLinesToMap(self):
    firstRow = "SWAMP, DESERT, LAKE"
    # Note that the second row is "interleaved" with the top row.
    secondRow = "WASTELAND, FOREST"
    self.assertEqual(
        board.GameBoard.LinesToMap([firstRow, secondRow]), {
            (0, 0): common.Terrain.SWAMP,
            (0, 1): common.Terrain.SWAMP,
            (0, 2): common.Terrain.DESERT,
            (0, 3): common.Terrain.DESERT,
            (0, 4): common.Terrain.LAKE,
            (0, 5): common.Terrain.LAKE,
            (1, 0): common.Terrain.WATER,
            (1, 1): common.Terrain.WASTELAND,
            (1, 2): common.Terrain.WASTELAND,
            (1, 3): common.Terrain.FOREST,
            (1, 4): common.Terrain.FOREST,
            (1, 5): common.Terrain.WATER,
        })


class TestGameBoard(unittest.TestCase):
  def setUp(self):
    # The default gameboard. No test should make modifications to this. We do this only once
    # during set-up since we have to read from a file.
    self.default_board = board.GameBoard()

  def testDefaultGameTerrainEdgeCases(self):
    # First row.
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="A", column=1)),
        common.Terrain.PLAIN)  # First.
    # Second.
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="A", column=2)),
        common.Terrain.MOUNTAIN)
    # Second to last.
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="A", column=12)),
        common.Terrain.WASTELAND)
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="A", column=13)),
        common.Terrain.SWAMP)  # Last.

    # Second row.
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="B", column=1)),
        common.Terrain.DESERT)  # First.
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="B", column=2)),
        common.Terrain.WATER)  # Second.
    # Second to last.
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="B", column=11)),
        common.Terrain.WATER)
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="B", column=12)),
        common.Terrain.DESERT)  # Last

  def testDefaultGameBoardTerrainRandom(self):

    # Random checks.
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="F", column=4)),
        common.Terrain.WATER)
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="F", column=5)),
        common.Terrain.DESERT)
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="F", column=6)),
        common.Terrain.FOREST)
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="D", column=7)),
        common.Terrain.LAKE)
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="I", column=7)),
        common.Terrain.DESERT)
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="I", column=8)),
        common.Terrain.WASTELAND)
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="I", column=9)),
        common.Terrain.MOUNTAIN)

  def testExtraWaterTileForEvenRows(self):

    # We allow requesting the 13th column for these rows, but it's always
    # water.
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="B", column=13)),
        common.Terrain.WATER)
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="D", column=13)),
        common.Terrain.WATER)
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="F", column=13)),
        common.Terrain.WATER)
    self.assertEqual(
        self.default_board.GetTerrain(board.Position(row="H", column=13)),
        common.Terrain.WATER)

  def testDefaultGameBoardTerrainFailureCases(self):
    with self.assertRaises(KeyError):
      self.default_board.GetTerrain(
          board.Position(row=chr(ord("A") - 1), column=1))  # No such row.
    with self.assertRaises(KeyError):
      self.default_board.GetTerrain(board.Position(row="J",
                                                   column=1))  # No such row.
    with self.assertRaises(KeyError):
      self.default_board.GetTerrain(board.Position(
          row="A", column=0))  # No such column.
    with self.assertRaises(KeyError):
      self.default_board.GetTerrain(board.Position(
          row="I", column=14))  # No such column.

  def testDefaultGameBoardNeighborsCorners(self):

    self.assertCountEqual(
        self.default_board.GetNeighborTiles(board.Position(row="A", column=1)),
        {("A", 2), ("B", 1)})
    # We technically allow a fictional water tile at B13 to be a neighbor.
    self.assertCountEqual(
        self.default_board.GetNeighborTiles(
            board.Position(row="A", column=13)), {("A", 12), ("B", 12),
                                                  ("B", 13)})
    self.assertCountEqual(
        self.default_board.GetNeighborTiles(board.Position(row="I", column=1)),
        {("I", 2), ("H", 1)})
    # We technically allow a fictional water tile at G13 to be a neighbor.
    self.assertCountEqual(
        self.default_board.GetNeighborTiles(
            board.Position(row="I", column=13)), {("I", 12), ("H", 12),
                                                  ("H", 13)})

  def testDefaultGameBoardNeighborsEdge(self):
    pass

  def testDefaultGameBoardNeighborsMiddle(self):
    pass
