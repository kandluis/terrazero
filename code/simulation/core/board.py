import collections

from typing import Dict, NamedTuple, List, Optional, Set, Tuple

from simulation.core import common
from simulation import utils


class Position(NamedTuple):
  row: str
  column: int


def ParsePosition(msg: str) -> Optional[Position]:
  MIN_ROW = "A"
  MAX_ROW = "I"
  MIN_COL = 1
  MAX_COL = 13
  try:
    letter: str = msg[0].upper()
    column: int = int(msg[1:])
  except (IndexError, ValueError):
    return None
  if (MIN_ROW <= letter and letter <= MAX_ROW and MIN_COL <= column
      and column <= MAX_COL):
    return Position(row=letter, column=column)
  return None


class GameBoard:
  def __init__(self):
    self._TERRAIN_MAP_FILE: str = "data/starting_map.csv"
    # Map from (row, col) to terrain. Note that this is a raw representation of the
    # terrain for the map, and likely does not correspond to the representation expected
    # by the players. Use the helper methods in this class instead.
    self._tiles: Dict[Tuple[int, int], common.
                      Terrain] = self._LoadStartingMap()
    rows, cols = zip(*self._tiles.keys())
    self._maxRowIndex, self._maxColIndex = max(rows), max(cols)

    # Same as self._tiles but represents the currently (in any) exsting
    # structure on the map.
    self._structures: Dict[Tuple[int, int], Optional[
        common.Structure]] = collections.defaultdict(lambda: None)

  @staticmethod
  def LinesToMap(lines: List[str]) -> Dict[Tuple[int, int], common.Terrain]:
    """See documentation of LoadStartingMap"""
    terrain: Dict[Tuple[int, int], common.Terrain] = {}
    for i, line in enumerate(lines):
      tilesnames: List[str] = [line.strip() for line in line.split(",")]
      # Odd tiles are padded at the beginning and end with water.
      rowIndex: int = 0
      if i % 2 == 1:
        terrain[(i, rowIndex)] = common.Terrain.WATER
        rowIndex += 1
      for tilename in tilesnames:
        for _ in range(2):
          terrain[(i, rowIndex)] = common.Terrain[tilename.upper()]
          rowIndex += 1
      if i % 2 == 1:
        terrain[(i, rowIndex)] = common.Terrain.WATER
    return terrain

  def CanBeBuilt(self, pos: Position, structure: common.Structure,
                 owner: common.Terrain) -> bool:
    """Checks if the given structure by the specified owner can be built at row/col """
    rawPos = self._ToRaw(pos)
    terrain = self._tiles[rawPos]
    if terrain != owner:
      return False
    exstingStructure = self._structures[rawPos]
    if structure == common.Structure.DWELLING:
      return (exstingStructure is None)
    return (exstingStructure is not None
            and exstingStructure.IsUpgradeableTo(structure))

  def Build(self, pos: Position, structure: common.Structure) -> None:
    """Builds the given structure at the specified location. Will throw if an invalid structure is built."""
    rawPos = self._ToRaw(pos)
    terrain = self._tiles[rawPos]
    exstingStructure = self._structures[rawPos]
    if not self.CanBeBuilt(pos, structure, terrain):
      raise utils.InternalError(
          "Attempting to build %s at %s which is invalid!" % (structure, pos))
    self._structures[rawPos] = structure

  def GetTerrain(self, pos: Position) -> common.Terrain:
    """Returns the terrain for the row, column specified, where row is one of A-I and column
    is one of 1-13. Note that even rows only have 1-12"""
    return self._tiles[self._ToRaw(pos)]

  def GetStructure(self, pos: Position) -> Optional[common.Structure]:
    return self._structures[self._ToRaw(pos)]

  def GetNeighborTiles(self, pos: Position) -> Set[Position]:
    rawRow, rawColumn = self._ToRaw(pos)
    # The tile side dependso n the row.
    otherRawColumn: int = rawColumn - 1 if rawRow % 2 == 0 else rawColumn + 1
    # We union the neighbors for both sides of the tile.
    rawNeighbors: Set[Tuple[int, int]] = self._GetRawNeighbors(
        rawRow, rawColumn) | self._GetRawNeighbors(rawRow, otherRawColumn)
    # Now we just convert them back to their tile values and dedup. Don't
    # count yourself.
    return {self._FromRaw(*rawNeighbor)
            for rawNeighbor in rawNeighbors} - {pos}

  def NeighborStructureOwners(
      self, pos: Position) -> Set[Tuple[common.Structure, common.Terrain]]:
    results: Set[Tuple[common.Structure, common.Terrain]] = set()
    for neighbor in self.GetNeighborTiles(pos):
      terrain: common.Terrain = self.GetTerrain(pos)
      structure: Optional[common.Structure] = self.GetStructure(pos)
      if not structure:
        continue
      results.add((structure, terrain))
    return results

  def _GetRawNeighbors(self, row: int, column: int) -> Set[Tuple[int, int]]:
    neighbors: Set[Tuple[int, int]] = set()
    if row > 0:  # Look Up.
      neighbors.add((row - 1, column))
    if row < self._maxRowIndex:  # Look down.
      neighbors.add((row + 1, column))
    if column > 0:  # Look left.
      neighbors.add((row, column - 1))
    if column < self._maxColIndex:  # Look right.
      neighbors.add((row, column + 1))
    return neighbors

  def _ToRaw(self, pos: Position) -> Tuple[int, int]:
    rawRow: int = ord(pos.row.upper()) - ord('A')
    rawColumn: int = 2 * (pos.column - 1) + 1
    return rawRow, rawColumn

  def _FromRaw(self, rawRow: int, rawColumn: int) -> Position:
    row: str = chr(ord('A') + rawRow)
    if rawRow % 2 == 0:
      column = int(rawColumn / 2) + 1
    else:
      column = int((rawColumn - 1) / 2) + 1
    return Position(row=row, column=column)

  def _LoadStartingMap(self) -> Dict[Tuple[int, int], common.Terrain]:
    """
    To make finding neighbors easier, we split the typical hexagonal map for TM
    vertically into double the number of tiles. This means we have [0,25] values
    along the top and [0,7] columns.

    Essentially, all tiles are split into two. Odd-index rows are padded on both end
    with water tiles.
    """
    lines: List[str] = []
    with open(self._TERRAIN_MAP_FILE) as f:
      lines = f.readlines()
    return GameBoard.LinesToMap(lines)
