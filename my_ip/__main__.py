#!/usr/bin/env python3

__doc__ = 'My IP server on TCP'

import argparse
import logging

from my_ip.tcp_server import start_server

_logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--host',
        type=str,
        default='localhost',
        help='Listening host (default: %(default)s)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=0,
        help='Listening port; 0 means random (default: %(default)s)'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        help='Increase verbosity (max verbosity: -vv)'
    )

    args = parser.parse_args()

    if args.verbose is None:
        args.verbose = 0
    elif args.verbose > 2:
        args.verbose = 2

    return args


def main():
    args = parse_arguments()
    logging.basicConfig(
        level=[logging.WARNING, logging.INFO, logging.DEBUG][args.verbose],
        format='%(asctime)s{} %(message)s'.format(
            '' if args.verbose < 2 else ' %(name)-20s %(threadName)-30s %(levelname)-7s'
        ),
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    start_server(args.host, args.port)


if __name__ == '__main__':
    main()
