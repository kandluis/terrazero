import unittest

from simulation.core import common
from simulation import utils


class TestResources(unittest.TestCase):
  def test_validation(self) -> None:
    self.assertTrue(common.Resources().is_valid())
    self.assertTrue(
        common.Resources(coins=1, workers=1, bridges=1, priests=1).is_valid())
    self.assertFalse(common.Resources(coins=-1).is_valid())

  def test_force_valid(self) -> None:
    invalidResources = common.Resources(coins=-1)
    self.assertFalse(invalidResources.is_valid())
    invalidResources.force_valid()
    self.assertTrue(invalidResources.is_valid())

  def test_equality_operator(self) -> None:
    self.assertEqual(
        common.Resources(coins=10, workers=1, bridges=2, priests=4),
        common.Resources(coins=10, workers=1, bridges=2, priests=4))
    self.assertNotEqual(
        common.Resources(coins=10, workers=1, bridges=2, priests=4),
        common.Resources(coins=10, workers=1, bridges=3, priests=4))

  def test_addition_operator(self) -> None:
    self.assertEqual(
        common.Resources(workers=1) + common.Resources(workers=2, priests=4),
        common.Resources(workers=3, priests=4))
    self.assertEqual(
        sum((common.Resources(workers=10),
             common.Resources(workers=2, bridges=4))),
        common.Resources(workers=12, bridges=4))
    resources = common.Resources(workers=10)
    resources += common.Resources(workers=1)
    self.assertEqual(resources, common.Resources(workers=11))

  def test_subtraction(self) -> None:
    self.assertEqual(
        common.Resources(workers=1) - common.Resources(workers=1, priests=4),
        common.Resources(workers=0, priests=-4))
    resources = common.Resources(workers=10)
    resources -= common.Resources(workers=1)
    self.assertEqual(resources, common.Resources(workers=9))


class TestIncome(unittest.TestCase):
  def test_functions_raise_errors(self) -> None:
    with self.assertRaises(utils.InternalError):
      common.Income().is_valid()

    with self.assertRaises(utils.InternalError):
      common.Income().force_valid()

  def test_equality_operator(self) -> None:
    self.assertEqual(
        common.Income(coins=10, workers=1, bridges=2, priests=4, power=10),
        common.Income(coins=10, workers=1, bridges=2, priests=4, power=10))
    self.assertNotEqual(
        common.Income(coins=10, workers=1, bridges=2, priests=4, power=4),
        common.Income(coins=10, workers=1, bridges=2, priests=4, power=3))

  def test_addition_operator(self) -> None:
    self.assertEqual(
        common.Income(power=1) + common.Income(power=2, priests=4),
        common.Income(power=3, priests=4))
    self.assertEqual(
        sum((common.Income(power=10), common.Income(power=2, bridges=4))),
        common.Income(power=12, bridges=4))
    income = common.Income(power=10)
    income += common.Income(power=1)
    self.assertEqual(income, common.Income(power=11))

  def test_subtraction(self) -> None:
    self.assertEqual(
        common.Income(power=1) - common.Income(power=1, priests=4),
        common.Income(power=0, priests=-4))
    income = common.Income(power=10)
    income -= common.Income(power=1)
    self.assertEqual(income, common.Income(power=9))


class TestBonusCard(unittest.TestCase):
  def test_income_from_bonus_cards(self) -> None:
    self.assertEqual(common.BonusCard.PRIEST.player_income(),
                     common.Income(priests=1))
    self.assertEqual(common.BonusCard.WORKER_3POWER.player_income(),
                     common.Income(workers=1, power=3))
    self.assertEqual(common.BonusCard.COIN6.player_income(),
                     common.Income(coins=6))
    self.assertEqual(common.BonusCard.POWER3_SHIPPING.player_income(),
                     common.Income(power=3))
    self.assertEqual(common.BonusCard.SPADE_COIN2.player_income(),
                     common.Income(coins=2))
    self.assertEqual(common.BonusCard.CULT_COIN4.player_income(),
                     common.Income(coins=4))
    self.assertEqual(common.BonusCard.DWELLING_COIN2.player_income(),
                     common.Income(coins=2))
    self.assertEqual(common.BonusCard.TRADING_POST_WORKER.player_income(),
                     common.Income(workers=1))
    self.assertEqual(common.BonusCard.STRONGHOLD_WORKER2.player_income(),
                     common.Income(workers=2))


class TestFavorTile(unittest.TestCase):
  def testIncomeFromFavorTiel(self) -> None:
    self.assertEqual(common.FavorTile.COIN3_FIRE.player_income(),
                     common.Income(coins=3))
    self.assertEqual(common.FavorTile.WORKER_POWER_EARTH2.player_income(),
                     common.Income(workers=1, power=1))
    self.assertEqual(common.FavorTile.POWER4_AIR2.player_income(),
                     common.Income(power=4))
    self.assertEqual(common.FavorTile.TP3VP_WATER.player_income(),
                     common.Income())
    self.assertEqual(common.FavorTile.DWELLING2_EARTH.player_income(),
                     common.Income())
    self.assertEqual(common.FavorTile.TP1234_AIR.player_income(),
                     common.Income())
    self.assertEqual(common.FavorTile.TOWN_FIRE2.player_income(),
                     common.Income())
    self.assertEqual(common.FavorTile.CULTACTION_AIR2.player_income(),
                     common.Income())
    self.assertEqual(common.FavorTile.FIRE3.player_income(), common.Income())
    self.assertEqual(common.FavorTile.WATER3.player_income(), common.Income())
    self.assertEqual(common.FavorTile.EARTH3.player_income(), common.Income())
    self.assertEqual(common.FavorTile.AIR3.player_income(), common.Income())


class TestStructureUpgrades(unittest.TestCase):
  def testDwellingUpgrades(self) -> None:
    structure = common.Structure.DWELLING
    self.assertFalse(structure.is_upgradeable_to(common.Structure.DWELLING))
    self.assertTrue(structure.is_upgradeable_to(common.Structure.TRADING_POST))
    self.assertFalse(structure.is_upgradeable_to(common.Structure.TEMPLE))
    self.assertFalse(structure.is_upgradeable_to(common.Structure.STRONGHOLD))
    self.assertFalse(structure.is_upgradeable_to(common.Structure.SANCTUARY))

  def testTradingPostUpgrades(self) -> None:
    structure = common.Structure.DWELLING
    self.assertFalse(structure.is_upgradeable_to(common.Structure.DWELLING))
    self.assertTrue(structure.is_upgradeable_to(common.Structure.TRADING_POST))
    self.assertFalse(structure.is_upgradeable_to(common.Structure.TEMPLE))
    self.assertFalse(structure.is_upgradeable_to(common.Structure.STRONGHOLD))
    self.assertFalse(structure.is_upgradeable_to(common.Structure.SANCTUARY))
