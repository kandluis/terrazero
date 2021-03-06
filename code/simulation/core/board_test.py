import unittest

from simulation.core import board
from simulation.core import common
from simulation import utils


class TestPosition(unittest.TestCase):
  def test_initialization(self) -> None:
    pos = board.Position(row='row', column=1)
    self.assertEqual('row', pos.row)
    self.assertEqual(1, pos.column)

  def test_parse_position(self) -> None:
    self.assertEqual(board.ParsePosition("A13"),
                     board.Position(row="A", column=13))
    self.assertEqual(board.ParsePosition("I1"),
                     board.Position(row="I", column=1))

  def test_parse_position_failure(self) -> None:
    self.assertIsNone(board.ParsePosition("J1"))
    self.assertIsNone(board.ParsePosition("A14"))


class TestGameBoardModule(unittest.TestCase):
  def test_empty_lines_to_map(self) -> None:
    self.assertEqual(board.GameBoard.lines_to_map([]), {})

  def test_single_lines_to_map(self) -> None:
    self.assertEqual(
        board.GameBoard.lines_to_map(["WATER, SWAMP, DESERT, WATER, PLAIN"]), {
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

  def test_multi_lines_to_map(self) -> None:
    firstRow = "SWAMP, DESERT, LAKE"
    # Note that the second row is "interleaved" with the top row.
    secondRow = "WASTELAND, FOREST"
    self.assertEqual(
        board.GameBoard.lines_to_map([firstRow, secondRow]), {
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
  def setUp(self) -> None:
    # The default gameboard. No test should make modifications to this. We do
    # this only once during set-up since we have to read from a file.
    self.default_board = board.GameBoard()

  def test_default_game_terrain_edge_cases(self) -> None:
    # First row.
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="A", column=1)),
        common.Terrain.PLAIN)  # First.
    # Second.
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="A", column=2)),
        common.Terrain.MOUNTAIN)
    # Second to last.
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="A", column=12)),
        common.Terrain.WASTELAND)
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="A", column=13)),
        common.Terrain.SWAMP)  # Last.

    # Second row.
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="B", column=1)),
        common.Terrain.DESERT)  # First.
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="B", column=2)),
        common.Terrain.WATER)  # Second.
    # Second to last.
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="B", column=11)),
        common.Terrain.WATER)
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="B", column=12)),
        common.Terrain.DESERT)  # Last

  def test_default_game_bard_terrain_random(self) -> None:

    # Random checks.
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="F", column=4)),
        common.Terrain.WATER)
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="F", column=5)),
        common.Terrain.DESERT)
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="F", column=6)),
        common.Terrain.FOREST)
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="D", column=7)),
        common.Terrain.LAKE)
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="I", column=7)),
        common.Terrain.DESERT)
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="I", column=8)),
        common.Terrain.WASTELAND)
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="I", column=9)),
        common.Terrain.MOUNTAIN)

  def test_extra_water_tile_for_even_rows(self) -> None:

    # We allow requesting the 13th column for these rows, but it's always
    # water.
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="B", column=13)),
        common.Terrain.WATER)
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="D", column=13)),
        common.Terrain.WATER)
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="F", column=13)),
        common.Terrain.WATER)
    self.assertEqual(
        self.default_board.get_terrain(board.Position(row="H", column=13)),
        common.Terrain.WATER)

  def test_default_game_board_terrain_failure_cases(self) -> None:
    with self.assertRaises(KeyError):
      self.default_board.get_terrain(
          board.Position(row=chr(ord("A") - 1), column=1))  # No such row.
    with self.assertRaises(KeyError):
      self.default_board.get_terrain(board.Position(row="J",
                                                    column=1))  # No such row.
    with self.assertRaises(KeyError):
      self.default_board.get_terrain(board.Position(
          row="A", column=0))  # No such column.
    with self.assertRaises(KeyError):
      self.default_board.get_terrain(board.Position(
          row="I", column=14))  # No such column.

  def test_default_game_board_neighbors_corners(self) -> None:

    self.assertCountEqual(
        self.default_board.get_neighbor_tiles(board.Position(row="A",
                                                             column=1)),
        {("A", 2), ("B", 1)})
    # We technically allow a fictional water tile at B13 to be a neighbor.
    self.assertCountEqual(
        self.default_board.get_neighbor_tiles(
            board.Position(row="A", column=13)), {("A", 12), ("B", 12),
                                                  ("B", 13)})
    self.assertCountEqual(
        self.default_board.get_neighbor_tiles(board.Position(row="I",
                                                             column=1)),
        {("I", 2), ("H", 1)})
    # We technically allow a fictional water tile at G13 to be a neighbor.
    self.assertCountEqual(
        self.default_board.get_neighbor_tiles(
            board.Position(row="I", column=13)), {("I", 12), ("H", 12),
                                                  ("H", 13)})

  def testcan_be_built_basic(self) -> None:
    # Swamps can be built on A13.
    a13 = board.ParsePosition("A13")
    assert a13 is not None
    self.assertTrue(
        self.default_board.can_be_built(a13, common.Structure.DWELLING,
                                        [common.Terrain.SWAMP]))
    # We can build as long as one of the terrains can be built.DWELLING
    self.assertTrue(
        self.default_board.can_be_built(
            a13, common.Structure.DWELLING,
            [common.Terrain.MOUNTAIN, common.Terrain.SWAMP]))

    # But we can't build anything other than a dwelling.DWELLING
    self.assertFalse(
        self.default_board.can_be_built(a13, common.Structure.TRADING_POST,
                                        [common.Terrain.SWAMP]))
    self.assertFalse(
        self.default_board.can_be_built(a13, common.Structure.TEMPLE,
                                        [common.Terrain.SWAMP]))

    self.assertFalse(
        self.default_board.can_be_built(a13, common.Structure.SANCTUARY,
                                        [common.Terrain.SWAMP]))
    self.assertFalse(
        self.default_board.can_be_built(a13, common.Structure.STRONGHOLD,
                                        [common.Terrain.SWAMP]))

    # We also can't build anything that's not our terrain.
    self.assertFalse(
        self.default_board.can_be_built(a13, common.Structure.DWELLING,
                                        [common.Terrain.MOUNTAIN]))

  def test_cannot_build_on_water(self) -> None:
    b2 = board.ParsePosition("B2")
    assert b2 is not None
    self.assertFalse(
        self.default_board.can_be_built(b2, common.Structure.DWELLING, [
            common.Terrain.MOUNTAIN, common.Terrain.SWAMP,
            common.Terrain.PLAIN, common.Terrain.LAKE, common.Terrain.DESERT,
            common.Terrain.FOREST
        ]))

  def test_build_dwelling(self) -> None:
    # Let's build a dwelling.
    a1 = board.ParsePosition("A1")
    assert a1 is not None
    self.default_board.build(a1, common.Structure.DWELLING)
    self.assertEqual(self.default_board.get_structure(a1),
                     common.Structure.DWELLING)

    # We can now build a trading post.
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.DWELLING,
                                        [common.Terrain.PLAIN]))
    self.assertTrue(
        self.default_board.can_be_built(a1, common.Structure.TRADING_POST,
                                        [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.TEMPLE,
                                        [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.SANCTUARY,
                                        [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.STRONGHOLD,
                                        [common.Terrain.PLAIN]))

  def test_build_trading_post(self) -> None:
    # Let's build a dwelling and trading post.
    a1 = board.ParsePosition("A1")
    assert a1 is not None
    self.default_board.build(a1, common.Structure.DWELLING)
    self.default_board.build(a1, common.Structure.TRADING_POST)
    self.assertEqual(self.default_board.get_structure(a1),
                     common.Structure.TRADING_POST)

    # We can now build either a temple or stronghold.
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.DWELLING,
                                        [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.TRADING_POST,
                                        [common.Terrain.PLAIN]))
    self.assertTrue(
        self.default_board.can_be_built(a1, common.Structure.TEMPLE,
                                        [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.SANCTUARY,
                                        [common.Terrain.PLAIN]))
    self.assertTrue(
        self.default_board.can_be_built(a1, common.Structure.STRONGHOLD,
                                        [common.Terrain.PLAIN]))

  def test_build_temple(self) -> None:
    # Let's build a dwelling and trading post.
    a1 = board.ParsePosition("A1")
    assert a1 is not None
    self.default_board.build(a1, common.Structure.DWELLING)
    self.default_board.build(a1, common.Structure.TRADING_POST)
    self.default_board.build(a1, common.Structure.TEMPLE)
    self.assertEqual(self.default_board.get_structure(a1),
                     common.Structure.TEMPLE)

    # We can now build a sanctuary.
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.DWELLING,
                                        [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.TRADING_POST,
                                        [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.TEMPLE,
                                        [common.Terrain.PLAIN]))
    self.assertTrue(
        self.default_board.can_be_built(a1, common.Structure.SANCTUARY,
                                        [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.STRONGHOLD,
                                        [common.Terrain.PLAIN]))

  def test_build_sanctuary(self) -> None:
    # Let's build a dwelling and trading post.
    a1 = board.ParsePosition("A1")
    assert a1 is not None
    self.default_board.build(a1, common.Structure.DWELLING)
    self.default_board.build(a1, common.Structure.TRADING_POST)
    self.default_board.build(a1, common.Structure.TEMPLE)
    self.default_board.build(a1, common.Structure.SANCTUARY)
    self.assertEqual(self.default_board.get_structure(a1),
                     common.Structure.SANCTUARY)

    # We can build nothing!
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.DWELLING,
                                        [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.TRADING_POST,
                                        [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.TEMPLE,
                                        [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.SANCTUARY,
                                        [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.STRONGHOLD,
                                        [common.Terrain.PLAIN]))

  def test_build_strong_hold(self) -> None:
    # Let's build a dwelling and trading post.
    a1 = board.ParsePosition("A1")
    assert a1 is not None
    self.default_board.build(a1, common.Structure.DWELLING)
    self.default_board.build(a1, common.Structure.TRADING_POST)
    self.default_board.build(a1, common.Structure.STRONGHOLD)
    self.assertEqual(self.default_board.get_structure(a1),
                     common.Structure.STRONGHOLD)

    # We can build nothing!
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.DWELLING,
                                        [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.TRADING_POST,
                                        [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.TEMPLE,
                                        [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.SANCTUARY,
                                        [common.Terrain.PLAIN]))
    self.assertFalse(
        self.default_board.can_be_built(a1, common.Structure.STRONGHOLD,
                                        [common.Terrain.PLAIN]))

  def test_build_failures(self) -> None:
    a1 = board.ParsePosition("A1")
    assert a1 is not None
    with self.assertRaises(utils.InternalError):
      self.default_board.build(a1, common.Structure.TRADING_POST)

    self.default_board.build(a1, common.Structure.DWELLING)
    with self.assertRaises(utils.InternalError):
      self.default_board.build(a1, common.Structure.TEMPLE)

    self.default_board.build(a1, common.Structure.TRADING_POST)
    self.default_board.build(a1, common.Structure.TEMPLE)
    with self.assertRaises(utils.InternalError):
      self.default_board.build(a1, common.Structure.STRONGHOLD)

  def test_default_game_board_neighbors(self) -> None:
    # We include the pseudo-tile 'b13'
    a13 = board.ParsePosition("A13")
    assert a13 is not None
    a12 = board.ParsePosition("A12")
    assert a12 is not None
    b12 = board.ParsePosition("B12")
    assert b12 is not None
    b13 = board.ParsePosition("B13")
    assert b13 is not None
    self.assertCountEqual(self.default_board.get_neighbor_tiles(a13), [
        a12,
        b12,
        b13,
    ])

    e1 = board.ParsePosition("E1")
    assert e1 is not None
    f1 = board.ParsePosition("F1")
    assert f1 is not None
    e2 = board.ParsePosition("E2")
    assert e2 is not None
    d1 = board.ParsePosition("D1")
    assert d1 is not None
    self.assertCountEqual(self.default_board.get_neighbor_tiles(e1),
                          [f1, e2, d1])

    e6 = board.ParsePosition("E6")
    assert e6 is not None
    e5 = board.ParsePosition("E5")
    assert e5 is not None
    d5 = board.ParsePosition("D5")
    assert d5 is not None
    d6 = board.ParsePosition("D6")
    assert d6 is not None
    e7 = board.ParsePosition("E7")
    assert e7 is not None
    f6 = board.ParsePosition("F6")
    assert f6 is not None
    f5 = board.ParsePosition("F5")
    assert f5 is not None
    self.assertCountEqual(self.default_board.get_neighbor_tiles(e6),
                          [e5, d5, d6, e7, f6, f5])

  def test_default_game_board_neighbors_structure_owners(self) -> None:
    # No structures anywhere!
    a13 = board.ParsePosition("A13")
    assert a13 is not None
    self.assertTrue(
        len(self.default_board.neighbor_structure_owners(a13)) == 0)

    # We build some structures.
    a12 = board.ParsePosition("A12")
    assert a12 is not None
    b12 = board.ParsePosition("B12")
    assert b12 is not None
    self.default_board.build(a12, common.Structure.DWELLING)
    self.default_board.build(b12, common.Structure.DWELLING)

    self.assertCountEqual(self.default_board.neighbor_structure_owners(a13), [
        (common.Structure.DWELLING, common.Terrain.WASTELAND),
        (common.Structure.DWELLING, common.Terrain.DESERT),
    ])
