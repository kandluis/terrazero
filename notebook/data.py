#!/usr/bin/env python
# coding: utf-8

import argparse
import datetime
import json
import os
import pickle
import requests

from concurrent import futures
from dateutil import relativedelta
from urllib import request
from urllib import error

from typing import Callable, Dict, List, Optional, Text, Tuple


_END_OF_SAMPLE_TOKEN = '\n<|endoftext|>\n'
_WORKER_COUNT = 100


class Game:
  """An in-memory representation of a TM game.

  Properties:
    game_id: The game id assigned to this game by terra.snellman.net
    player_count: The number of players who started this game.
    total_vp: The sum of all player's VP.
  """

  def __init__(self, json) -> None:
    if len(json) == 1:
      self.game_id = json['game']
      self.player_count = 0
      self.total_vp = 0
    else:
      self.game_id = json['game']
      self.player_count = json['player_count']
      self.total_vp = json['events']['faction']['all']['vp']['round']['all']

  def averageVPPerPlayer(self) -> float:
    """Returns the average VP earned by each player in this game. """
    return self.total_vp / self.player_count

  def __str__(self) -> str:
    """Returns a string representation of a Game."""
    return """
        Game: %s
        Players: %s
        Total VP: %s
        """ % (self.game_id, self.player_count, self.total_vp)

  def __repr__(self) -> str:
    return self.__str__()


def fetchAllSummaryData(minDate: datetime.datetime,
                        maxDate: datetime.datetime,
                        keepPredicate: Callable[[Game], bool],
                        local: bool = False,
                        maxGames: Optional[int] = None) -> List[Game]:
  """Fetches the Games based on summary data.

    Args:
        minDate: The smallest date from which to fetch games
          (only the month matters)
        maxDate: The largest date from which to fetch games
          (only the month matters)
        keepPredicate: A callable. For memory efficiency, we can push down
          filtering on game using this function. If this function returns true,
          the Game is kept. Otherwise it is immediately discared.
        maxGames: The maximum number of games to return. Games are retrieved
          from latest to oldest, date wise.

    Returns:
        A list of Game objects fetched from Terra Snellman.
  """
  BASE_URL = "https://terra.snellman.net/data/events"
  results: List[Game] = []
  while minDate < maxDate and (not maxGames or len(results) < maxGames):
    filename = "snellman/summary-%s.pkl" % (maxDate.strftime("%Y-%m"))
    address = "{}/{}.json".format(BASE_URL, maxDate.strftime("%Y-%m"))
    data = None
    if not local:
      try:
        with request.urlopen(address) as site:
          data = json.loads(site.read().decode())
      except error.URLError:
        print("Cannot download data for data %s" % (maxDate.strftime("%Y-%m")))
        maxDate -= relativedelta.relativedelta(months=1)
        continue
      with open("snellman/summary-%s.pkl" % (maxDate.strftime("%Y-%m")),
                'wb') as f:
        pickle.dump(data, f)
    else:
      try:
        with open(filename, 'rb') as f:
          data = pickle.load(f)
      except FileNotFoundError:
        print("Could not unpickle from filename %s" % (filename))
        maxDate -= relativedelta.relativedelta(months=1)
        continue

    for obj in data:
      game = Game(obj)
      if keepPredicate(game):
        results.append(game)
    del data
    maxDate -= relativedelta.relativedelta(months=1)
    print("Collected %s games from %s." % (len(results),
                                           address if not local else filename))
  return results


def keepHighScoringGames(game: Game) -> bool:
  """Filter function that keeps only high scoring games."""
  return game.averageVPPerPlayer() > 120


def downloadLogForGame(game: Game) -> Text:
  """Downloads the entire log (text) for the given game.

  Args:
    game: The game for which the playlog will be downloaded.

  Returns:
    A string consisting of all commands in the game log (seperated by ".").
  """
  kBaseUrl = "https://terra.snellman.net/app/view-game/"
  res = requests.post(kBaseUrl, data={'game': game.game_id})
  data = json.loads(res.content)
  commands = [
      command.get('commands', '').split(".") or command.get('comment', '')
      for command in data['ledger']
      if 'commands' in command or 'comment' in command
  ]
  gameLog = ". ".join(
      item.strip().lower() for sublist in commands for item in sublist)
  return gameLog


def parseShardedFilename(filename: Text) -> Tuple[int, int]:
  """Parses a sharded filename

  Args:
    filename: Must be in the format
      /path/to/file-{shardNumber}-of-{totalShards}.suffix

  Returns:
    A tuple of (shardNumber, totalShards)
  """
  prefix: Text = filename.split(".")[0]
  parts: List[Text] = prefix.split("-")
  totalShards = int(parts[-1])
  shardNumber = int(parts[-3])
  return (shardNumber, totalShards)


def loadGameLedgesFromDisk() -> List[Text]:
  """Loads the game ledges which have already been downloaded from disk.

  Returns:
    A list of game ledges read from the given location.
  """
  for (dirpath, dirnames, filenames) in os.walk("snellman"):
    maxFileInFileSet: Dict[int, Text] = {}
    for filename in filenames:
      if not filename.startswith("sentences-"):
        continue
      nShard, totalShards = parseShardedFilename(filename)
      if totalShards in maxFileInFileSet:
        nPrevShards, _ = parseShardedFilename(maxFileInFileSet[totalShards])
        if nPrevShards < nShard:
          maxFileInFileSet[totalShards] = filename
      else:
        maxFileInFileSet[totalShards] = filename
    if not maxFileInFileSet:
      print("No sentences to load...")
      return []
    filenameToLoad: Text = maxFileInFileSet[max(maxFileInFileSet.keys())]
    print("Reading from file: %s" % filenameToLoad)
    with open(os.path.join(dirpath, filenameToLoad), 'rb') as f:
      sentences = pickle.load(f)
    print("Loaded %s games" % len(sentences))
    return sentences
  else:
    print("No sentences to load...")
    return []


def fetchAllGameLogs(detailsLocal: bool = False,
                     summaryLocal: bool = False,
                     saveEvery: int = 1000,
                     maxGames: int = 20000) -> Text:
  """Downloads game data and dumps to disk.

  Args:
    detailsLocal: If true, game data is loaded only from the disk data.
    summaryLocal: If true, summary data is loaded only from disk.
    saveEvery: Specifies approximately how many games to process before storing
        a checkpoint on disk.
    maxGames: The approximate number of maximum games to download.

  Returns:
    A single string containing all loaded game logs.
  """
  def downloadGameWrapper(info: Tuple[int, Game]) -> Text:
    i, game = info
    print("Downloading game %s: %s" % (i, game.game_id))
    return downloadLogForGame(game)

  OLDEST_DATE = datetime.datetime(year=2013, month=1, day=15)
  NEWEST_DATE = datetime.datetime.now()
  data: List[Game] = fetchAllSummaryData(
      OLDEST_DATE,
      NEWEST_DATE,
      keepPredicate=keepHighScoringGames,
      maxGames=maxGames,
      local=summaryLocal)
  sentences: List[Text] = loadGameLedgesFromDisk()
  if not detailsLocal:
    try:
      # Try to continue where we left off. Assume user "did the right thing"
      # and is using the same "data" to load the games.
      # Migrate to a set of ids eventually.
      processedSinceLastSave = 0
      for i in range(len(sentences), len(data), _WORKER_COUNT):
        with futures.ThreadPoolExecutor(max_workers=_WORKER_COUNT) as executor:
          inp = [(k, data[k])
                 for k in range(i, min(i + _WORKER_COUNT, len(data)))]
          concurrent_sentences = executor.map(downloadGameWrapper, inp)
        sentences.extend(concurrent_sentences)
        processedSinceLastSave += _WORKER_COUNT
        if processedSinceLastSave >= saveEvery:
          filename: Text = 'snellman/sentences-%s-of-%s.pkl' % (i, len(data))
          print("Saving to %s" % filename)
          with open(filename, 'wb') as f:
            pickle.dump(sentences, f)
          processedSinceLastSave = 0
    finally:
      filename = "snellman/sentences-%s-of-%s.pkl" % (i, len(data))
      print("Dumping to %s " % filename)
      with open(filename, 'wb') as f:
        pickle.dump(sentences, f)
  return _END_OF_SAMPLE_TOKEN.join(sentences)


def setUpParser() -> argparse.ArgumentParser:
  """Setup the parser for command line arguments."""
  parser = argparse.ArgumentParser(description='Download TM game data.')
  parser.add_argument(
      '--saveEvery',
      type=int,
      help='How often to save the details if downloading, or how often they '
      'were saved if already downloaded and loading from disk.',
      default=1000)
  parser.add_argument(
      '--detailsLocal', dest='detailsLocal', action='store_true')
  parser.add_argument(
      '--no-detailsLocal', dest='detailsLocal', action='store_false')
  parser.set_defaults(feature=True)

  parser.add_argument(
      '--summaryLocal', dest='summaryLocal', action='store_true')
  parser.add_argument(
      '--no-summaryLocal', dest='summaryLocal', action='store_false')
  parser.add_argument(
      '--maxGames',
      type=int,
      help='Maximum number of games to download',
      default=int(20e3))
  parser.add_argument(
      '--game', type=str,
      help='If set, downloads and prings the game log for this game',
      default=None)
  parser.set_defaults(feature=True)
  return parser


if __name__ == '__main__':
  parser = setUpParser()
  args = parser.parse_args()
  if not args.game:
    text = fetchAllGameLogs(
        detailsLocal=args.detailsLocal,
        summaryLocal=args.summaryLocal,
        saveEvery=args.saveEvery,
        maxGames=args.maxGames)
    with open("snellman/games.input", "w") as f:
      f.write(text)
  else:
    print(downloadLogForGame(Game({
        'game': args.game
    }))[-1024:])
