"""Add application.properties to Application's S3 Bucket directory."""
import logging
import argparse
from .create_archaius import init_properties

LOG = logging.getLogger(__name__)


def main():
    """Create application.properties for a given application."""
    logging.basicConfig()
    parser = argparse.ArgumentParser(description=main.__doc__)

    parser.add_argument('-d',
                        '--debug',
                        action='store_const',
                        const=logging.DEBUG,
                        default=logging.INFO,
                        help='Set DEBUG output')
    parser.add_argument('-e',
                        '--env',
                        choices=('dev', 'stage', 'prod'),
                        default='dev',
                        help='Deploy environment')
    parser.add_argument('-g',
                        '--group',
                        default='extra',
                        help='Application Group name, e.g. forrest')
    parser.add_argument('-a',
                        '--app',
                        default='unnecessary',
                        help='Application name, e.g. forrestcore')
    args = parser.parse_args()

    LOG.setLevel(args.debug)
    logging.getLogger(__package__).setLevel(args.debug)
    vars(args).pop('debug')

    LOG.debug('Args: %s', vars(args))

    init_properties(env=args.env, group=args.group, app=args.app)


if __name__ == '__main__':
    main()