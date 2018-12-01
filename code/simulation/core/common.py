import enum

from typing import Any, NamedTuple, TypeVar

from simulation import utils


class Resources:
  def __init__(self: 'Resources',
               coins: int = 0,
               workers: int = 0,
               bridges: int = 0,
               priests: int = 0) -> None:
    self.coins: int = coins
    self.workers: int = workers
    self.bridges: int = bridges
    self.priests: int = priests

  def IsValid(self: 'Resources') -> int:
    return not (self.coins < 0 or self.workers < 0 or self.bridges < 0
                or self.priests < 0)

  def ForceValid(self: 'Resources') -> None:
    self.coins = max(0, self.coins)
    self.workers = max(0, self.workers)
    self.bridges = max(0, self.bridges)
    self.priests = max(0, self.priests)

  def __eq__(self: 'Resources', other: Any) -> bool:
    return (isinstance(other, Resources) and self.coins == other.coins
            and self.workers == other.workers and self.priests == other.priests
            and self.bridges == other.bridges)

  def __add__(self: 'Resources', other: 'Resources') -> 'Resources':
    return Resources(
        coins=self.coins + other.coins,
        workers=self.workers + other.workers,
        bridges=self.bridges + other.bridges,
        priests=self.priests + other.priests)

  def __radd__(self: 'Resources', other: 'Resources') -> 'Resources':
    if other == 0: return self
    return self.__add__(other)

  def __iadd__(self: 'Resources', other: 'Resources') -> 'Resources':
    self.coins += other.coins
    self.workers += other.workers
    self.bridges += other.bridges
    self.priests += other.priests
    return self

  def __sub__(self: 'Resources', other: 'Resources') -> 'Resources':
    return Resources(
        coins=self.coins - other.coins,
        workers=self.workers - other.workers,
        bridges=self.bridges - other.bridges,
        priests=self.priests - other.priests)

  def __rsub__(self: 'Resources', other: 'Resources') -> 'Resources':
    if other == 0: return self
    return self.__sub__(other)

  def __isub__(self: 'Resources', other: 'Resources') -> 'Resources':
    self.coins -= other.coins
    self.workers -= other.workers
    self.bridges -= other.bridges
    self.priests -= other.priests
    return self

  def __str__(self: 'Resources') -> str:
    return """
    Coins: {coins}     Workers: {workers}   Priests: {priests}   Bridges: {bridges}
    """.format(
        coins=self.coins,
        workers=self.workers,
        priests=self.priests,
        bridges=self.bridges)


class Income:
  def __init__(self: 'Income', power: int = 0, **kwargs):
    self.resources = Resources(**kwargs)
    self.power = power

  def IsValid(self: 'Income') -> int:
    raise utils.InternalError("Income should not be used this way!")

  def ForceValid(self: 'Income') -> None:
    raise utils.InternalError("Income should not be used this way!")

  def __eq__(self, other: Any) -> bool:
    return (isinstance(other, Income) and self.resources == other.resources
            and self.power == other.power)

  def __add__(self: 'Income', other: 'Income') -> 'Income':
    newIncome = Income()
    newIncome.resources = self.resources + other.resources
    newIncome.power = self.power + other.power
    return newIncome

  def __radd__(self: 'Income', other: 'Income') -> 'Income':
    if other == 0: return self
    return self.__add__(other)

  def __iadd__(self: 'Income', other: 'Income') -> 'Income':
    self.resources += other.resources
    self.power += other.power
    return self

  def __sub__(self: 'Income', other: 'Income') -> 'Income':
    newIncome = Income()
    newIncome.resources = self.resources - other.resources
    newIncome.power = self.power - other.power
    return newIncome

  def __rsub__(self: 'Income', other: 'Income') -> 'Income':
    if other == 0: return self
    return self.__sub__(other)

  def __isub__(self: 'Income', other: 'Income') -> 'Income':
    self.resources -= other.resources
    self.power -= other.power
    return self

  def __str__(self: 'Income') -> str:
    return """
    {resources}
    Power: {power}
    """.format(
        resources=self.resources, power=self.power)


@enum.unique
class Terrain(enum.Enum):
  PLAIN = enum.auto()
  SWAMP = enum.auto()
  LAKE = enum.auto()
  FOREST = enum.auto()
  MOUNTAIN = enum.auto()
  WASTELAND = enum.auto()
  DESERT = enum.auto()
  WATER = enum.auto()  # BLUE, unbuildable

  def GetColor(self) -> str:
    if self == Terrain.PLAIN:
      return "BROWN"
    if self == Terrain.SWAMP:
      return "BLACK"
    if self == Terrain.LAKE:
      return "BLUE"
    if self == Terrain.FOREST:
      return "GREEN"
    if self == Terrain.MOUNTAIN:
      return "GREY"
    if self == Terrain.WASTELAND:
      return "RED"
    if self == Terrain.DESERT:
      return "YELLOW"
    if self == Terrain.WATER:
      return "BLUE[unbuildable]"
    raise utils.UnimplementedError(
        "Humand description of %s does not exist" % self.name)

  def __str__(self) -> str:
    return "%s (%s)" % (super(Terrain, self).__str__(), self.GetColor())


@enum.unique
class PowerBowl(enum.Enum):
  I = enum.auto()
  II = enum.auto()
  III = enum.auto()


@enum.unique
class CultTrack(enum.Enum):
  """The four possible cult tracks"""
  FIRE = enum.auto()  # Fire track.
  WATER = enum.auto()  # Water track.
  EARTH = enum.auto()  # Earth track.
  AIR = enum.auto()  # Air track.


@enum.unique
class TownKey(enum.Enum):
  """The town keys"""
  WOKERS2 = enum.auto()
  PRIEST = enum.auto()
  CULT = enum.auto()  # 1 up on every cult-track.
  POWER8 = enum.auto()  # 8 power.
  COIN6 = enum.auto()  # 6 coins.

  def _GetHumanDescription(self) -> str:
    if self == TownKey.WOKERS2:
      return "2 immediate workers"
    if self == TownKey.PRIEST:
      return "1 immediate priest"
    if self == TownKey.CULT:
      return "1 up on every cult-track."
    if self == TownKey.POWER8:
      return "8 immediate power."
    if self == TownKey.COIN6:
      return "6 immediate coins."
    raise utils.UnimplementedError(
        "Humand description of %s does not exist" % self.name)

  def __str__(self) -> str:
    return "%s [%s]" % (super(TownKey, self).__str__(),
                        self._GetHumanDescription())


@enum.unique
class BonusCard(enum.Enum):
  """The nine possible bonus cards.  Each one tends to work at each Phase of the game.
  Phase I is income, Phase II is during gameplay, and Phase III is at end of round.
  """
  PRIEST = enum.auto()  # 1 priest income.
  WORKER_3POWER = enum.auto()  # 1 worker income and 3 power income.
  COIN6 = enum.auto()  # 6 coins income.
  # 3 power income and +1 shipping for Phase I and II.
  POWER3_SHIPPING = enum.auto()
  SPADE_COIN2 = enum.auto()  # 1 spade special action + 2 coin income.
  CULT_COIN4 = enum.auto()  # 1 cult track special action + 4 coin income.
  # 1 vp per dwelling in board at end, 2 coin income.
  DWELLING_COIN2 = enum.auto()
  # 2 vp per TP on board at end, 1 worker income.
  TRADING_POST_WORKER = enum.auto()
  STRONGHOLD_WORKER2 = enum.auto()  # 4 vp per SH/TE. 2 worker income.

  def __init__(self, value: int):
    self.coins = 0

  def PlayerIncome(self) -> Income:
    if self == BonusCard.PRIEST:
      return Income(priests=1)
    if self == BonusCard.WORKER_3POWER:
      return Income(workers=1, power=3)
    if self == BonusCard.COIN6:
      return Income(coins=6)
    if self == BonusCard.POWER3_SHIPPING:
      return Income(power=3)
    if self == BonusCard.SPADE_COIN2:
      return Income(coins=2)
    if self == BonusCard.CULT_COIN4:
      return Income(coins=4)
    if self == BonusCard.DWELLING_COIN2:
      return Income(coins=2)
    if self == BonusCard.TRADING_POST_WORKER:
      return Income(workers=1)
    if self == BonusCard.STRONGHOLD_WORKER2:
      return Income(workers=2)

    raise utils.InternalError("FavorTile %s is not implemented!" % self)

  def _GetHumanDescription(self) -> str:
    if self == BonusCard.PRIEST:
      return "1 priest income%s." % ("" if self.coins == 0 else
                                     " <%s coins> " % self.coins)
    if self == BonusCard.WORKER_3POWER:
      return "1 wrker income and 3 power income%s." % (
          "" if self.coins == 0 else " <%s coins> " % self.coins)
    if self == BonusCard.COIN6:
      return "6 coins income%s." % ("" if self.coins == 0 else
                                    " <%s coins> " % self.coins)
    if self == BonusCard.POWER3_SHIPPING:
      return "3 power income and +1 shipping for Phase I and II%s." % (
          "" if self.coins == 0 else " <%s coins> " % self.coins)
    if self == BonusCard.SPADE_COIN2:
      return "1 spade special action and 2 coin income%s." % (
          "" if self.coins == 0 else " <%s coins> " % self.coins)
    if self == BonusCard.CULT_COIN4:
      return "1 cult track special action + 4 coin income%s." % (
          "" if self.coins == 0 else " <%s coins> " % self.coins)
    if self == BonusCard.DWELLING_COIN2:
      return "1 vp per dwelling in board at end, 2 coin income%s." % (
          "" if self.coins == 0 else " <%s coins> " % self.coins)
    if self == BonusCard.TRADING_POST_WORKER:
      return "2 vp per TP on board at end, 1 worker income%s." % (
          "" if self.coins == 0 else " <%s coins> " % self.coins)
    if self == BonusCard.STRONGHOLD_WORKER2:
      return "4 vp per SH/TE. 2 worker income%s." % (
          "" if self.coins == 0 else " <%s coins> " % self.coins)
    raise utils.UnimplementedError(
        "Humand description of %s does not exist" % self.name)

  def __str__(self) -> str:
    return "%s [%s]" % (super(BonusCard, self).__str__(),
                        self._GetHumanDescription())

  def __repr__(self) -> str:
    return self.__str__()


@enum.unique
class ScoringTile(enum.Enum):
  """Scoring Tiles apply to each round. They expecify getting additional VP during the
  Action phase, cult bonus awared at the end of round (in Phase III)"""
  TP_AIR4_SPADE = enum.auto()  # 2 VP per TP built, and get a spade per 4 Air.
  # 2 VP per Dwelling built, and 1 priest per 4 Water.
  DWELLING_WATER4_PRIEST = enum.auto()
  # 2 VP per TP built, and get a spade for 4 Water.
  TP_WATER4_SPADE = enum.auto()
  # 5 VP per town built, and get 1 spade per 4 on earth.
  TOWN_EARTH4_SPADE = enum.auto()
  # 4 VP per stronghold, and get 1 worker per 2 air.
  STRONGHOLD_AIR2_WORKER = enum.auto()
  # 2 VP per spade used, and get 1 coint per 1 earth.
  SPADE_EARTH_COIN = enum.auto()
  # 2 VP per dwelling built, and get 4 power per 4 fire.
  DWELLING_FIRE4_POWER4 = enum.auto()
  # 5 VP per stornghold, and get 1 worker per 2 fire.
  STRONGHOLD_FIRE2_WORKER = enum.auto()

  def _GetHumanDescription(self) -> str:
    if self == ScoringTile.TP_AIR4_SPADE:
      return "Phase II: 2 VP per TP built. Phase III: Get 1 spade per 4 Air."
    if self == ScoringTile.DWELLING_WATER4_PRIEST:
      return "Phase II: 2 VP per Dwelling built. Phase III: Get 1 priest per 4 Water."
    if self == ScoringTile.TP_WATER4_SPADE:
      return "Phase II: 2 VP per TP built. Phase III: Get a spade for 4 Water."
    if self == ScoringTile.TOWN_EARTH4_SPADE:
      return "Phase II: 5 VP per town built. Phase III: Get 1 spade per 4 on Earth."
    if self == ScoringTile.STRONGHOLD_AIR2_WORKER:
      return "Phase II: 4 VP per stronghold. Phase III: Get 1 worker per 2 Air."
    if self == ScoringTile.SPADE_EARTH_COIN:
      return "Phase II: 2 VP per spade used. Phase III: Get 1 coint per 1 Earth."
    if self == ScoringTile.DWELLING_FIRE4_POWER4:
      return "Phase II: 2 VP per dwelling built. Phase III: Get 4 power per 4 Fire."
    if self == ScoringTile.STRONGHOLD_FIRE2_WORKER:
      return "Phase II: 5 VP per stornghold. Phase III: Get 1 worker per 2 Fire."
    raise utils.UnimplementedError(
        "Humand description of %s does not exist" % self.name)

  def __str__(self) -> str:
    return "%s [%s]" % (super(ScoringTile, self).__str__(),
                        self._GetHumanDescription())


@enum.unique
class FavorTile(enum.Enum):
  """You may only have one favor tile of each type. Most of these are just passive income
  and immediate advancement in the cult track. There are also some tiles with special
  abilities"""
  COIN3_FIRE = enum.auto()  # 3 coin income, 1 fire advancement.
  TP3VP_WATER = enum.auto()  # 3 VP per built dwelling, 1 water advancement.
  DWELLING2_EARTH = enum.auto()  # 2 VP per dwelling built, 1 earth.
  # Get 2/3/3/4 VP per 1/2/3/4 TPs when passing. 1 Air.
  TP1234_AIR = enum.auto()
  # Town founding only requires combined power of 6, instead of 7. 2 Fire.
  TOWN_FIRE2 = enum.auto()
  # Special action to use cult track, plus 2 water.
  CULTACTION_AIR2 = enum.auto()
  WORKER_POWER_EARTH2 = enum.auto()  # 1 worker + 1 power income, 2 eart.
  POWER4_AIR2 = enum.auto()  # 4 power income, 2 air.
  FIRE3 = enum.auto()  # 3 fire.
  WATER3 = enum.auto()  # 3 water.
  EARTH3 = enum.auto()  # 3 earth.
  AIR3 = enum.auto()  # 3 air.

  def PlayerIncome(self) -> Income:
    if self == FavorTile.COIN3_FIRE:
      return Income(coins=3)
    if self == FavorTile.WORKER_POWER_EARTH2:
      return Income(workers=1, power=1)
    if self == FavorTile.POWER4_AIR2:
      return Income(power=4)
    if (self == FavorTile.TP3VP_WATER or self == FavorTile.DWELLING2_EARTH
        or self == FavorTile.TP1234_AIR or self == FavorTile.TOWN_FIRE2
        or self == FavorTile.CULTACTION_AIR2 or self == FavorTile.FIRE3
        or self == FavorTile.WATER3 or self == FavorTile.EARTH3
        or self == FavorTile.AIR3):
      return Income()
    raise utils.InternalError("FavorTile %s is not implemented!" % self)

  def _GetHumanDescription(self) -> str:
    if self == FavorTile.COIN3_FIRE:
      return "3 coin income, 1 fire advancement."
    if self == FavorTile.TP3VP_WATER:
      return "3 VP per built dwelling, 1 water advancement."
    if self == FavorTile.DWELLING2_EARTH:
      return "2 VP per dwelling built, 1 earth."
    if self == FavorTile.TP1234_AIR:
      return "Get 2/3/3/4 VP per 1/2/3/4 TPs when passing. 1 Air."
    if self == FavorTile.TOWN_FIRE2:
      return "Town founding only requires combined power of 6, instead of 7. 2 Fire."
    if self == FavorTile.CULTACTION_AIR2:
      return "Special action to use cult track, plus 2 water."
    if self == FavorTile.WORKER_POWER_EARTH2:
      return "1 worker + 1 power income, 2 eart."
    if self == FavorTile.POWER4_AIR2:
      return "4 power income, 2 air."
    if self == FavorTile.FIRE3:
      return "3 fire."
    if self == FavorTile.WATER3:
      return "3 water."
    if self == FavorTile.EARTH3:
      return "3 earth."
    if self == FavorTile.AIR3:
      return "3 air."
    raise utils.UnimplementedError(
        "Humand description of %s does not exist" % self.name)


@enum.unique
class Structure(enum.Enum):
  """The different building types available in TM."""
  DWELLING = enum.auto()
  TRADING_POST = enum.auto()
  SANCTUARY = enum.auto()
  TEMPLE = enum.auto()
  STRONGHOLD = enum.auto()

  def IsUpgradeableTo(self, other: 'Structure') -> bool:
    """Returns true if 'other' is a structure to which we can upgrade"""
    if other == Structure.TRADING_POST:
      return self == Structure.DWELLING
    if other == Structure.TEMPLE or other == Structure.STRONGHOLD:
      return self == Structure.TRADING_POST
    if other == Structure.SANCTUARY:
      return self == Structure.TEMPLE
    if other == Structure.DWELLING:
      return False
    raise utils.InternalError("Invalid structure: %s" % other)
