import abc

from typing import Dict, List, NamedTuple

from simulation.core import common
from simulation import utils


class Faction(abc.ABC):
  """
  Interface for accessing one of the 14 Factions.
  """
  TOTAL_STRUCTURES: Dict[common.Structure, int] = {
      common.Structure.DWELLING: 8,
      common.Structure.TRADING_POST: 4,
      common.Structure.TEMPLE: 3,
      common.Structure.SANCTUARY: 1,
      common.Structure.STRONGHOLD: 1,
  }

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

  @abc.abstractmethod
  def _WorkerIncomeSpots(self) -> List[common.Income]:
    pass

  @abc.abstractmethod
  def _TPIncomeSpots(self) -> List[common.Income]:
    pass

  @abc.abstractmethod
  def _TempleIncomeSpots(self) -> List[common.Income]:
    pass

  @abc.abstractmethod
  def _SantuaryIncome(self) -> common.Income:
    pass

  @abc.abstractmethod
  def _StrongHoldIncome(self) -> common.Income:
    pass

  @abc.abstractmethod
  def _DefaultIncome(self) -> common.Income:
    pass

  def IncomeForStructures(
      self, structures: Dict[common.Structure, int]) -> common.Income:
    """This includes default income"""
    income = self._DefaultIncome()
    for structure, count in structures.items():
      TOTAL = Faction.TOTAL_STRUCTURES[structure]
      assert count <= TOTAL
      structure_income: List[common.Income]
      if structure == common.Structure.STRONGHOLD:
        structure_income = [self._StrongHoldIncome()] if count > 0 else []
      elif structure == common.Structure.SANCTUARY:
        structure_income = [self._SantuaryIncome()] if count > 0 else []
      elif structure == common.Structure.TEMPLE:
        structure_income = self._TempleIncomeSpots()
        assert len(structure_income) == TOTAL
      elif structure == common.Structure.TRADING_POST:
        structure_income = self._TPIncomeSpots()
        assert len(structure_income) == TOTAL
      elif structure == common.Structure.DWELLING:
        structure_income = self._WorkerIncomeSpots()
        assert len(structure_income) == TOTAL
      else:
        raise utils.InternalError("Structure %s is not defined." % structure)
      for spot in range(count):
        income += structure_income[spot]
    return income

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

  def _DefaultIncome(self) -> common.Income:
    return common.Income(workers=1)

  def _WorkerIncomeSpots(self) -> List[common.Income]:
    return [
        common.Income(workers=1)
        for _ in range(Faction.TOTAL_STRUCTURES[common.Structure.DWELLING] - 1)
    ] + [common.Income()]

  def _TPIncomeSpots(self) -> List[common.Income]:
    return [
        common.Income(coins=2, power=1) for _ in range(
            Faction.TOTAL_STRUCTURES[common.Structure.TRADING_POST] // 2)
    ] + [
        common.Income(coins=2, power=2) for _ in range(
            Faction.TOTAL_STRUCTURES[common.Structure.TRADING_POST] // 2)
    ]

  def _TempleIncomeSpots(self) -> List[common.Income]:
    return [
        common.Income(priests=1)
        for _ in range(Faction.TOTAL_STRUCTURES[common.Structure.TEMPLE])
    ]

  def _SantuaryIncome(self) -> common.Income:
    return common.Income(priests=1)

  def _StrongHoldIncome(self) -> common.Income:
    return common.Income(power=2)


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

  def _DefaultIncome(self) -> common.Income:
    return common.Income()

  def _WorkerIncomeSpots(self) -> List[common.Income]:
    return [
        common.Income(workers=1),
        common.Income(workers=1),
        common.Income(),
        common.Income(workers=1),
        common.Income(workers=1),
        common.Income(),
        common.Income(workers=1),
        common.Income(workers=1)
    ]

  def _TPIncomeSpots(self) -> List[common.Income]:
    return [
        common.Income(coins=2, power=1) for _ in range(
            Faction.TOTAL_STRUCTURES[common.Structure.TRADING_POST] // 2)
    ] + [
        common.Income(coins=2, power=2) for _ in range(
            Faction.TOTAL_STRUCTURES[common.Structure.TRADING_POST] // 2)
    ]

  def _TempleIncomeSpots(self) -> List[common.Income]:
    return [
        common.Income(priests=1),
        common.Income(power=5),
        common.Income(priests=1)
    ]

  def _SantuaryIncome(self) -> common.Income:
    return common.Income(priests=1)

  def _StrongHoldIncome(self) -> common.Income:
    return common.Income(power=2)


def AllAvailable() -> List[Faction]:
  return [Halflings(), Engineers()]