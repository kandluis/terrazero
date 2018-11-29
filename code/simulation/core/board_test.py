import unittest

from simulation.core import board
from simulation.core import common
from simulation import utils


class TestPosition(unittest.TestCase):
  def testInitialization(self):
    pos = board.Position(row='row', column=1)
    self.assertEqual('row', pos.row)
    self.assertEqual(1, pos.column)

  def testParsePosition(self):
    self.assertEqual(
        board.ParsePosition("A13"), board.Position(row="A", column=13))
    self.assertEqual(
        board.ParsePosition("I1"), board.Position(row="I", column=1))

  def testParsePositionFailure(self):
    self.assertIsNone(board.ParsePosition("J1"))
    self.assertIsNone(board.ParsePosition("A14"))


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

  def testCanBeBuiltBasic(self):
    # Swamps can be built on A13.
    self.assertTrue(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A13"), common.Structure.DWELLING,
            [common.Terrain.SWAMP]))
    # We can build as long as one of the terrains can be built.DWELLING
    self.assertTrue(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A13"), common.Structure.DWELLING,
            [common.Terrain.MOUNTAIN, common.Terrain.SWAMP]))

    # But we can't build anything other than a dwelling.DWELLING
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A13"), common.Structure.TRADING_POST,
            [common.Terrain.SWAMP]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A13"), common.Structure.TEMPLE,
            [common.Terrain.SWAMP]))

    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A13"), common.Structure.SANCTUARY,
            [common.Terrain.SWAMP]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A13"), common.Structure.STRONGHOLD,
            [common.Terrain.SWAMP]))

    # We also can't build anything that's not our terrain.
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A13"), common.Structure.DWELLING,
            [common.Terrain.MOUNTAIN]))

  def testCannotBuildOnWater(self):
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("B2"), common.Structure.DWELLING, [
                common.Terrain.MOUNTAIN, common.Terrain.SWAMP,
                common.Terrain.PLAIN, common.Terrain.LAKE,
                common.Terrain.DESERT, common.Terrain.FOREST
            ]))

  def testBuildDwelling(self):
    # Let's build a dwelling.
    self.default_board.Build(
        board.ParsePosition("A1"), common.Structure.DWELLING)
    self.assertEqual(
        self.default_board.GetStructure(board.ParsePosition("A1")),
        common.Structure.DWELLING)

    # We can now build a trading post.
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.DWELLING,
            [common.Terrain.PLAIN]))
    self.assertTrue(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.TRADING_POST,
            [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.TEMPLE,
            [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.SANCTUARY,
            [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.STRONGHOLD,
            [common.Terrain.PLAIN]))

  def testBuildTradingPost(self):
    # Let's build a dwelling and trading post.
    self.default_board.Build(
        board.ParsePosition("A1"), common.Structure.DWELLING)
    self.default_board.Build(
        board.ParsePosition("A1"), common.Structure.TRADING_POST)
    self.assertEqual(
        self.default_board.GetStructure(board.ParsePosition("A1")),
        common.Structure.TRADING_POST)

    # We can now build either a temple or stronghold.
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.DWELLING,
            [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.TRADING_POST,
            [common.Terrain.PLAIN]))
    self.assertTrue(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.TEMPLE,
            [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.SANCTUARY,
            [common.Terrain.PLAIN]))
    self.assertTrue(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.STRONGHOLD,
            [common.Terrain.PLAIN]))

  def testBuildTemple(self):
    # Let's build a dwelling and trading post.
    self.default_board.Build(
        board.ParsePosition("A1"), common.Structure.DWELLING)
    self.default_board.Build(
        board.ParsePosition("A1"), common.Structure.TRADING_POST)
    self.default_board.Build(
        board.ParsePosition("A1"), common.Structure.TEMPLE)
    self.assertEqual(
        self.default_board.GetStructure(board.ParsePosition("A1")),
        common.Structure.TEMPLE)

    # We can now build a sanctuary.
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.DWELLING,
            [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.TRADING_POST,
            [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.TEMPLE,
            [common.Terrain.PLAIN]))
    self.assertTrue(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.SANCTUARY,
            [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.STRONGHOLD,
            [common.Terrain.PLAIN]))

  def testBuildSanctuary(self):
    # Let's build a dwelling and trading post.
    self.default_board.Build(
        board.ParsePosition("A1"), common.Structure.DWELLING)
    self.default_board.Build(
        board.ParsePosition("A1"), common.Structure.TRADING_POST)
    self.default_board.Build(
        board.ParsePosition("A1"), common.Structure.TEMPLE)
    self.default_board.Build(
        board.ParsePosition("A1"), common.Structure.SANCTUARY)
    self.assertEqual(
        self.default_board.GetStructure(board.ParsePosition("A1")),
        common.Structure.SANCTUARY)

    # We can build nothing!
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.DWELLING,
            [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.TRADING_POST,
            [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.TEMPLE,
            [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.SANCTUARY,
            [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.STRONGHOLD,
            [common.Terrain.PLAIN]))

  def testBuildStrongHold(self):
    # Let's build a dwelling and trading post.
    self.default_board.Build(
        board.ParsePosition("A1"), common.Structure.DWELLING)
    self.default_board.Build(
        board.ParsePosition("A1"), common.Structure.TRADING_POST)
    self.default_board.Build(
        board.ParsePosition("A1"), common.Structure.STRONGHOLD)
    self.assertEqual(
        self.default_board.GetStructure(board.ParsePosition("A1")),
        common.Structure.STRONGHOLD)

    # We can build nothing!
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.DWELLING,
            [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.TRADING_POST,
            [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.TEMPLE,
            [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.SANCTUARY,
            [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.CanBeBuilt(
            board.ParsePosition("A1"), common.Structure.STRONGHOLD,
            [common.Terrain.PLAIN]))

  def testBuildFailures(self):
    with self.assertRaises(utils.InternalError):
      self.default_board.Build(
          board.ParsePosition("A1"), common.Structure.TRADING_POST)

    self.default_board.Build(
        board.ParsePosition("A1"), common.Structure.DWELLING)
    with self.assertRaises(utils.InternalError):
      self.default_board.Build(
          board.ParsePosition("A1"), common.Structure.TEMPLE)

    self.default_board.Build(
        board.ParsePosition("A1"), common.Structure.TRADING_POST)
    self.default_board.Build(
        board.ParsePosition("A1"), common.Structure.TEMPLE)
    with self.assertRaises(utils.InternalError):
      self.default_board.Build(
          board.ParsePosition("A1"), common.Structure.STRONGHOLD)

  def testDefaultGameBoardNeighbors(self):
    # We include the pseudo-tile 'b13'
    self.assertCountEqual(
        self.default_board.GetNeighborTiles(board.ParsePosition("A13")), [
            board.ParsePosition("A12"),
            board.ParsePosition("B12"),
            board.ParsePosition("B13"),
        ])
    self.assertCountEqual(
        self.default_board.GetNeighborTiles(board.ParsePosition("E1")), [
            board.ParsePosition("F1"),
            board.ParsePosition("E2"),
            board.ParsePosition("D1")
        ])
    self.assertCountEqual(
        self.default_board.GetNeighborTiles(board.ParsePosition("E6")), [
            board.ParsePosition("E5"),
            board.ParsePosition("D5"),
            board.ParsePosition("D6"),
            board.ParsePosition("E7"),
            board.ParsePosition("F6"),
            board.ParsePosition("F5")
        ])

  def testDefaultGameBoardNeighbordStructureOwners(self):
    # No structures anywhere!
    self.assertTrue(
        len(
            self.default_board.NeighborStructureOwners(
                board.ParsePosition("A13"))) == 0)

    # We build some structures.
    self.default_board.Build(
        board.ParsePosition("A12"), common.Structure.DWELLING)
    self.default_board.Build(
        board.ParsePosition("B12"), common.Structure.DWELLING)

    self.assertCountEqual(
        self.default_board.NeighborStructureOwners(board.ParsePosition("A13")),
        [
            (common.Structure.DWELLING, common.Terrain.WASTELAND),
            (common.Structure.DWELLING, common.Terrain.DESERT),
        ])