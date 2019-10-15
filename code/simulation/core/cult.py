from typing import Dict, List, Tuple

from simulation.core import common
from simulation.core import faction as faction_lib
from simulation.core import player


class CultBoard:
  """Class representing the cult board."""
  # Mapping from arriving cult track location which produces power
  # to how much power is received.
  ADDITIONAL_POWER: Dict[int, int] = {3: 1, 5: 2, 7: 2, 10: 3}
  # Moving to this location requires a town-key.
  TOWN_KEY_REQUIRED: int = 10

  # Number of availabe order positions for priests.
  NUM_ORDERS: int = 4

  def __init__(self, factions: List[faction_lib.Faction]):
    # Mapping from cult track to list of availabler orders.
    # Factions is the list of factions playing on the cult track.
    self.available_orders: Dict[common.CultTrack, List[int]] = {
        common.CultTrack.FIRE: [2, 2, 2, 3],
        common.CultTrack.WATER: [2, 2, 2, 3],
        common.CultTrack.EARTH: [2, 2, 2, 3],
        common.CultTrack.AIR: [2, 2, 2, 3],
    }
    # Mapping from cult-track to index to which terrain/faction occupies order.
    # indexes map as 1 -> 3, 2 -> 2, 3 -> 2, 4 -> 2.
    self.occupied_orders: Dict[common.CultTrack, Dict[int, common.Terrain]] = {
        common.CultTrack.EARTH: {},
        common.CultTrack.WATER: {},
        common.CultTrack.FIRE: {},
        common.CultTrack.AIR: {}
    }
    # Mapping from cult-track to mapping from terrain/faction to current
    # positions.
    self.positions: Dict[common.CultTrack, Dict[common.Terrain, int]] = {
        common.CultTrack.EARTH: {},
        common.CultTrack.WATER: {},
        common.CultTrack.FIRE: {},
        common.CultTrack.AIR: {}
    }
    for faction in factions:
      for track, pos in faction.starting_cult_positions().items():
        self.positions[track][faction.home_terrain()] = pos

  def sacrifice_priest_to_order(self, player: player.Player,
                                order: common.CultTrack) -> Tuple[int, int]:
    """The player is sacrificing their priest to the order specified.

    Returns a tuple of (spacesGained, powerGained).  Note that spacesGained
    can be zero if the Player is at 9 but has no town key.
    """
    terrain: common.Terrain = player.faction.home_terrain()
    if self.available_orders[order]:
      spaces_to_attempt: int = self.available_orders[order].pop()
      self.occupied_orders[order][CultBoard.NUM_ORDERS -
                                  len(self.available_orders[order])] = terrain
      # Tell the player the have now lost a priest.
      player.sacrifice_priest_to_order()
    else:
      spaces_to_attempt = 1
    curr_pos = self.positions[order][terrain]
    expected_pos = curr_pos + spaces_to_attempt
    power_collected = sum([
        power for pos, power in CultBoard.ADDITIONAL_POWER.items()
        if curr_pos < pos and pos <= expected_pos
    ])
    if expected_pos < CultBoard.TOWN_KEY_REQUIRED:
      self.positions[order][terrain] = expected_pos
    # We've maxed the cult-board. We might end up moving less than expected.
    # Check to see if we can even take the town right now.
    elif max(self.positions[order].values()
             ) < CultBoard.TOWN_KEY_REQUIRED and player.use_town_key():
      self.positions[order][terrain] = CultBoard.TOWN_KEY_REQUIRED
    else:
      power_collected -= min(3, power_collected)
      self.positions[order][terrain] = CultBoard.TOWN_KEY_REQUIRED - 1
    return (self.positions[order][terrain] - curr_pos, power_collected)
