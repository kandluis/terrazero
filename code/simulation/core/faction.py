import abc

from typing import Dict, List, NamedTuple

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
  def StartingResources(self) -> common.Resources:
    """Returns the number of initial resources for this class"""
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
  def StructureCost(self, structure: common.Structure,
                    adjacentEnemyStructure: bool) -> common.Resources:
    pass

  def __str__(self) -> str:

    return """
      ---------------- {class_name} ----------------
      Home Terrain: {terrain}

      Starting Resources:
      {resources}

      Power:
      {power}

      Shipping:
      {shipping}

      Cult Positions:
      {cult}
    """.format(
        terrain=self.HomeTerrain(),
        resources=self.StartingResources(),
        power=self.StartingPower(),
        shipping=self.StartingShipping(),
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

  def StartingResources(self) -> common.Resources:
    return common.Resources(workers=3, priests=0, coins=15, bridges=0)

  def StartingCultPositions(self) -> Dict[common.CultTrack, int]:
    return {
        common.CultTrack.FIRE: 0,
        common.CultTrack.EARTH: 1,
        common.CultTrack.AIR: 1,
        common.CultTrack.WATER: 0
    }

  def StartingShipping(self) -> int:
    return 0

  def StructureCost(self, structure: common.Structure,
                    adjacentEnemyStructure: bool) -> common.Resources:
    if structure == common.Structure.DWELLING:
      return common.Resources(workers=1, coins=2)
    if structure == common.Structure.TRADING_POST:
      return common.Resources(
          workers=2, coins=3 if adjacentEnemyStructure else 6)
    if structure == common.Structure.STRONGHOLD:
      return common.Resources(workers=4, coins=8)
    if structure == common.Structure.TEMPLE:
      return common.Resources(workers=2, coins=5)
    if structure == common.Structure.SANCTUARY:
      return common.Resources(workers=4, coins=6)
    raise utils.InternalError("Unknown cost for structure: %s" % structure)


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

  def StartingResources(self) -> common.Resources:
    return common.Resources(workers=2, priests=0, coins=10, bridges=0)

  def StartingCultPositions(self) -> Dict[common.CultTrack, int]:
    return {
        common.CultTrack.FIRE: 0,
        common.CultTrack.EARTH: 0,
        common.CultTrack.AIR: 0,
        common.CultTrack.WATER: 0
    }

  def StartingShipping(self) -> int:
    return 0

  def StructureCost(self, structure: common.Structure,
                    adjacentEnemyStructure: bool) -> common.Resources:
    if structure == common.Structure.DWELLING:
      return common.Resources(workers=1, coins=1)
    if structure == common.Structure.TRADING_POST:
      return common.Resources(
          workers=1, coins=2 if adjacentEnemyStructure else 4)
    if structure == common.Structure.STRONGHOLD:
      return common.Resources(workers=3, coins=6)
    if structure == common.Structure.TEMPLE:
      return common.Resources(workers=1, coins=4)
    if structure == common.Structure.SANCTUARY:
      return common.Resources(workers=3, coins=6)
    raise utils.InternalError("Unknown cost for structure: %s" % structure)


def AllAvailable() -> List[Faction]:
  return [Halflings(), Engineers()]