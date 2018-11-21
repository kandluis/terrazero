from typing import Dict, List, Tuple

from simulation.core import faction
from simulation.core import common

class CultBoard:
  """Class representing the cult board. 
  """
  # Mapping from arriving cult track location which produces power
  # to how much power is received.
  ADDITIONAL_POWER: Dict[int, int] = {
    3: 1, 5: 2, 7: 2, 10: 3
  }
  # Moving to this location
  TOWN_KEY_REQUIRED: int = 10

  # Number of availabe order positions for priests.
  NUM_ORDERS: int = 4

  def __init__(self, factions: List[faction.Faction]):
    # Mapping from cult track to list of availabler orders.
    # Factions is the list of factions playing on the cult track.
    self.available_orders: Dict[common.CultTrack: List[int]] = {
      common.CultTrack.FIRE: [2, 2, 2, 3], 
      common.CultTrack.WATER: [2, 2, 2, 3],
      common.CultTrack.EARTH: [2, 2, 2, 3],
      common.CultTrack.AIR: [2, 2, 2, 3],
    }
    # Mapping from cult-track to index to which terrain/faction occupies that order.
    # indexes map as 1 -> 3, 2 -> 2, 3 -> 2, 4 -> 2.
    self.occupied_orders: Dict[common.CultTrack, Dict[int, common.Terrain]] = {
      common.CultTrack.EARTH: {}, common.CultTrack.WATER: {}, common.CultTrack.FIRE: {}, common.CultTrack.AIR: {}
    }
    # Mapping from cult-track to mapping from terrain/faction to current positions.
    self.positions: Dict[common.CultTrack, Dict[common.Terrain, int]] = {
      common.CultTrack.EARTH: {}, common.CultTrack.WATER: {}, common.CultTrack.FIRE: {}, common.CultTrack.AIR: {}
    }
    for faction in factions:
      for track, pos in faction.StartingCultPositions().items():
        self.positions[track][faction.HomeTerrain()] = pos

  def SacrificePriestToOrder(self, player: 'Player', order: common.CultTrack) -> Tuple[int, int]:
    """The player is sacrificing their priest to the order specified.

    Returns a tuple of (spacesGained, powerGained). Note that spacesGained can be zero
    if the Player is at 9 but has no town key.
    """
    terrain: common.Terrain = player.faction.HomeTerrain()
    if self.available_orders[order]:
      spacesToAttempt: int = self.available_orders[order].pop()
      self.occupied_orders[order][CultBoard.NUM_ORDERS - len(self.available_orders[order])] = terrain
    else:
      spacesToAttempt: int = 1
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