from typing import List

from simulation.core import common
from simulation.core import board
from simulation.core import cult
from simulation.core import faction
from simulation.core import gameplay
from simulation.core import player
from simulation.interface import terminal
from simulation.interface import io

NUM_ROUNDS = 6


class GameRunner:
  def __init__(self):
    self.game = self._InitGame()

  def _InitGame(self) -> gameplay.Game:
    interface: io.IO = terminal.CommandLine()
    interface.WelcomeMessage()

    num_players: int = interface.RequestNumberOfPlayers()
    player_names: List[str] = interface.RequestPlayerNames(num_players)

    scoring_tiles: List[common.ScoringTile] = gameplay.SelectGameScoringTiles()
    bonus_cards: List[common.BonusCard] = gameplay.SelectGameBonusCards(
        num_players=num_players)

    interface.DisplayScoringTiles(scoring_tiles)
    interface.DisplayBonusCards(bonus_cards)
    player_factions = interface.RequestPlayerFactions(
        player_names, available=faction.AllAvailable())

    players = [
        player.Player(name=player_name, player_faction=selected_faction)
        for player_name, selected_faction in zip(player_names, player_factions)
    ]
    return gameplay.Game(players, scoring_tiles, bonus_cards, interface)

  def execute(self) -> None:
    self.game.InitializeDwellings()
    self.game.InitializeBonusCards()
    for _ in range(NUM_ROUNDS):
      self.game.IncomePhase()
