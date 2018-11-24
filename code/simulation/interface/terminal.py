from typing import Any, List, Optional, Set

from simulation.interface import io
from simulation.core import common
from simulation.core import faction
from simulation.core import player
from simulation.core import board


class CommandLine(io.IO):
  """Class which handles prompting and collecting user responses/actions"""
  MAX_INPUT_CHARS = 25

  def __init__(self):
    pass

  def _VerticalSpace(self):
    print("""


    """)

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
    self._VerticalSpace()
    print(r"""
      Welcome to TM! A copy of the rulebook is located at 
      http://www.feuerland-spiele.de/dateien/Terra_Mystica_EN_1.0_.pdf
      """)

  def RequestNumberOfPlayers(self) -> int:
    self._VerticalSpace()
    return self._RequestInteger("Enter the number of players playing?: ")

  def RequestPlayerNames(self, num_players: int) -> List[str]:
    self._VerticalSpace()
    return [
        self._RequestString("Name for Player %s?: " % (i + 1))
        for i in range(num_players)
    ]

  def _DisplayPrintableValue(self, value: Any) -> None:
    print(str(value))

  def _DisplayMessage(self, msg: str) -> None:
    print("============== %s ==============" % msg)

  def DisplayScoringTiles(self, tiles: List[common.ScoringTile]) -> None:
    self._VerticalSpace()
    self._DisplayMessage("Scoring Tiles")
    for tile in tiles:
      self._DisplayPrintableValue(tile)

  def DisplayBonusCards(self, cards: List[common.BonusCard]) -> None:
    self._VerticalSpace()
    self._DisplayMessage("Bonus Tiles")
    for card in cards:
      self._DisplayPrintableValue(card)

  def _DisplayFactions(self, factions: List[faction.Faction]) -> None:
    for available_faction in factions:
      print(str(available_faction))

  def RequestPlayerFactions(
      self, player_names: List[str],
      available: List[faction.Faction]) -> List[faction.Faction]:
    self._VerticalSpace()
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

  def InvalidInput(self):
    self._VerticalSpace()
    print("That's not valid! Please try again.")

  def InformInitialDwellingPlacement(self) -> None:
    self._VerticalSpace()
    self._DisplayMessage("Placing initial settlements!")

  def _NamePrefix(self, pl: player.Player) -> str:
    return "%s [%s]" % (type(pl.faction).__name__, pl.name)

  def RequestLocation(self, pl: player.Player) -> board.Position:
    self._VerticalSpace()
    while True:
      reqStr = self._RequestString(
          "%s - Select a tile for the action: " % self._NamePrefix(pl))
      pos: Optional[board.Position] = board.ParsePosition(reqStr)
      if pos:
        return pos
      print("Invalid position %s requested. Please try again." % reqStr)

  def RequestBonusCardSelection(self, pl: player.Player,
                                available: List[common.BonusCard]) -> int:
    self._VerticalSpace()
    for i, card in enumerate(available):
      print("%s : %s" % (i + 1, card))
    while True:
      index: int = self._RequestInteger(
          "%s - Select the index of the bonus card to take: " %
          self._NamePrefix(pl))
      if 1 <= index and index <= len(available):
        return index - 1
      print("The selected index %s is out of range [%s, %s)!" %
            (index, 1, len(available)))
