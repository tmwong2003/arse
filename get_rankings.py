#!/usr/bin/env python
'''
Created on Sep 11, 2017

@author: twong
'''

from __future__ import print_function

import argparse
import arse
import logging

_logger = logging.getLogger(__name__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    arse.add_general_args(parser)
    args = parser.parse_args()

    logging.basicConfig(level=args.debug_level)

    positions = args.position
    if positions is None:
        positions = arse.PLAYER_POSITIONS
    rankings = arse.get_rankings(positions=positions)
    for p in positions:
        print(rankings[p].position)
        print(rankings[p])
