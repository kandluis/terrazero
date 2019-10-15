import unittest
import random

from unittest import mock

from simulation.core import board
from simulation.core import cult
from simulation.core import gameplay
from simulation.core import common
from simulation.core import player
from simulation.interface import io


class TestGameObject(unittest.TestCase):
  def setUp(self) -> None:
    self.mock_interface = mock.Mock(auto_spec=io.IO)

  def test_selecting_game_scoring_tiles(self) -> None:
    random.seed(1)
    self.assertCountEqual(gameplay.select_game_scoring_tiles(), [
        common.ScoringTile.TP_WATER4_SPADE,
        common.ScoringTile.STRONGHOLD_AIR2_WORKER,
        common.ScoringTile.TP_AIR4_SPADE,
        common.ScoringTile.STRONGHOLD_FIRE2_WORKER,
        common.ScoringTile.SPADE_EARTH_COIN,
        common.ScoringTile.DWELLING_WATER4_PRIEST,
    ])

    random.seed(2)
    self.assertCountEqual(gameplay.select_game_scoring_tiles(), [
        common.ScoringTile.TP_AIR4_SPADE,
        common.ScoringTile.STRONGHOLD_FIRE2_WORKER,
        common.ScoringTile.DWELLING_FIRE4_POWER4,
        common.ScoringTile.TP_WATER4_SPADE,
        common.ScoringTile.DWELLING_WATER4_PRIEST,
        common.ScoringTile.STRONGHOLD_AIR2_WORKER,
    ])

    random.seed(3)
    self.assertCountEqual(gameplay.select_game_scoring_tiles(), [
        common.ScoringTile.TOWN_EARTH4_SPADE,
        common.ScoringTile.STRONGHOLD_AIR2_WORKER,
        common.ScoringTile.DWELLING_FIRE4_POWER4,
        common.ScoringTile.DWELLING_WATER4_PRIEST,
        common.ScoringTile.TP_WATER4_SPADE,
        common.ScoringTile.STRONGHOLD_FIRE2_WORKER,
    ])

  def test_selecting_bonus_cards_for_players(self) -> None:
    self.assertEqual(len(gameplay.select_game_bonus_cards(num_players=3)),
                     3 + 3)
    self.assertEqual(len(gameplay.select_game_bonus_cards(num_players=5)),
                     5 + 3)

  @mock.patch.object(cult, 'CultBoard')
  def test_opponent_at_position(self, _: mock.Mock) -> None:
    player1 = mock.Mock(auto_spec=player.Player)
    player1.faction.home_terrain.return_value = common.Terrain.MOUNTAIN

    player2 = mock.Mock(auto_spec=player.Player)
    player2.faction.home_terrain.return_value = common.Terrain.WASTELAND

    # Board will always tell us we have a dwelling on a mountain terrain
    # and a dwelling on a wasteland terrain next to us.
    mock_board = mock.Mock(auto_spec=board.GameBoard)
    mock_board.neighbor_structure_owners.return_value = set(
        ((common.Structure.DWELLING, common.Terrain.MOUNTAIN),
         (common.Structure.DWELLING, common.Terrain.WASTELAND)))

    game = gameplay.Game(players=[player1, player2],
                         scoring_tiles=[],
                         bonus_cards=[],
                         interface=self.mock_interface)
    game.board = mock_board

    self.assertTrue(
        game.player_has_opponent_neighbors_at_position(
            player1, board.Position(row="A", column=1)))

  @mock.patch.object(cult, 'CultBoard')
  def test_only_myself_around_me(self, _: mock.Mock) -> None:
    player1 = mock.Mock(auto_spec=player.Player)
    player1.faction.home_terrain.return_value = common.Terrain.MOUNTAIN

    player2 = mock.Mock(auto_spec=player.Player)
    player2.faction.home_terrain.return_value = common.Terrain.WASTELAND

    game = gameplay.Game(players=[player1, player2],
                         scoring_tiles=[],
                         bonus_cards=[],
                         interface=self.mock_interface)

    # Board will always tell us we have a dwelling on a mountain terrain
    # and a dwelling on a wasteland terrain next to us.
    mock_board = mock.Mock(auto_spec=board.GameBoard)
    mock_board.neighbor_structure_owners.return_value = set([
        (common.Structure.DWELLING, common.Terrain.MOUNTAIN),
        (common.Structure.DWELLING, common.Terrain.MOUNTAIN)
    ])

    game.board = mock_board

    self.assertFalse(
        game.player_has_opponent_neighbors_at_position(
            player1, board.Position(row="A", column=1)))

  @mock.patch.object(cult, 'CultBoard')
  def test_no_one_around_me(self, _: mock.Mock) -> None:
    player1 = mock.Mock(auto_spec=player.Player)
    player1.faction.home_terrain.return_value = common.Terrain.MOUNTAIN

    player2 = mock.Mock(auto_spec=player.Player)
    player2.faction.home_terrain.return_value = common.Terrain.WASTELAND

    # Board will always tell us we have a dwelling on a mountain terrain
    # and a dwelling on a wasteland terrain next to us.
    mock_board = mock.Mock(auto_spec=board.GameBoard)
    mock_board.neighbor_structure_owners.return_value = []

    game = gameplay.Game(players=[player1, player2],
                         scoring_tiles=[],
                         bonus_cards=[],
                         interface=self.mock_interface)
    game.board = mock_board

    self.assertFalse(
        game.player_has_opponent_neighbors_at_position(
            player1, board.Position(row="A", column=1)))

  def test_player_limits(self) -> None:
    with self.assertRaises(AssertionError):
      gameplay.Game(players=[mock.Mock(auto_spec=player.Player)],
                    scoring_tiles=[],
                    bonus_cards=[],
                    interface=self.mock_interface)

    with self.assertRaises(AssertionError):
      gameplay.Game(
          players=[mock.Mock(auto_spec=player.Player) for _ in range(6)],
          scoring_tiles=[],
          bonus_cards=[],
          interface=self.mock_interface)
