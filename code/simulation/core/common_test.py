import unittest

from simulation.core import common


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


class TestResources(unittest.TestCase):
  def testValidation(self):
    self.assertTrue(common.Resources().IsValid())
    self.assertTrue(common.Resources(power=1).IsValid())
    self.assertFalse(common.Resources(power=-1).IsValid())

  def testForceValid(self):
    invalidResources = common.Resources(power=-1)
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
