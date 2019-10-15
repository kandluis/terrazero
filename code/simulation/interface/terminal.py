from typing import Any, List, Optional, Set

from simulation.interface import io
from simulation.core import common
from simulation.core import faction
from simulation.core import player
from simulation.core import board


class CommandLine(io.IO):
  """Class which handles prompting and collecting user responses/actions"""
  _MAX_INPUT_CHARS = 25

  def __init__(self) -> None:
    pass

  def _vertical_space(self) -> None:
    print("""


    """)

  def _request_integer(self, message: str) -> int:
    while True:
      try:
        return int(input(message))
      except ValueError:
        print("Invalid value entered!")

  def _request_string(self, message: str) -> str:
    while True:
      candidate = input(message)
      if len(candidate) < CommandLine._MAX_INPUT_CHARS:
        return candidate
      print("Entered value is too long!")

  def welcome_message(self) -> None:
    self._vertical_space()
    print(r"""
      Welcome to TM! A copy of the rulebook is located at
      http://www.feuerland-spiele.de/dateien/Terra_Mystica_EN_1.0_.pdf
      """)

  def request_number_of_players(self) -> int:
    self._vertical_space()
    return self._request_integer("Enter the number of players playing?: ")

  def request_player_names(self, num_players: int) -> List[str]:
    self._vertical_space()
    return [
        self._request_string("Name for Player %s?: " % (i + 1))
        for i in range(num_players)
    ]

  def _display_printable_value(self, value: Any) -> None:
    print(str(value))

  def _display_message(self, msg: str) -> None:
    print("============== %s ==============" % msg)

  def display_scoring_tiles(self, tiles: List[common.ScoringTile]) -> None:
    self._vertical_space()
    self._display_message("Scoring Tiles")
    for tile in tiles:
      self._display_printable_value(tile)

  def display_bonus_cards(self, cards: List[common.BonusCard]) -> None:
    self._vertical_space()
    self._display_message("Bonus Tiles")
    for card in cards:
      self._display_printable_value(card)

  def _display_factions(self, factions: List[faction.Faction]) -> None:
    for available_faction in factions:
      print(str(available_faction))

  def request_player_factions(self, player_names: List[str],
                              available: List[faction.Faction]
                              ) -> List[faction.Faction]:
    self._vertical_space()
    self._display_message("Faction Selection")
    self._display_message("Available Factions")
    self._display_factions(available)

    used: Set[str] = set()
    selected: List[faction.Faction] = []
    for player_name in player_names:
      while True:
        candidate = self._request_string(
            "%s, please select an available faction by name: " % player_name)
        if candidate in used:
          print("The requested faction %s has already been picked!" %
                candidate)
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

  def invalid_input(self) -> None:
    self._vertical_space()
    print("That's not valid! Please try again.")

  def inform_initial_dwelling_placement(self) -> None:
    self._vertical_space()
    self._display_message("Placing initial settlements!")

  def _name_prefix(self, pl: player.Player) -> str:
    return "%s [%s]" % (type(pl.faction).__name__, pl.name)

  def request_location(self, pl: player.Player) -> board.Position:
    self._vertical_space()
    while True:
      reqStr = self._request_string("%s - Select a tile for the action: " %
                                    self._name_prefix(pl))
      pos: Optional[board.Position] = board.ParsePosition(reqStr)
      if pos:
        return pos
      print("Invalid position %s requested. Please try again." % reqStr)

  def request_bonus_card_selection(self, pl: player.Player,
                                   available: List[common.BonusCard]) -> int:
    self._vertical_space()
    for i, card in enumerate(available):
      print("%s : %s" % (i + 1, card))
    while True:
      index: int = self._request_integer(
          "%s - Select the index of the bonus card to take: " %
          self._name_prefix(pl))
      if 1 <= index and index <= len(available):
        return index - 1
      print("The selected index %s is out of range [%s, %s)!" %
            (index, 1, len(available)))
