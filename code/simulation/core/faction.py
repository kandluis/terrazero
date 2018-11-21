from typing import Dict

from simulation.core import utils
from simulation.core import common

class Faction:
  """
  Interface for accessing one of the 14 Factions.
  """
  def __init__(self):
    raise utils.UnimplementedError("Using abstract Faction interface")

  def HomeTerrain(self) -> common.Terrain:
    """Returns the home terrain of the faction"""
    raise utils.UnimplementedError("Using abstract Faction interface")

  def StartingPower(self) -> Dict[common.PowerBowl, int]:
    """Returns a mapping for the initial power for this faction"""
    raise utils.UnimplementedError("Using abstract Faction interface")

  def StartingWorkers(self) -> int:
    """Returns the number of initial workers"""
    raise utils.UnimplementedError("Using abstract Faction interface")

  def StartingCoins(self) -> int:
    """Returns the number of initial coins"""
    raise utils.UnimplementedError("Using abstract Faction interface")

  def StartingCultPositions(self) -> Dict[common.CultTrack, int]:
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

  def HomeTerrain(self) -> common.Terrain:
    return common.Terrain.PLAIN

  def StartingPower(self) -> Dict[common.PowerBowl, int]:
    return { common.PowerBowl.I : 3, common.PowerBowl.II : 9, common.PowerBowl.III : 0}

  def StartingWorkers(self) -> int:
    return 3

  def StartingCoins(self) -> int:
    return 15

  def StartingCultPositions(self) -> Dict[common.CultTrack, int]:
    return {common.CultTrack.FIRE : 0, common.CultTrack.EARTH : 1, common.CultTrack.AIR : 1, common.CultTrack.WATER : 0}

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
    return { common.PowerBowl.I : 3, common.PowerBowl.II : 9, common.PowerBowl.III : 0}

  def StartingWorkers(self) -> int:
    return 2

  def StartingCoins(self) -> int:
    return 10

  def StartingCultPositions(self) -> Dict[common.CultTrack, int]:
    return {common.CultTrack.FIRE : 0, common.CultTrack.EARTH : 0, common.CultTrack.AIR : 0, common.CultTrack.WATER : 0}

  def StartingShipping(self) -> int:
    return 0

  def StartingPriests(self) -> int:
    return 0




    

