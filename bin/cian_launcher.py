import argparse
import logging
import os
import sys

os.path.dirname(os.path.abspath(__file__))
from cian_flats import run


def _run_command(command):
    if command == 'download':
        run.download_from_web_to_files()
    elif command == 'parse':
        run.parse_and_save_to_excel()
    elif command == 'download_and_parse':
        run.download_from_web_to_files()
        run.parse_and_save_to_excel()
    elif command == 'reload_errors':
        run.parse_and_save_to_excel()


def parse_and_run_command(args):
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("command", choices=['download', 'parse', 'download_and_parse'],
                        help='download: just download web pages to compute;\n'
                             'parse: parsing and saving info to xls from local files;\n'
                             'download_and_parse: download+parse'
                        )
    args = parser.parse_args(args)
    command = args.command
    _run_command(command)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(funcName)-30s %(levelname)-8s %(message)s')
    try:
        parse_and_run_command(sys.argv[1:])
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.critical('SOS!! EXECUTION STOPPED', exc_info=True)
