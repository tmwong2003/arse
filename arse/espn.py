'''
Created on Sep 11, 2017

@author: twong
'''

import logging

import requests
from lxml import html

_logger = logging.getLogger(__name__)


class Ranking(object):
    _URL = 'https://www.espn.com/nfl/stats/team/_/season/2018/seasontype/2'

    _TEAM_NAME_MAP = {
        'Arizona': 'Arizona Cardinals',
        'Atlanta': 'Atlanta Falcons',
        'Baltimore': 'Baltimore Ravens',
        'Buffalo': 'Buffalo Bills',
        'Carolina': 'Carolina Panthers',
        'Chicago': 'Chicago Bears',
        'Cincinnati': 'Cincinnati Bengals',
        'Cleveland': 'Cleveland Browns',
        'Dallas': 'Dallas Cowboys',
        'Denver': 'Denver Broncos',
        'Detroit': 'Detroit Lions',
        'Green Bay': 'Green Bay Packers',
        'Houston': 'Houston Texans',
        'Indianapolis': 'Indianapolis Colts',
        'Jacksonville': 'Jacksonville Jaguars',
        'Kansas City': 'Kansas City Chiefs',
        'LA Chargers': 'Los Angeles Chargers',
        'LA Rams': 'Los Angeles Rams',
        'Miami': 'Miami Dolphins',
        'Minnesota': 'Minnesota Vikings',
        'New Orleans': 'New Orleans Saints',
        'NY Giants': 'New York Giants',
        'NY Jets': 'New York Jets',
        'New England': 'New England Patriots',
        'Oakland': 'Oakland Raiders',
        'Philadelphia': 'Philadelphia Eagles',
        'Pittsburgh': 'Pittsburgh Steelers',
        'San Francisco': 'San Francisco 49ers',
        'Seattle': 'Seattle Seahawks',
        'Tampa Bay': 'Tampa Bay Buccaneers',
        'Tennessee': 'Tennessee Titans',
        'Washington': 'Washington Redskins',
    }

    def __init__(self, position):
        if position != 'OL':
            raise RuntimeError('Failed to get rankings: Possibly bad position {}?'.format(position))
        self._position = position
        _logger.debug('Getting rankings from {}'.format(self._URL))
        response = requests.get(self._URL)
        if response.status_code == 200:
            self._xpath_tree = html.fromstring(response.content)
        else:
            raise RuntimeError(f'Failed to get rankings from server: Got response code {response.status_code}')
        self._players = []
        rank = 1
        for rank in range(1, 33):
            player = self.xpath_tree.xpath(
                f'//*[@id="fittPageContainer"]/div[3]/div[1]/div/article/div/section/table/tbody/tr/td[1]/div/table/tbody/tr[{rank}]'
            )[0].text_content()
            self._players.append((rank, player, ''))

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
