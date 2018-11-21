import enum


@enum.unique
class Terrain(enum.Enum):
  PLAIN = enum.auto()  # Brown
  SWAMP = enum.auto()  # Black
  LAKE = enum.auto()  # Blue
  FOREST = enum.auto()  # Green
  MOUNTAIN = enum.auto()  # Grey
  WASTELAND = enum.auto()  # Red
  DESERT = enum.auto()  # Yellow
  WATER = enum.auto()  # BLUE WATER, unbuildable


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


@enum.unique
class BonusCards(enum.Enum):
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


@enum.unique
class ScoringTile(enum.Enum):
  """Scoring Tiles apply to each round. They expecify getting additional VP during the
  Action phase, cult bonus awared at the end of round (in Phase III)"""
  TP_AIR4_SPADE = enum.auto()  # 2 VP per TP built, and get a spade per 4 Air.
  # 2 VP per Dwelling built, and 1 priest per 4 Water.
  DWELLING_WATER4_PRIEST = enum.auto()
  # 2 VP per TP built, and get a spade for 4 Water.
  TP_WATER4_SPADE = enum.auto()
  # 5 VP per town built, and get 1 spade per 4 on cult track.
  TOWN_EARTH4_SPADE = enum.auto()
  # 4 VP per stronghold, and get 1 worker per 2 air.
  STRONGHOLD_AIR2_WORKER = enum.auto()
  # 2 VP per spade used, and get 1 coint per 1 earth.
  SPADE_EARTH_COIN = enum.auto()
  # 2 VP per dwelling built, and get 4 power per 4 fire.
  DWELLING_FIRE4_POWER4 = enum.auto()
  # 5 VP per stornghold, and get 1 worker per 2 fire.
  STRONGHOLD_FIRE2_WORKER = enum.auto()


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


@enum.unique
class Building(enum.Enum):
  """The different building types available in TM."""
  DWELLING = enum.auto()
  TRADING_HOUSE = enum.auto()
  SANCTUARY = enum.auto()
  TEMPLE = enum.auto()
  STRONGHOLD = enum.auto()
