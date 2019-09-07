'''
Created on Sep 10, 2017

@author: twong
'''

import json
import logging
import random

import pandas as pd
import requests

_logger = logging.getLogger(__name__)


def _deserialize_roster_json(roster_json):
    roster_cooked = json.loads(roster_json)
    try:
        players_json = roster_cooked['d'][0]
    except KeyError:
        raise RuntimeError("Failed to find data key 'd': Invalid roster JSON?")
    except IndexError:
        raise RuntimeError('Failed to find player JSON string: Invalid roster JSON or new format?')
    players_table = json.loads(players_json)
    if 'rows' not in players_table.keys():
        raise RuntimeError("Failed to find 'rows' in the player table: Invalid roster JSON or new format?")
    if 'cols' not in players_table.keys():
        raise RuntimeError("Failed to find 'cols' in the player table: Invalid roster JSON or new format?")
    players_table_rows = [[field['v'] for field in pos['c']] for pos in players_table['rows']]
    players_table_cols = [c['id'] for c in players_table['cols']]
    return pd.DataFrame(data=players_table_rows, columns=players_table_cols)


class Team(object):

    PLAYER_NAME = 'FullName'
    PLAYER_POSITION = 'PosShortName'

    TEPFFL_TEAM_IDS = range(1517, 1529)
    TEPFFL_ROSTER_SIZE_MAX = 19

    _ROSTER_URL = None
    _ROSTER_QUERY_TEMPLATE = '{}?rnd={}&seasonId={}&weekNumber={}&teamId={}'
    _ROSTER_SEASON = None
    _ROSTER_COLUMNS = [PLAYER_NAME, 'NflAbbreviation', PLAYER_POSITION]

    @classmethod
    def configure(cls, config):
        cls._ROSTER_URL = config.get('tepffl', 'url')
        cls._ROSTER_SEASON = config.get('tepffl', 'season')

    def __init__(self, team_id, week, filename=None):
        if self._ROSTER_URL is None:
            raise RuntimeError('Failed to set TEP FFL roster URL')
        if self._ROSTER_SEASON is None:
            raise RuntimeError('Failed to set TEP FFL season ID')
        self.team_id = team_id
        roster_json = None
        if filename is None:
            roster_url = self._ROSTER_QUERY_TEMPLATE.format(
                self._ROSTER_URL, int(random.uniform(0, 65536)), self._ROSTER_SEASON, week, self.team_id
            )
            _logger.debug('Getting roster from {}'.format(roster_url))
            response = requests.get(roster_url)
            if response.status_code == 200:
                roster_json = response.text
            else:
                raise RuntimeError(
                    f'Failed to get roster from server: Got response code {response.status_code})'
                )
        else:
            with open(filename) as f:
                roster_json = f.read()
        self._roster_df = _deserialize_roster_json(roster_json)
        for c in self._ROSTER_COLUMNS:
            if c not in self.df:
                raise RuntimeError(f"Failed to find '{c}' in the roster data")

    @property
    def df(self):
        return self._roster_df

    @property
    def roster(self):
        return self.df[['FullName', 'NflAbbreviation', 'PosShortName']]


def get_tepffl_args(parser):
    team_parser = parser.add_argument_group('Team options')
    team_parser.add_argument(
        '--team-id',
        nargs='*',
        type=int,
        choices=Team.TEPFFL_TEAM_IDS,
        help='Zero or more team IDs for which to retrieve rosters (default is to retrieve all rosters)',
    )


def get_rosters(week, team_ids=None):
    if team_ids is None:
        team_ids = Team.TEPFFL_TEAM_IDS
    teams = []
    for team_id in team_ids:
        _logger.debug('Gathering roster for team {}'.format(team_id))
        team = Team(team_id, week)
        if len(team.roster) < Team.TEPFFL_ROSTER_SIZE_MAX:
            _logger.warning(
                f'TEP FFL team with ID {team_id} has a short roster: Expected {Team.TEPFFL_ROSTER_SIZE_MAX}, got {len(team.roster)}'
            )
        if len(team.roster) > Team.TEPFFL_ROSTER_SIZE_MAX:
            _logger.error(
                f'TEP FFL team with ID {team_id} has an oversize roster: Expected {Team.TEPFFL_ROSTER_SIZE_MAX}, got {len(team.roster)}'
            )
        teams.append(team)
    return pd.concat([t.roster for t in teams], ignore_index=True)


def load_rosters(file):
    return pd.read_csv(file)
