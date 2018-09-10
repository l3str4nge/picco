#!/usr/bin/python
import os
import argparse
import sys
import logging

from validators import CommandArgsValidator
from application import Application

logger = logging.getLogger(__name__)

DESCRIPTION = """

    Here will be more detailed picco description with more information,
    for no it's for testing :)

"""

def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--in', help='Path for the INPUT files')
    parser.add_argument('--out', help='Path for the OUTPUT files')
    parser.add_argument('--date', help='Date when files where made')
    parser.add_argument('--name', help='Folder name to create in --out')
    parser.add_argument('--file', help='Put .txt file with multiple --in, --out, --name etc.')
    parser.add_argument('--zip', help='Type "yes" if you want to compress your data')
    parser.add_argument('--upload', help='Put login and pswd here for upload, note: zip must be True')
    args = parser.parse_args()

    logger.info('Checking arguments...')
    if not CommandArgsValidator(**args.__dict__).check():
        return False

    logger.info('Start application')
    Application(**args.__dict__).run()

if __name__ == '__main__':
    main()
