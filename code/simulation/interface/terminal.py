from typing import Any, List, Set

from simulation.core import common
from simulation.core import faction


class CommandLine:
  """Class which handles prompting and collecting user responses/actions"""
  MAX_INPUT_CHARS = 25

  def __init__(self):
    pass

  def _RequestInteger(self, message: str) -> int:
    while True:
      try:
        return int(input(message))
      except ValueError:
        print("Invalid value entered!")

  def _RequestString(self, message: str) -> str:
    while True:
      candidate = input(message)
      if len(candidate) < CommandLine.MAX_INPUT_CHARS:
        return candidate
      print("Entered value is too long!")

  def WelcomeMessage(self) -> None:
    print(r"""
      Welcome to TM! A copy of the rulebook is located at 
      http://www.feuerland-spiele.de/dateien/Terra_Mystica_EN_1.0_.pdf
      """)

  def RequestNumberOfPlayers(self) -> int:
    return self._RequestInteger("Enter the number of players playing?: ")

  def RequestPlayerNames(self, num_players: int) -> List[str]:
    return [
        self._RequestString("Name for Player %s?: " % (i + 1))
        for i in range(num_players)
    ]

  def _DisplayPrintableValue(self, value: Any) -> None:
    print(str(value))

  def _DisplayMessage(self, msg: str) -> None:
    print("============== %s ==============" % msg)

  def DisplayScoringTiles(self, tiles: List[common.ScoringTile]) -> None:
    self._DisplayMessage("Scoring Tiles")
    for tile in tiles:
      self._DisplayPrintableValue(tile)

  def DisplayBonusCards(self, cards: List[common.BonusCard]) -> None:
    self._DisplayMessage("Bonus Tiles")
    for card in cards:
      self._DisplayPrintableValue(card)

  def _DisplayFactions(self, factions: List[faction.Faction]) -> None:
    for available_faction in factions:
      print(str(available_faction))

  def RequestPlayerFactions(
      self, player_names: List[str],
      available: List[faction.Faction]) -> List[faction.Faction]:
    self._DisplayMessage("Faction Selection")
    self._DisplayMessage("Available Factions")
    self._DisplayFactions(available)

    used: Set[str] = set()
    selected: List[faction.Faction] = []
    for player_name in player_names:
      while True:
        candidate = self._RequestString(
            "%s, please select an available faction by name: " % player_name)
        if candidate in used:
          print(
              "The requested faction %s has already been picked!" % candidate)
          continue
        try:
          class_ = getattr(faction, candidate)
        except AttributeError:
          print("The requested faction %s is not available!" % candidate)
          continue
        used.add(candidate)
        selected.append(class_())
        break
    return selected
