import abc

from typing import List

from simulation.core import common
from simulation.core import faction
from simulation.core import board
from simulation.core import player


class IO(abc.ABC):
  """
  Interface for accessing the UI.
  """

  @abc.abstractmethod
  def welcome_message(self) -> None:
    pass

  @abc.abstractmethod
  def request_number_of_players(self) -> int:
    pass

  @abc.abstractmethod
  def request_player_names(self, num_players: int) -> List[str]:
    pass

  @abc.abstractmethod
  def display_scoring_tiles(self, tiles: List[common.ScoringTile]) -> None:
    pass

  @abc.abstractmethod
  def display_bonus_cards(self, cards: List[common.BonusCard]) -> None:
    pass

  @abc.abstractmethod
  def request_player_factions(self, player_names: List[str],
                              available: List[faction.Faction]
                              ) -> List[faction.Faction]:
    pass

  @abc.abstractmethod
  def invalid_input(self) -> None:
    pass

  @abc.abstractmethod
  def inform_initial_dwelling_placement(self) -> None:
    pass

  @abc.abstractmethod
  def request_location(self, pl: player.Player) -> board.Position:
    pass

  @abc.abstractmethod
  def request_bonus_card_selection(self, pl: player.Player,
                                   available: List[common.BonusCard]) -> int:
    pass
