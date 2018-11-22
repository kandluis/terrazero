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
  def WelcomeMessage(self) -> None:
    pass

  @abc.abstractmethod
  def RequestNumberOfPlayers(self) -> int:
    pass

  @abc.abstractmethod
  def RequestPlayerNames(self, num_players: int) -> List[str]:
    pass

  @abc.abstractmethod
  def DisplayScoringTiles(self, tiles: List[common.ScoringTile]) -> None:
    pass

  @abc.abstractmethod
  def DisplayBonusCards(self, cards: List[common.BonusCard]) -> None:
    pass

  @abc.abstractmethod
  def RequestPlayerFactions(
      self, player_names: List[str],
      available: List[faction.Faction]) -> List[faction.Faction]:
    pass

  @abc.abstractmethod
  def InvalidInput(self) -> None:
    pass

  @abc.abstractmethod
  def InformInitialDwellingPlacement(self) -> None:
    pass

  @abc.abstractmethod
  def RequestLocation(self, pl: player.Player) -> board.Position:
    pass