import abc

from typing import Dict, List

from simulation import utils
from simulation.core import common


class Faction(abc.ABC):
  """
  Interface for accessing one of the 14 Factions.
  """

  @abc.abstractmethod
  def HomeTerrain(self) -> common.Terrain:
    """Returns the home terrain of the faction"""
    pass

  @abc.abstractmethod
  def StartingPower(self) -> Dict[common.PowerBowl, int]:
    """Returns a mapping for the initial power for this faction"""
    pass

  @abc.abstractmethod
  def StartingWorkers(self) -> int:
    """Returns the number of initial workers"""
    pass

  @abc.abstractmethod
  def StartingCoins(self) -> int:
    """Returns the number of initial coins"""
    pass

  @abc.abstractmethod
  def StartingCultPositions(self) -> Dict[common.CultTrack, int]:
    """Returnst the starting cult positions"""
    pass

  @abc.abstractmethod
  def StartingShipping(self) -> int:
    """Returns the shillping level"""
    pass

  @abc.abstractmethod
  def StartingPriests(self) -> int:
    pass

  def __str__(self) -> str:

    return """
      ---------------- {class_name} ----------------
      Home Terrain: {terrain}

      Starting Resources:
      Coins: {coins}     Workers: {workers}    Shipping: {shipping}   Priests: {priests}

      Power:
      {power}

      Cult Positions:
      {cult}
    """.format(
        terrain=self.HomeTerrain(),
        coins=self.StartingCoins(),
        workers=self.StartingWorkers(),
        shipping=self.StartingShipping(),
        priests=self.StartingPriests(),
        power=self.StartingPower(),
        cult=self.StartingCultPositions(),
        class_name=type(self).__name__)


class Halflings(Faction):
  def __init__(self):
    pass

  def HomeTerrain(self) -> common.Terrain:
    return common.Terrain.PLAIN

  def StartingPower(self) -> Dict[common.PowerBowl, int]:
    return {
        common.PowerBowl.I: 3,
        common.PowerBowl.II: 9,
        common.PowerBowl.III: 0
    }

  def StartingWorkers(self) -> int:
    return 3

  def StartingCoins(self) -> int:
    return 15

  def StartingCultPositions(self) -> Dict[common.CultTrack, int]:
    return {
        common.CultTrack.FIRE: 0,
        common.CultTrack.EARTH: 1,
        common.CultTrack.AIR: 1,
        common.CultTrack.WATER: 0
    }

  def StartingShipping(self) -> int:
    return 0

  def StartingPriests(self) -> int:
    return 0


class Engineers(Faction):
  def __init__(self):
    pass

  def HomeTerrain(self) -> common.Terrain:
    return common.Terrain.MOUNTAIN

  def StartingPower(self) -> Dict[common.PowerBowl, int]:
    return {
        common.PowerBowl.I: 3,
        common.PowerBowl.II: 9,
        common.PowerBowl.III: 0
    }

  def StartingWorkers(self) -> int:
    return 2

  def StartingCoins(self) -> int:
    return 10

  def StartingCultPositions(self) -> Dict[common.CultTrack, int]:
    return {
        common.CultTrack.FIRE: 0,
        common.CultTrack.EARTH: 0,
        common.CultTrack.AIR: 0,
        common.CultTrack.WATER: 0
    }

  def StartingShipping(self) -> int:
    return 0

  def StartingPriests(self) -> int:
    return 0


def AllAvailable() -> List[Faction]:
  return [Halflings(), Engineers()]