'''
Created on Sep 11, 2017

@author: twong
'''

import logging

import requests
from lxml import html

_logger = logging.getLogger(__name__)


class Ranking(object):
    _FANTASYPROS_URL_TEMPLATE = 'https://www.fantasypros.com/nfl/start/{}.php'

    def __init__(self, position):
        self._position = position
        ranking_url = self._FANTASYPROS_URL_TEMPLATE.format(position.lower())
        _logger.debug('Getting rankings from {}'.format(ranking_url))
        response = requests.get(ranking_url)
        if response.status_code == 200:
            self._xpath_tree = html.fromstring(response.content)
        else:
            raise RuntimeError(
                f'Failed to get rankings from server: Got response code {response.status_code}: Possibly bad position {position}?'
            )
        self._players = []
        rank = 1
        for player in self.xpath_tree.xpath('//div[@class="player-select"]'):
            name = player.xpath('a/@title')[0]
            team = player.xpath('*[@class="player-team"]/text()')
            _logger.debug('Processing player {}'.format(name))
            self._players.append((rank, name, '' if len(team) <= 0 else team[0]))
            rank += 1

    @property
    def position(self):
        return self._position

    @property
    def xpath_tree(self):
        return self._xpath_tree

    def __repr__(self):
        return str(self._players)

    def __len__(self):
        return len(self._players)

    def __getitem__(self, key):
        return self._players[key]
