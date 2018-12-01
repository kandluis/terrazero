import copy

from typing import Any, Dict, List, Optional

from simulation.core import common
from simulation.core import faction
from simulation import utils


class Player:
  MAX_PRIESTS = 7

  def __init__(self, name: str, player_faction: faction.Faction) -> None:
    self.name = name
    self.faction: faction.Faction = player_faction
    self.power: Dict[common.PowerBowl, int] = player_faction.StartingPower()
    self.resources: common.Resources = player_faction.StartingResources()
    self.shipping: int = player_faction.StartingShipping()
    # Mapping from TowKey to whether or not we've used it already.
    self.used_town_keys: Dict[common.TownKey, bool] = {}

    # Map from types to the number the player currently has on his/her board.
    # We must make a copy!
    self.structures: Dict[common.Structure, int] = copy.deepcopy(
        faction.Faction.TOTAL_STRUCTURES)
    # Same as above but the structures already built.
    self.built_structures: Dict[common.Structure, int] = {
        common.Structure.DWELLING: 0,
        common.Structure.TRADING_POST: 0,
        common.Structure.TEMPLE: 0,
        common.Structure.SANCTUARY: 0,
        common.Structure.STRONGHOLD: 0,
    }

    # Victory points. All players start with 20.
    self.victory_points = 20

    # We explicitly track how many priests are still in play (if a priest is sent to
    # an order, it is no longer in play. The player should be informed of this)
    self.priests_still_in_play = Player.MAX_PRIESTS

    # Tracks the bonus card which the player currently has. This is optional
    # since it is not selected until after players set settlements. However,
    # once set, it should NEVER be empty in the future since players always take a
    # replacement card.
    self.bonus_card: Optional[common.BonusCard] = None

    # A list of favor tiles the player currently holds.
    self.favor_tiles: List[common.FavorTile] = []

    # Tracks the number of spades

  def SacrificePriestToOrder(self) -> None:
    self.priests_still_in_play -= 1

  def _MaxUseablePower(self) -> int:
    count: int = self.power[common.PowerBowl.III]
    return count + (self.power[common.PowerBowl.II] // 2)

  def _PowerRequiredToZeroNegativeReources(self,
                                           resources: common.Resources) -> int:
    # The costs of each.
    PRIESTS: int = 5
    WORKERS: int = 3
    COINS: int = 1

    required = 0
    if resources.coins < 0:
      required += (-COINS * resources.coins)
    if resources.workers < 0:
      required += (-WORKERS * resources.workers)
    if resources.priests < 0:
      required += (-PRIESTS * resources.priests)
    return required

  def _CanBurnPowerForMissingResources(self,
                                       resources: common.Resources) -> bool:
    """If all resources are positive, this trivially is true"""
    return (self._MaxUseablePower() >=
            self._PowerRequiredToZeroNegativeReources(resources))

  def CanBuild(self, structure, adjacentEnemies) -> bool:
    """Asks if the player can possibly build this structure with his available resources"""
    # Can't possible build if we don't have any such structures left
    # on the board.
    if self.structures[structure] <= 0:
      return False
    cost: common.Resources = self.faction.StructureCost(
        structure, adjacentEnemies)
    remainingResources = self.resources - cost
    if remainingResources.IsValid():
      return True
    return self._CanBurnPowerForMissingResources(remainingResources)

  def Build(self,
            structure: common.Structure,
            adjacentEnemies: bool,
            free: bool = False) -> None:
    """Asks the player to build the specified structure.
    If free is true, this costs the player no resources"""
    if not free and not self.CanBuild(structure, adjacentEnemies):
      raise utils.InternalError(
          "Attempted to build %s which is impossible with current resources: %s and power: %s"
          % (structure, self.resources, self.power))
    # Even though we haven't paid, we assume it's possible to build it.
    # It's invalid to call this function otherwise.
    self.structures[structure] -= 1
    self.built_structures[structure] += 1
    if free:
      return
    cost: common.Resources = self.faction.StructureCost(
        structure, adjacentEnemies)
    self.resources -= cost
    if self.resources.IsValid():
      return
    self.UsePower(self._PowerRequiredToZeroNegativeReources(self.resources))
    self.resources.ForceValid()
    return

  def CollectPhaseIIncome(self) -> None:
    """Should be called to inform the player that he/she needs to collect income."""
    proposed_income: common.Income = self.faction.IncomeForStructures(
        self.built_structures)
    assert self.bonus_card is not None
    proposed_income += self.bonus_card.PlayerIncome()
    for favor_tile in self.favor_tiles:
      proposed_income += favor_tile.PlayerIncome()
    self.resources += proposed_income

    # The number of priests that can be collected is bound.
    self.resources.priests = max(self.resources.priests,
                                 self.priests_still_in_play)

    # We now collect the power.
    self.GainPower(proposed_income.power)

  def UseTownKey(self) -> bool:
    """Returns true if an available town keys was used. False if no town key is available."""
    for key, used in self.used_town_keys.items():
      if not used:
        self.used_town_keys[key] = True
        return True
    return False

  def CanUsePower(self, amount: int) -> bool:
    """Returns true of the power can use the amount of power specifid. May require burning"""
    return self._MaxUseablePower() >= amount

  def UsePower(self, amount: int) -> None:
    """The player will use up the specified amount of power, even if it requires burning.

    Raises an error if it doesn't have enough power"""
    assert amount >= 0
    if not self.CanUsePower(amount):
      raise utils.InternalError(
          "Requesting to use %s power, which is not possible! Current power: %s."
          % (amount, self.power))
    # We assume you'll always use power from Bowl 3 downwards.
    toMove: int = min(amount, self.power[common.PowerBowl.III])
    amount -= toMove
    self.power[common.PowerBowl.III] -= toMove
    self.power[common.PowerBowl.I] += toMove
    if amount == 0:
      return
    toMove = min(2 * amount, self.power[common.PowerBowl.II])
    amount -= (toMove // 2)
    if amount != 0:
      raise utils.InternalError(
          "Something has gone terrible wrong! We thought we could use %s power, "
          "but we can't! Power: %s" % (amount, self.power))
    self.power[common.PowerBowl.II] -= toMove
    self.power[common.PowerBowl.I] += (toMove // 2)
    return

  def TakeBonusCard(self,
                    card: common.BonusCard) -> Optional[common.BonusCard]:
    """Takes the given card and returns the card the player currently holds,
    if any"""
    oldCard = self.bonus_card
    # NWe need to handle if we had a shipping card.
    if oldCard is None and oldCard == common.BonusCard.POWER3_SHIPPING:
      assert self.shipping > 0
      assert card != common.BonusCard.POWER3_SHIPPING
      self.shipping -= 1
    self.bonus_card = card
    # Move the coins (if any) from the bonus card to the income.
    self.resources.coins += self.bonus_card.coins
    self.bonus_card.coins = 0

    # We need to handle the shipping card.
    if card == common.BonusCard.POWER3_SHIPPING:
      assert oldCard != common.BonusCard.POWER3_SHIPPING
      self.shipping += 1

    return oldCard

  def GainTown(self, townKey: common.TownKey) -> None:
    self.used_town_keys[townKey] = False

  def GainPower(self, power: int) -> None:
    # Gain the given amount of power. Overflowing power is automatically
    # converted to coins.
    remainingPower: int = power
    assert remainingPower >= 0
    if remainingPower == 0:
      return None

    if self.power[common.PowerBowl.I] > 0:
      toMove = min(self.power[common.PowerBowl.I], remainingPower)
      self.power[common.PowerBowl.I] -= toMove
      self.power[common.PowerBowl.II] += toMove
      remainingPower -= toMove

    if remainingPower == 0:
      return None

    # If we still have power, power I bowl must be empty at this point.
    # Otherwise, we have no power left.
    assert self.power[common.PowerBowl.I] == 0
    if self.power[common.PowerBowl.II] > 0:
      toMove = min(self.power[common.PowerBowl.II], remainingPower)
      self.power[common.PowerBowl.II] -= toMove
      self.power[common.PowerBowl.III] += toMove
      remainingPower -= toMove

    if remainingPower == 0:
      return None

    # If we still have power, power II bowl must be empty at this point.
    assert self.power[common.PowerBowl.II] == 0

    # Spending an even amount of excess power always makes sense and is
    # optimal.
    self.resources.coins += int(remainingPower / 2)
    # TODO(nautilik): We assume player will want to spend remaining 1 power,
    # even if this means he'll end up with power stuck in
    # common.PowerBowl.II.
    if remainingPower % 2 == 1:
      self.power[common.PowerBowl.III] -= 1
      self.power[common.PowerBowl.II] += 1
      self.resources.coins += 1

    return None
