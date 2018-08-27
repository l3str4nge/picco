#!/usr/bin/python
import os
import argparse
import sys
import logging

from validators import CommandArgsValidator
from application import Application

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Test')
    parser.add_argument('--in', help='Path for the INPUT files')
    parser.add_argument('--out', help='Path for the OUTPUT files')
    parser.add_argument('--name', help='Folder name to create in --out')
    args = parser.parse_args()


    logger.info('Checking arguments...')
    if not CommandArgsValidator(**args.__dict__).check():
        return False

    logger.info('Start application')
    Application(**args.__dict__).run()

if __name__ == '__main__':
    main()
