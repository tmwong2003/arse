#!/usr/bin/env python
'''
Created on Sep 10, 2017

@author: twong
'''

from __future__ import print_function

import argparse
import logging
import pandas as pd

from arse import Team

_logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--position',
        '-p',
        default=None,
        choices=Team.TEPFFL_POSITIONS,
        help='Select only players for the named position (default is to select all)',
    )
    parser.add_argument(
        '--debug-level',
        default=logging.INFO,
        help='The debug level (default {})'.format(logging.getLevelName(logging.INFO)),
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.debug_level)

    # Step 1: Gather all of the TEP FFL active rosters
    teams = []
    for team_id in Team.TEPFFL_TEAM_IDS:
        _logger.info('Gathering roster for team {}'.format(team_id))
        team = Team(team_id)
        if len(team.roster) < Team.TEPFFL_ROSTER_SIZE_MAX:
            _logger.warning('TEP FFL team with ID {} has a short roster: Expected {}, got {}'.format(team_id, Team.TEPFFL_ROSTER_SIZE_MAX, len(team.roster)))
        if len(team.roster) > Team.TEPFFL_ROSTER_SIZE_MAX:
            _logger.error('TEP FFL team with ID {} has an oversize roster: Expected {}, got {}'.format(team_id, Team.TEPFFL_ROSTER_SIZE_MAX, len(team.roster)))
        teams.append(team)
    df = pd.concat([t.roster for t in teams], ignore_index=True)

    # Step 3: Get ranked offensive lines

    if args.position is not None:
        print(df[df.PosShortName == args.position])
    else:
        print(df)
