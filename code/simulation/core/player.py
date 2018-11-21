from typing import Dict

from simulation.core import common
from simulation.core import faction


class Player:
  def __init__(self, player_faction: faction.Faction):
    self.faction: faction.Faction = player_faction
    self.power: Dict[common.PowerBowl, int] = player_faction.StartingPower()
    self.coins: int = player_faction.StartingCoins()
    self.workers: int = player_faction.StartingWorkers()
    self.shipping: int = player_faction.StartingShipping()
    # Mapping from TowKey to whether or not we've used it already.
    self.used_town_keys: Dict[common.TownKey, bool] = {}
    self.bridges: int = 0
    self.priests: int = player_faction.StartingPriests()

    # Victory points. All players start with 20.
    self.victory_points = 20

  def UseTownKey(self) -> bool:
    """Returns true if an available town keys was used. False if no town key is available."""
    for key, used in self.used_town_keys.items():
      if not used:
        self.used_town_keys[key] = True
        return True
    return False

  def GainTown(self, townKey: common.TownKey) -> None:
    self.used_town_keys[townKey] = False

  def GainPower(self, power: int) -> None:
    # Gain the given amount of power. Overflowing power is automatically
    # converted to coins.
    remainingPower: int = power
    assert remainingPower >= 0
    if remainingPower == 0:
      return

    if self.power[common.PowerBowl.I] > 0:
      toMove = min(self.power[common.PowerBowl.I], remainingPower)
      self.power[common.PowerBowl.I] -= toMove
      self.power[common.PowerBowl.II] += toMove
      remainingPower -= toMove

    if remainingPower == 0:
      return

    # If we still have power, power I bowl must be empty at this point.
    # Otherwise, we have no power left.
    assert self.power[common.PowerBowl.I] == 0
    if self.power[common.PowerBowl.II] > 0:
      toMove = min(self.power[common.PowerBowl.II], remainingPower)
      self.power[common.PowerBowl.II] -= toMove
      self.power[common.PowerBowl.III] += toMove
      remainingPower -= toMove

    if remainingPower == 0:
      return

    # If we still have power, power II bowl must be empty at this point.
    assert self.power[common.PowerBowl.II] == 0

    # Spending an even amount of excess power always makes sense and is
    # optimal.
    self.coins += int(remainingPower / 2)
    # TODO(nautilik): We assume player will want to spend remaining 1 power,
    # even if this means he'll end up with power stuck in
    # common.PowerBowl.II.
    if remainingPower % 2 == 1:
      self.power[common.PowerBowl.III] -= 1
      self.power[common.PowerBowl.II] += 1
      self.coins += 1
