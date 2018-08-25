#!/usr/bin/python
import os
import argparse
import sys


class CommandArgsValidator:
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs

    def check(self):
        for key, value in self.kwargs.items():
            if not value:
                sys.stdout.write(f'--{key} is not defined! Try again.\n')

def main():
    parser = argparse.ArgumentParser(description='Test')
    parser.add_argument('--in', help='Path for the INPUT files')
    parser.add_argument('--out', help='Path for the OUTPUT files')
    parser.add_argument('--name', help='Folder name to create in --out')
    args = parser.parse_args()
    CommandArgsValidator(**args.__dict__).check()

if __name__ == '__main__':
    main()
