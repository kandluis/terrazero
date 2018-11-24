import random

from typing import List, Optional

from simulation.core import common
from simulation.core import player as player_module
from simulation.core import cult
from simulation.interface import io
from simulation.core import board


class Game:
  NUM_ROUNDS = 6
  MIN_PLAYERS = 2
  MAX_PLAYERS = 5

  def __init__(self, players: List[player_module.Player],
               scoring_tiles: List[common.ScoringTile],
               bonus_cards: List[common.BonusCard], interface: io.IO) -> None:
    self.num_players = len(players)
    assert Game.MIN_PLAYERS <= self.num_players <= Game.MAX_PLAYERS
    # self.players[i] is the player which will go on turn i.
    self.players = players
    # self.scoring_tiles[i] is the scorling tile for the (i+1)-th round of gameplay.
    self.scoring_tiles: List[common.ScoringTile] = scoring_tiles
    # just a list of the currently available bonus tiles.
    self.available_bonus_cards: List[common.BonusCard] = bonus_cards

    # The index of the current round being played.
    self.round_index: int = 0

    self.board = board.GameBoard()
    self.cultboard = cult.CultBoard(
        factions=[player.faction for player in self.players])
    self.interface = interface

  def PlayerHasOpponentNeighborsAtPosition(self, player: player_module.Player,
                                           pos: board.Position) -> bool:
    home: common.Terrain = player.faction.HomeTerrain()
    neighbors: List[common.Terrain] = [
        terrain for _, terrain in self.board.NeighborStructureOwners(pos)
        if terrain != home
    ]
    return len(neighbors) > 0

  def _TransformAndBuild(self, player) -> None:
    while True:
      pos: board.Position = self.interface.RequestLocation(player)
      final_terrains: List[common.Terrain] = player.ReachableTerrains()
      pass

  def _PlaceInitialDWellings(self, player) -> None:
    while True:
      pos: board.Position = self.interface.RequestLocation(player)
      if not self.board.CanBeBuilt(
          pos,
          structure=common.Structure.DWELLING,
          final_terrain=[player.faction.HomeTerrain()]):
        self.interface.InvalidInput()
        continue

      self.board.Build(pos, structure=common.Structure.DWELLING)
      # This one is built for free!
      player.Build(
          common.Structure.DWELLING,
          adjacentEnemies=self.PlayerHasOpponentNeighborsAtPosition(
              player, pos),
          free=True)
      break

  def InitializeDwellings(self) -> None:
    # 1st dwellings.
    self.interface.InformInitialDwellingPlacement()
    for player in self.players:
      self._PlaceInitialDWellings(player)

    # 2nd dwellings.
    self.interface.InformInitialDwellingPlacement()
    for player in reversed(self.players):
      self._PlaceInitialDWellings(player)

    # TODO(luis): Handle Chaos Magicians and Nomads

  def SwapBonusCards(self, player: player_module.Player) -> None:
    """The player has passed (usually) and we need to swap cards."""
    selected_index: int = self.interface.RequestBonusCardSelection(
        player, self.available_bonus_cards)
    selected_card: common.BonusCard = self.available_bonus_cards.pop(
        selected_index)
    returnedCard: Optional[common.BonusCard] = player.TakeBonusCard(
        selected_card)
    if returnedCard:
      self.available_bonus_cards.append(returnedCard)

  def _EndRoundForBonusCards(self):
    """Perform required activities at the end of a round"""
    for card in self.available_bonus_cards:
      card.coins += 1

  def EndRound(self):
    # TODO....
    self._EndRoundForBonusCards()

  def InitializeBonusCards(self) -> None:
    for player in reversed(self.players):
      self.SwapBonusCards(player)
    self._EndRoundForBonusCards()

  def IncomePhase(self) -> None:
    """Go through the income phase of a Round"""
    for player in self.players:
      player.CollectPhaseIIncome()

  def ActionPhase(self) -> None:
    """Execute the action phase. self.players is already in order."""
    for player in self.players:
      pass


def SelectGameScoringTiles() -> List[common.ScoringTile]:
  return random.sample(list(common.ScoringTile), Game.NUM_ROUNDS)


def SelectGameBonusCards(num_players: int) -> List[common.BonusCard]:
  return random.sample(list(common.BonusCard), num_players + 3)
