import unittest

from simulation.core import faction

class TestHalflingFaction(unittest.TestCase):
  def testCreation(self):
    halfing = faction.Halflings()