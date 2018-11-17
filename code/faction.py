from enum import Enum, auto, unique
import utils

from typing import Dict, List, Tuple, Set

@unique
class Terrain(Enum):
  PLAIN = auto() # Brown
  SWAMP = auto() # Black
  LAKE = auto() # Blue
  FOREST = auto() # Green
  MOUNTAIN = auto() # Grey
  WASTELAND = auto() # Red
  DESERT = auto() # Yellow
  WATER = auto() # BLUE WATER, unbuildable

@unique
class PowerBowl(Enum):
  I = auto()
  II = auto()
  III = auto()

@unique
class CultTrack(Enum):
  FIRE = auto()
  WATER = auto()
  EARTH = auto()
  AIR = auto()

class CultBoard:
  # Mapping from arriving cult track location which produces power
  # to how much power is received.
  ADDITIONAL_POWER: Dict[int, int] = {
    3: 1, 5: 2, 7: 2, 10: 3
  }
  # Moving to this location
  TOWN_KEY_REQUIRED = 10

  # Number of availabe order positions for priests.
  NUM_ORDERS = 4

  def __init__(self, factions):
    # Mapping from cult track to list of availabler orders.
    # Factions is the list of factions playing on the cult track.
    self.available_orders: Dict[CultTrack: List[int]] = {
      CultTrack.FIRE: [2, 2, 2, 3], 
      CultTrack.WATER: [2, 2, 2, 3],
      CultTrack.EARTH: [2, 2, 2, 3],
      CultTrack.AIR: [2, 2, 2, 3],
    }
    # Mapping from cult-track to index to which terrain/faction occupies that order.
    # indexes map as 1 -> 3, 2 -> 2, 3 -> 2, 4 -> 2.
    self.occupied_orders: Dict[CultTrack, Dict[int, Terrain]] = {
      CultTrack.EARTH: {}, CultTrack.WATER: {}, CultTrack.FIRE: {}, CultTrack.AIR: {}
    }
    # Mapping from cult-track to mapping from terrain/faction to current positions.
    self.positions: Dict[CultTrack, Dict[Terrain, int]] = {
      CultTrack.EARTH: {}, CultTrack.WATER: {}, CultTrack.FIRE: {}, CultTrack.AIR: {}
    }
    for faction in factions:
      for track, pos in faction.StartingCultPositions().items():
        self.positions[track][faction.HomeTerrain()] = pos

  def SacrificePriestToOrder(self, player: 'Player', order: CultTrack) -> Tuple[int, int]:
    """The player is sacrificing their priest to the order specified.

    Returns a tuple of (spacesGained, powerGained). Note that spacesGained can be zero
    if the Player is at 9 but has no town key.
    """
    terrain = player.faction.HomeTerrain()
    if self.available_orders[order]:
      spacesToAttempt = self.available_orders[order].pop()
      self.occupied_orders[order][CultBoard.NUM_ORDERS - len(self.available_orders[order])] = terrain
    else:
      spacesToAttempt = 1
    currPosition = self.positions[order][terrain]
    expectedPosition = currPosition + spacesToAttempt
    powerCollected = sum([ power for pos, power in CultBoard.ADDITIONAL_POWER.items()
        if currPosition < pos and pos <= expectedPosition])
    if expectedPosition < CultBoard.TOWN_KEY_REQUIRED:
      self.positions[order][terrain] = expectedPosition
    # We've maxed the cult-board. We might end up moving less than expected. Check to see if we
    # can even take the town right now. 
    elif max(self.positions[order].values()) < CultBoard.TOWN_KEY_REQUIRED and player.UseTownKey():
      self.positions[order][terrain] = CultBoard.TOWN_KEY_REQUIRED
    else:
      powerCollected -= min(3, powerCollected)
      self.positions[order][terrain] = CultBoard.TOWN_KEY_REQUIRED - 1
    return (self.positions[order][terrain] - currPosition, powerCollected)

@unique
class Building(Enum):
  DWELLING = auto()
  TRADING_HOUSE = auto()
  SANCTUARY = auto()
  TEMPLE = auto()
  STRONGHOLD = auto()

class GameBoard:
  def __init__(self):
    self._TERRAIN_MAP_FILE = "data/starting_map.csv"
    # Map from (row, col) to terrain. Note that this is a raw representation of the
    # terrain for the map, and likely does not correspond to the representation expected
    # by the players. Use the helper methods in this class instead.
    self._tiles: Dict[Tuple[int, int], Terrain] = self._LoadStartingMap()
    rows, cols = zip(*self._tiles.keys())
    self._maxRowIndex, self._maxColIndex = max(rows), max(cols)


  @staticmethod
  def LinesToMap(lines: List[str]) -> Dict[Tuple[int, int], Terrain]:
    """See documentation of LoadStartingMap"""
    terrain = {}
    for i, line in enumerate(lines):
      tilesnames = [line.strip() for line in line.split(",")]
      # Odd tiles are padded at the beginning and end with water.
      rowIndex = 0
      if i % 2 == 1:
        terrain[(i, rowIndex)] = Terrain.WATER
        rowIndex += 1
      for tilename in tilesnames:
        for _ in range(2):
          terrain[(i, rowIndex)] = Terrain[tilename.upper()]
          rowIndex += 1 
      if i % 2 == 1:
        terrain[(i, rowIndex)] = Terrain.WATER
    return terrain

  def GetTerrain(self, row: str, column: int) -> Terrain:
    """Returns the terrain for the row, column specified, where row is one of A-I and column
    is one of 1-13. Note that even rows only have 1-12""" 
    return self._tiles[(self._ToRaw(row, column))]

  def GetNeighborTiles(self, row: str, column: int) -> Set[Tuple[str, int]]:
    rawRow, rawColumn = self._ToRaw(row, column)
    # The tile side dependso n the row.
    otherRawColumn = rawColumn - 1 if rawRow % 2 == 0 else rawColumn + 1
    # We union the neighbors for both sides of the tile.
    rawNeighbors = self._GetRawNeighbors(rawRow, rawColumn) | self._GetRawNeighbors(rawRow, otherRawColumn)
    # Now we just convert them back to their tile values and dedup. Don't count yourself.
    return {self._FromRaw(*rawNeighbor) for rawNeighbor in rawNeighbors} - { (row, column) }

  def _GetRawNeighbors(self, row: int, column: int) -> Set[Tuple[int, int]]:
    neighbors = set()
    if row > 0: # Look Up.
      neighbors.add((row - 1, column))
    if row < self._maxRowIndex: # Look down.
      neighbors.add((row + 1, column))
    if column > 0: # Look left.
      neighbors.add((row, column - 1))
    if column < self._maxColIndex: # Look right.
      neighbors.add((row, column + 1))
    return neighbors


  def _ToRaw(self, row: str, column: int) -> Tuple[int, int]:
    rawRow: int = ord(row.upper()) - ord('A')
    rawColumn: int = 2 * (column - 1) + 1
    return rawRow, rawColumn

  def _FromRaw(self, rawRow: int, rawColumn: int) -> Tuple[str, int]:
    row = chr(ord('A') + rawRow)
    if rawRow % 2 == 0:
      column = int(rawColumn / 2) + 1
    else:
      column = int((rawColumn - 1) / 2) + 1
    return row, column

  def _LoadStartingMap(self) -> Dict[Tuple[int, int], Terrain]:
    """
    To make finding neighbors easier, we split the typical hexagonal map for TM
    vertically into double the number of tiles. This means we have [0,25] values
    along the top and [0,7] columns.

    Essentially, all tiles are split into two. Odd-index rows are padded on both end
    with water tiles.
    """
    lines = []
    with open(self._TERRAIN_MAP_FILE) as f:
      lines = f.readlines()
    return GameBoard.LinesToMap(lines)


class Faction:
  """
  Interface for accessing one of the 14 Factions.
  """
  def __init__(self):
    raise utils.UnimplementedError("Using abstract Faction interface")

  def HomeTerrain(self) -> Terrain:
    """Returns the home terrain of the faction"""
    raise utils.UnimplementedError("Using abstract Faction interface")

  def StartingPower(self) -> Dict[PowerBowl, int]:
    """Returns a mapping for the initial power for this faction"""
    raise utils.UnimplementedError("Using abstract Faction interface")

  def StartingWorkers(self) -> int:
    """Returns the number of initial workers"""
    raise utils.UnimplementedError("Using abstract Faction interface")

  def StartingCoins(self) -> int:
    """Returns the number of initial coins"""
    raise utils.UnimplementedError("Using abstract Faction interface")

  def StartingCultPositions(self) -> Dict[CultTrack, int]:
    """Returnst the starting cult positions"""
    raise utils.UnimplementedError("Using abstract Faction interface")

  def StartingShipping(self) -> int:
    """Returns the shillping level"""
    raise utils.UnimplementedError("Using abstract Faction interface")

  def StartingPriests(self) -> int:
    raise utils.UnimplementedError("Using abstract Faction interface")


class Halflings(Faction):
  def __init__(self):
    pass

  def HomeTerrain(self) -> Terrain:
    return Terrain.PLAIN

  def StartingPower(self) -> Dict[PowerBowl, int]:
    return { PowerBowl.I : 3, PowerBowl.II : 9, PowerBowl.III : 0}

  def StartingWorkers(self) -> int:
    return 3

  def StartingCoins(self) -> int:
    return 15

  def StartingCultPositions(self) -> Dict[CultTrack, int]:
    return {CultTrack.FIRE : 0, CultTrack.EARTH : 1, CultTrack.AIR : 1, CultTrack.WATER : 0}

  def StartingShipping(self) -> int:
    return 0

  def StartingPriests(self) -> int:
    return 0

class Engineers(Faction):
  def __init__(self):
    pass

  def HomeTerrain(self) -> Terrain:
    return Terrain.MOUNTAIN

  def StartingPower(self) -> Dict[PowerBowl, int]:
    return { PowerBowl.I : 3, PowerBowl.II : 9, PowerBowl.III : 0}

  def StartingWorkers(self) -> int:
    return 2

  def StartingCoins(self) -> int:
    return 10

  def StartingCultPositions(self) -> Dict[CultTrack, int]:
    return {CultTrack.FIRE : 0, CultTrack.EARTH : 0, CultTrack.AIR : 0, CultTrack.WATER : 0}

  def StartingShipping(self) -> int:
    return 0

  def StartingPriests(self) -> int:
    return 0

@unique
class TownKey(Enum):
  """The town keys"""
  WOKERS2 = auto()
  PRIEST = auto()
  CULT = auto() # 1 up on every cult-track.
  POWER8 = auto() # 8 power.
  COIN6 = auto() # 6 coins.

@unique
class BonusCards(Enum):
  PRIEST = auto() # 1 priest income.coins
  WORKER_3POWER = auto()
  COIN6 = auto()
  POWER3_SHIPPING = auto()
  SPADE_COIN2 = auto()
  CULT_COIN4 = auto()
  DWELLING_COIN2 = auto()
  TRADING_POST_WORKER = auto()
  STRONGHOLD_WORKER2 = auto()

class RoundBonus(Enum):
  pass

class FavorTile(Enum):
  pass

class SpecialActions(Enum):
  pass

class Player:
  def __init__(self, faction: Faction):
    self.faction: Faction = faction 
    self.power: Dict[PowerBowl, int] = faction.StartingPower()
    self.coins: int = faction.StartingCoins()
    self.workers: int = faction.StartingWorkers()
    self.shipping: int = faction.StartingShipping()
    # Mapping from TowKey to whether or not we've used it already.
    self.used_town_keys: Dict[TownKey: bool] = {}
    self.bridges = 0
    self.priests = faction.StartingPriests()

  def UseTownKey(self) -> bool:
    """Returns true if an available town keys was used. False if no town key is available."""
    for key, used in self.used_town_keys.items():
      if not used:
        self.used_town_keys[key] = True
        return True
    return False

  def GainTown(self, townKey: TownKey) -> None:
    self.used_town_keys[townKey] = False

  def GainPower(self, power: int) -> None:
    # Gain the given amount of power. Overflowing power is automatically converted to coins.
    remainingPower = power
    assert remainingPower >= 0
    if remainingPower == 0: return

    if self.power[PowerBowl.I] > 0:
      toMove = min(self.power[PowerBowl.I], remainingPower)
      self.power[PowerBowl.I] -= toMove
      self.power[PowerBowl.II] += toMove
      remainingPower -= toMove
  
    if remainingPower == 0: return
    
    # If we still have power, power I bowl must be empty at this point.
    # Otherwise, we have no power left.
    assert self.power[PowerBowl.I] == 0
    if self.power[PowerBowl.II] > 0:
      toMove = min(self.power[PowerBowl.II], remainingPower)
      self.power[PowerBowl.II] -= toMove
      self.power[PowerBowl.III] += toMove
      remainingPower -= toMove

    if remainingPower == 0: return

    # If we still have power, power II bowl must be empty at this point.
    assert self.power[PowerBowl.II] == 0

    # Spending an even amount of excess power always makes sense and is optimal. 
    self.coins += int(remainingPower / 2)
    # TODO(nautilik): We assume player will want to spend remaining 1 power,
    # even if this means he'll end up with power stuck in PowerBowl.II.
    if remainingPower % 2 == 1:
      self.power[PowerBowl.III] -= 1
      self.power[PowerBowl.II] += 1
      self.coins += 1




    

