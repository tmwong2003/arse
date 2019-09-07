#!/usr/bin/env python
'''
Created on Sep 10, 2017

@author: twong
'''

import argparse
import json
import logging

import arse

from configparser import SafeConfigParser

_logger = logging.getLogger(__name__)

if __name__ == '__main__':
    config = SafeConfigParser()

    parser = argparse.ArgumentParser(add_help=False)
    arse.add_general_args(parser)
    args = parser.parse_args()

    logging.basicConfig(level=args.debug_level)

    config.read(args.config_path)

    # Step 1: Gather all of the TEP FFL active rosters
    arse.Team.configure(config)
    if args.file is not None:
        rosters = arse.load_rosters(args.file)
    else:
        rosters = arse.get_rosters(args.week)

    # Step 2: Get rankings

    rankings = arse.get_rankings(args.position)

    # Step 3: Generate the free-agent rankings
    remap = json.loads(config.get('map', 'map'))

    def fix(name):  # @IgnorePep8
        if name in remap:
            name = str(remap[name])
        return filter(str.isalnum, name).lower()

    print('Week {} free agents'.format(args.week))
    positions = args.position if args.position is not None else arse.PLAYER_POSITIONS
    for position in positions:
        taken = [
            fix(t) for t in rosters[rosters[arse.Team.PLAYER_POSITION] == position][arse.Team.PLAYER_NAME].tolist()
        ]
        print('{} free agents ({} taken, {} ranked)'.format(position, len(taken), len(rankings[position])))
        for player in [p for p in rankings[position] if fix(p[1]) not in taken]:
            print('{}\t{} {}'.format(player[0], player[1], player[2]))
