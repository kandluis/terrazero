import enum
import utils

from typing import Dict

class Terrain(enum.Enum):
  PLAINS = 0
  SWAMP = 1
  LAKES = 2
  FOREST = 3
  MOUNTAINS = 4
  WASTELAND = 5
  DESERT = 6

class PowerBowl(enum.Enum):
  I = auto()
  II = auto()
  III = auto()

class CultTrack(enum.Enum):
  FIRE = auto()
  WATER = auto()
  EARTH = auto()
  AIR = auto()

class Building(enum.Enum):
  DWELLING = auto()
  TRADING_HOUSE = auto()
  SANCTUARY = auto()
  TEMPLE = auto()
  STRONGHOLD = auto()


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


class Player:
  def __inti__(self, faction: Faction):
    self.faction: Faction = faction 
    self.power: Dict[PowerBowl, int] = {}