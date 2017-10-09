#!/usr/bin/env python
'''
Created on Sep 11, 2017

@author: twong
'''

from __future__ import print_function

import argparse
import arse
import logging

from ConfigParser import SafeConfigParser

_logger = logging.getLogger(__name__)


if __name__ == '__main__':
    config = SafeConfigParser()

    parser = argparse.ArgumentParser(add_help=False)
    arse.get_tepffl_args(parser)
    arse.add_general_args(parser)
    parser.add_argument(
        '--to-file',
        type=str,
        default=None,
        help='File to which to save rosters (default is to dump to stdout)',
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.debug_level)

    config.read(args.config_path)

    arse.Team.configure(config)
    rosters = arse.get_rosters(args.week, team_ids=args.team_id)
    if args.to_file is not None:
        print("Saving to file {}...".format(args.to_file))
        rosters.to_csv(args.to_file, index=False)
    else:
        print(rosters)
