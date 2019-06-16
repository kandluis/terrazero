import unittest

from simulation.core import common
from simulation.core import faction


class TestHalflingFaction(unittest.TestCase):
  def testHalflingCreation(self) -> None:
    halfling = faction.Halflings()

  def testStartingResources(self) -> None:
    halfling = faction.Halflings()

    self.assertEqual(halfling.HomeTerrain(), common.Terrain.PLAIN)
    self.assertEqual(halfling.StartingPower(), {
        common.PowerBowl.I: 3,
        common.PowerBowl.II: 9,
        common.PowerBowl.III: 0
    })
    self.assertEqual(halfling.StartingResources(),
                     common.Resources(workers=3, coins=15))
    self.assertEqual(
        {
            common.CultTrack.EARTH: 1,
            common.CultTrack.AIR: 1,
            common.CultTrack.WATER: 0,
            common.CultTrack.FIRE: 0
        }, halfling.StartingCultPositions())
    self.assertEqual(halfling.StartingShipping(), 0)

  def testStructureCost(self) -> None:
    halfling = faction.Halflings()

    # Dwelling.
    self.assertEqual(
        halfling.StructureCost(common.Structure.DWELLING,
                               adjacentEnemyStructure=False),
        common.Resources(workers=1, coins=2))
    self.assertEqual(
        halfling.StructureCost(common.Structure.DWELLING,
                               adjacentEnemyStructure=True),
        common.Resources(workers=1, coins=2))

    # Trading post.
    self.assertEqual(
        halfling.StructureCost(common.Structure.TRADING_POST,
                               adjacentEnemyStructure=False),
        common.Resources(workers=2, coins=6))
    self.assertEqual(
        halfling.StructureCost(common.Structure.TRADING_POST,
                               adjacentEnemyStructure=True),
        common.Resources(workers=2, coins=3))

    # Stronghold
    self.assertEqual(
        halfling.StructureCost(common.Structure.STRONGHOLD,
                               adjacentEnemyStructure=False),
        common.Resources(workers=4, coins=8))
    self.assertEqual(
        halfling.StructureCost(common.Structure.STRONGHOLD,
                               adjacentEnemyStructure=True),
        common.Resources(workers=4, coins=8))

    # Temple.
    self.assertEqual(
        halfling.StructureCost(common.Structure.TEMPLE,
                               adjacentEnemyStructure=False),
        common.Resources(workers=2, coins=5))
    self.assertEqual(
        halfling.StructureCost(common.Structure.TEMPLE,
                               adjacentEnemyStructure=True),
        common.Resources(workers=2, coins=5))

    # Sanctuary.
    self.assertEqual(
        halfling.StructureCost(common.Structure.SANCTUARY,
                               adjacentEnemyStructure=False),
        common.Resources(workers=4, coins=6))
    self.assertEqual(
        halfling.StructureCost(common.Structure.SANCTUARY,
                               adjacentEnemyStructure=True),
        common.Resources(workers=4, coins=6))

  def testIncomeForStructures(self) -> None:
    halfling = faction.Halflings()

    # tests SH + SA + DW income.
    self.assertEqual(
        halfling.IncomeForStructures({
            common.Structure.DWELLING: 4,
            common.Structure.STRONGHOLD: 1,
            common.Structure.SANCTUARY: 1
        }), common.Income(workers=(4 + 1), priests=1, power=2))

    # Tests last DW does not give income + TP + TE income
    self.assertEqual(
        halfling.IncomeForStructures({
            common.Structure.DWELLING: 8,
            common.Structure.TRADING_POST: 3,
            common.Structure.TEMPLE: 1
        }), common.Income(workers=8, priests=1, coins=6, power=4))


class TestEngineerFaction(unittest.TestCase):
  def testEngineerCreation(self) -> None:
    engineer = faction.Engineers()

  def testStartingResources(self) -> None:
    engineer = faction.Engineers()

    self.assertEqual(engineer.HomeTerrain(), common.Terrain.MOUNTAIN)
    self.assertEqual(engineer.StartingPower(), {
        common.PowerBowl.I: 3,
        common.PowerBowl.II: 9,
        common.PowerBowl.III: 0
    })
    self.assertEqual(engineer.StartingResources(),
                     common.Resources(workers=2, coins=10))
    self.assertEqual(
        {
            common.CultTrack.AIR: 0,
            common.CultTrack.WATER: 0,
            common.CultTrack.FIRE: 0,
            common.CultTrack.EARTH: 0
        }, engineer.StartingCultPositions())
    self.assertEqual(engineer.StartingShipping(), 0)

  def testStructureCost(self) -> None:
    engineer = faction.Engineers()

    # Dwelling.
    self.assertEqual(
        engineer.StructureCost(common.Structure.DWELLING,
                               adjacentEnemyStructure=False),
        common.Resources(workers=1, coins=1))
    self.assertEqual(
        engineer.StructureCost(common.Structure.DWELLING,
                               adjacentEnemyStructure=True),
        common.Resources(workers=1, coins=1))

    # Trading post.
    self.assertEqual(
        engineer.StructureCost(common.Structure.TRADING_POST,
                               adjacentEnemyStructure=False),
        common.Resources(workers=1, coins=4))
    self.assertEqual(
        engineer.StructureCost(common.Structure.TRADING_POST,
                               adjacentEnemyStructure=True),
        common.Resources(workers=1, coins=2))

    # Stronghold
    self.assertEqual(
        engineer.StructureCost(common.Structure.STRONGHOLD,
                               adjacentEnemyStructure=False),
        common.Resources(workers=3, coins=6))
    self.assertEqual(
        engineer.StructureCost(common.Structure.STRONGHOLD,
                               adjacentEnemyStructure=True),
        common.Resources(workers=3, coins=6))

    # Temple.
    self.assertEqual(
        engineer.StructureCost(common.Structure.TEMPLE,
                               adjacentEnemyStructure=False),
        common.Resources(workers=1, coins=4))
    self.assertEqual(
        engineer.StructureCost(common.Structure.TEMPLE,
                               adjacentEnemyStructure=True),
        common.Resources(workers=1, coins=4))

    # Sanctuary.
    self.assertEqual(
        engineer.StructureCost(common.Structure.SANCTUARY,
                               adjacentEnemyStructure=False),
        common.Resources(workers=3, coins=6))
    self.assertEqual(
        engineer.StructureCost(common.Structure.SANCTUARY,
                               adjacentEnemyStructure=True),
        common.Resources(workers=3, coins=6))

  def testIncomeForStructures(self) -> None:
    engineer = faction.Engineers()

    # tests SH + SA + DW income, with 1 DW incoming missing.
    self.assertEqual(
        engineer.IncomeForStructures({
            common.Structure.DWELLING: 4,
            common.Structure.STRONGHOLD: 1,
            common.Structure.SANCTUARY: 1
        }), common.Income(workers=3, priests=1, power=2))

    # Test TP + TE income, extra power.
    self.assertEqual(
        engineer.IncomeForStructures({
            common.Structure.TRADING_POST: 3,
            common.Structure.TEMPLE: 2
        }), common.Income(priests=1, coins=6, power=9))


class TestFactionModule(unittest.TestCase):
  def testAllFactions(self) -> None:
    # A change detector test when someone tries to add more factions.
    self.assertEqual(len(faction.AllAvailable()), 2)
