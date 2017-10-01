from __future__ import print_function

import espn
import fantasypros
import logging

from tepffl import Team, get_rosters, get_team_args, load_rosters

PLAYER_POSITIONS = ['QB', 'RB', 'WR', 'TE', 'OL', 'DST', 'K']


def add_general_args(parser):
    common_parser = parser.add_argument_group('General options')
    common_parser.add_argument(
        '--help', '-h',
        action='help',
        help='Show this help message',
    )
    common_parser.add_argument(
        '--file',
        default=None,
        type=str,
        help='File from which to load league rosters (default is to load from the league server)',
    )
    common_parser.add_argument(
        '--position',
        nargs='*',
        choices=PLAYER_POSITIONS,
        help='Select only players for the named position (default is to select all)',
    )
    common_parser.add_argument(
        '--config-path',
        default='config.ini',
        help='The path to the configuration file',
    )
    common_parser.add_argument(
        '--debug-level',
        default=logging.INFO,
        help='The debug level (default {})'.format(logging.getLevelName(logging.INFO)),
    )


def get_rankings(positions=None):
    if positions is None:
        positions = PLAYER_POSITIONS
    rankings = {}
    for position in positions:
        if position not in PLAYER_POSITIONS:
            raise ValueError('Got an invalid position: Expected {}, got {}'.format(PLAYER_POSITIONS, position))
        if position == 'OL':
            rankings[position] = espn.Ranking(position)
        else:
            rankings[position] = fantasypros.Ranking(position)
    return rankings
