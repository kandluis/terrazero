import unittest

from simulation.core import faction


class TestHalflingFaction(unittest.TestCase):
  def testHalfingCreation(self):
    halfing = faction.Halflings()

  def testEngineerCreation(self):
    engineer = faction.Engineers()
