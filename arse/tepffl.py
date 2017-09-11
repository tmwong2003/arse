#!/usr/bin/env python
'''
Created on Sep 10, 2017

@author: twong
'''

from __future__ import print_function

import argparse
import json
import logging
import pandas as pd
import random
import requests

_logger = logging.getLogger(__name__)


def _deserialize_roster_json(roster_json):
    roster_cooked = json.loads(roster_json)
    try:
        players_json = roster_cooked['d'][0]
    except KeyError:
        raise RuntimeError('Failed to find data key \'d\': Invalid roster JSON?')
    except IndexError:
        raise RuntimeError('Failed to find player JSON string: Invalid roster JSON or new format?')
    players_table = json.loads(players_json)
    if 'rows' not in players_table.keys():
        raise RuntimeError('Failed to find \'rows\' in the player table: Invalid roster JSON or new format?')
    if 'cols' not in players_table.keys():
        raise RuntimeError('Failed to find \'cols\' in the player table: Invalid roster JSON or new format?')
    players_table_rows = [[field['v'] for field in p['c']] for p in players_table['rows']]
    players_table_cols = [c['id'] for c in players_table['cols']]
    return pd.DataFrame(data=players_table_rows, columns=players_table_cols)


class Team(object):

    TEPFFL_TEAM_IDS = range(1517, 1529)
    TEPFFL_POSITIONS = ['QB', 'RB', 'WR', 'OL', 'DST', 'K']
    TEPFFL_ROSTER_SIZE_MAX = 19

    _ROSTER_URL_TEMPLATE = ''

    _ROSTER_COLUMNS = ['FullName', 'NflAbbreviation', 'PosShortName']

    def __init__(self, team_id, filename=None):
        self.team_id = team_id

        roster_json = None
        if filename is None:
            roster_url = self._ROSTER_URL_TEMPLATE.format(int(random.uniform(0, 65536)), self.team_id)
            response = requests.get(roster_url)
            if response.status_code == 200:
                roster_json = response.text
            else:
                raise RuntimeError('Failed to get roster from server: Got response code {}'.format(response.status_code))
        else:
            with open(filename) as f:
                roster_json = f.read()
        self._roster_df = _deserialize_roster_json(roster_json)
        for c in self._ROSTER_COLUMNS:
            if c not in self.df:
                raise RuntimeError('Failed to find \'{}\' in the roster data'.format(c))

    @property
    def df(self):
        return self._roster_df

    @property
    def roster(self):
        return self.df[['FullName', 'NflAbbreviation', 'PosShortName']]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--team-id',
        nargs='*',
        default=Team.TEPFFL_TEAM_IDS,
        type=int,
        choices=Team.TEPFFL_TEAM_IDS,
        help='Zero or more team IDs for which to retrieve rosters (default is to retrieve all rosters)',
    )
    parser.add_argument(
        '--position',
        '-p',
        default=None,
        choices=Team.TEPFFL_POSITIONS,
        help='Show only players in the named position (default is to show all)',
    )
    parser.add_argument(
        '--debug-level',
        default=logging.INFO,
        help='The debug level (default {})'.format(logging.getLevelName(logging.INFO)),
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.debug_level)

    for team_id in args.team_id:
        _logger.info('Gathering roster for team {}'.format(team_id))
        r = Team(team_id)
        if args.position is not None:
            print(r.roster[r.df.PosShortName == args.position])
        else:
            print(r.roster)
