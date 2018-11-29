import unittest

from simulation.core import common
from simulation import utils


class TestResources(unittest.TestCase):
  def testValidation(self):
    self.assertTrue(common.Resources().IsValid())
    self.assertTrue(
        common.Resources(coins=1, workers=1, bridges=1, priests=1).IsValid())
    self.assertFalse(common.Resources(coins=-1).IsValid())

  def testForceValid(self):
    invalidResources = common.Resources(coins=-1)
    self.assertFalse(invalidResources.IsValid())
    invalidResources.ForceValid()
    self.assertTrue(invalidResources.IsValid())

  def tesEqualityOperator(self):
    self.assertEqual(
        common.Resources(coins=10, workers=1, bridges=2, priests=4, power=10),
        common.Resources(coins=10, workers=1, bridges=2, priests=4, power=10))
    self.assertNotEqual(
        common.Resources(coins=10, workers=1, bridges=2, priests=4, power=10),
        common.Resources(coins=10, workers=1, bridges=3, priests=4, power=10))

  def testAdditionOperator(self):
    self.assertEqual(
        common.Resources(workers=1) + common.Resources(workers=2, priests=4),
        common.Resources(workers=3, priests=4))
    self.assertEqual(
        sum((common.Resources(workers=10), common.Resources(
            worker=2, bridges=4))), common.Resources(workers=12, bridges=4))
    resources = common.Resources(workers=10)
    resources += common.Resources(workers=1, power=4)
    self.assertEqual(resources, common.Resources(workers=11, power=4))

  def testSubtraction(self):
    self.assertEqual(
        common.Resources(workers=1) - common.Resources(workers=1, priests=4),
        common.Resources(workers=0, priests=-4))
    resources = common.Resources(workers=10, power=4)
    resources -= common.Resources(workers=1)
    self.assertEqual(resources, common.Resources(workers=9, power=4))


class TestIncome(unittest.TestCase):
  def testFunctionsRaiseErrors(self):
    with self.assertRaises(utils.InternalError):
      common.Income().IsValid()

    with self.assertRaises(utils.InternalError):
      common.Income().ForceValid()


class TestBonusCard(unittest.TestCase):
  def testIncomeFromBonusCards(self):
    self.assertEqual(common.BonusCard.PRIEST.PlayerIncome(),
                     common.Income(priests=1))
    self.assertEqual(common.BonusCard.WORKER_3POWER.PlayerIncome(),
                     common.Income(workers=1, power=3))
    self.assertEqual(common.BonusCard.COIN6.PlayerIncome(),
                     common.Income(coins=6))
    self.assertEqual(common.BonusCard.POWER3_SHIPPING.PlayerIncome(),
                     common.Income(power=3))
    self.assertEqual(common.BonusCard.SPADE_COIN2.PlayerIncome(),
                     common.Income())
    self.assertEqual(common.BonusCard.CULT_COIN4.PlayerIncome(),
                     common.Income())
    self.assertEqual(common.BonusCard.DWELLING_COIN2.PlayerIncome(),
                     common.Income())
    self.assertEqual(common.BonusCard.TRADING_POST_WORKER.PlayerIncome(),
                     common.Income())
    self.assertEqual(common.BonusCard.STRONGHOLD_WORKER2.PlayerIncome(),
                     common.Income())


class TestFavorTile(unittest.TestCase):
  def testIncomeFromFavorTiel(self):
    self.assertEqual(common.FavorTile.COIN3_FIRE.PlayerIncome(),
                     common.Income(coins=3))
    self.assertEqual(common.FavorTile.WORKER_POWER_EARTH2.PlayerIncome(),
                     common.Income(workers=1, power=1))
    self.assertEqual(common.FavorTile.POWER4_AIR2.PlayerIncome(),
                     common.Income(power=4))
    self.assertEqual(common.FavorTile.TP3VP_WATER.PlayerIncome(),
                     common.Income())
    self.assertEqual(common.FavorTile.DWELLING2_EARTH.PlayerIncome(),
                     common.Income())
    self.assertEqual(common.FavorTile.TP1234_AIR.PlayerIncome(),
                     common.Income())
    self.assertEqual(common.FavorTile.TOWN_FIRE2.PlayerIncome(),
                     common.Income())
    self.assertEqual(common.FavorTile.CULTACTION_AIR2.PlayerIncome(),
                     common.Income())
    self.assertEqual(common.FavorTile.FIRE3.PlayerIncome(), common.Income())
    self.assertEqual(common.FavorTile.WATER3.PlayerIncome(), common.Income())
    self.assertEqual(common.FavorTile.EARTH3.PlayerIncome(), common.Income())
    self.assertEqual(common.FavorTile.AIR3.PlayerIncome(), common.Income())


class TestResources(unittest.TestCase):
  def testValidation(self):
    self.assertTrue(common.Resources().IsValid())
    self.assertTrue(common.Resources(coins=1).IsValid())
    self.assertFalse(common.Resources(coins=-1).IsValid())

  def testForceValid(self):
    invalidResources = common.Resources(coins=-1)
    self.assertFalse(invalidResources.IsValid())
    invalidResources.ForceValid()
    self.assertTrue(invalidResources.IsValid())


class TestStructureUpgrades(unittest.TestCase):
  def testDwellingUpgrades(self):
    structure = common.Structure.DWELLING
    self.assertFalse(structure.IsUpgradeableTo(common.Structure.DWELLING))
    self.assertTrue(structure.IsUpgradeableTo(common.Structure.TRADING_POST))
    self.assertFalse(structure.IsUpgradeableTo(common.Structure.TEMPLE))
    self.assertFalse(structure.IsUpgradeableTo(common.Structure.STRONGHOLD))
    self.assertFalse(structure.IsUpgradeableTo(common.Structure.SANCTUARY))

  def testTradingPostUpgrades(self):
    structure = common.Structure.DWELLING
    self.assertFalse(structure.IsUpgradeableTo(common.Structure.DWELLING))
    self.assertTrue(structure.IsUpgradeableTo(common.Structure.TRADING_POST))
    self.assertFalse(structure.IsUpgradeableTo(common.Structure.TEMPLE))
    self.assertFalse(structure.IsUpgradeableTo(common.Structure.STRONGHOLD))
    self.assertFalse(structure.IsUpgradeableTo(common.Structure.SANCTUARY))
