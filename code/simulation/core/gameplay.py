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
    # self.scoring_tiles[i] is the scorling tile for the (i+1)-th round of
    # gameplay.
    self.scoring_tiles: List[common.ScoringTile] = scoring_tiles
    # just a list of the currently available bonus tiles.
    self.available_bonus_cards: List[common.BonusCard] = bonus_cards

    # The index of the current round being played.
    self.round_index: int = 0

    self.board = board.GameBoard()
    self.cultboard = cult.CultBoard(
        factions=[player.faction for player in self.players])
    self.interface = interface

  def player_has_opponent_neighbors_at_position(self,
                                                player: player_module.Player,
                                                pos: board.Position) -> bool:
    home: common.Terrain = player.faction.home_terrain()
    neighbors: List[common.Terrain] = [
        terrain for _, terrain in self.board.neighbor_structure_owners(pos)
        if terrain != home
    ]
    return len(neighbors) > 0

  def _transform_and_build(self, player: player_module.Player) -> None:
    while True:
      pos: board.Position = self.interface.request_location(player)  # noqa
      # final_terrains: List[common.Terrain] = player.ReachableTerrains()
      pass

  def _place_initial_dwellings(self, player: player_module.Player) -> None:
    while True:
      pos: board.Position = self.interface.request_location(player)
      can_be_built = self.board.can_be_built(
          pos,
          structure=common.Structure.DWELLING,
          final_terrain=[player.faction.home_terrain()])
      if not can_be_built:
        self.interface.invalid_input()
        continue

      self.board.build(pos, structure=common.Structure.DWELLING)
      # This one is built for free!
      player.build(
          common.Structure.DWELLING,
          adjacentEnemies=self.player_has_opponent_neighbors_at_position(
              player, pos),
          free=True)
      break

  def initialize_dwellings(self) -> None:
    # 1st dwellings.
    self.interface.inform_initial_dwelling_placement()
    for player in self.players:
      self._place_initial_dwellings(player)

    # 2nd dwellings.
    self.interface.inform_initial_dwelling_placement()
    for player in reversed(self.players):
      self._place_initial_dwellings(player)

    # TODO(luis): Handle Chaos Magicians and Nomads

  def swap_bonus_cards(self, player: player_module.Player) -> None:
    """The player has passed (usually) and we need to swap cards."""
    selected_index: int = self.interface.request_bonus_card_selection(
        player, self.available_bonus_cards)
    selected_card: common.BonusCard = self.available_bonus_cards.pop(
        selected_index)
    returnedCard: Optional[common.BonusCard] = player.take_bonus_card(
        selected_card)
    if returnedCard:
      self.available_bonus_cards.append(returnedCard)

  def _end_round_for_bonus_cards(self) -> None:
    """Perform required activities at the end of a round"""
    for card in self.available_bonus_cards:
      card.coins += 1

  def end_round(self) -> None:
    # TODO....
    self._end_round_for_bonus_cards()

  def initialize_bonus_cards(self) -> None:
    for player in reversed(self.players):
      self.swap_bonus_cards(player)
    self._end_round_for_bonus_cards()

  def income_phase(self) -> None:
    """Go through the income phase of a Round"""
    for player in self.players:
      player.collect_phase_ii_income()

  def action_phase(self) -> None:
    """Execute the action phase. self.players is already in order."""
    for player in self.players:
      pass


def select_game_scoring_tiles() -> List[common.ScoringTile]:
  return random.sample(list(common.ScoringTile), Game.NUM_ROUNDS)


def select_game_bonus_cards(num_players: int) -> List[common.BonusCard]:
  return random.sample(list(common.BonusCard), num_players + 3)
