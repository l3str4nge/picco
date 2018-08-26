#!/usr/bin/python
import os
import argparse
import sys
from validators import CommandArgsValidator

def main():
    parser = argparse.ArgumentParser(description='Test')
    parser.add_argument('--in', help='Path for the INPUT files')
    parser.add_argument('--out', help='Path for the OUTPUT files')
    parser.add_argument('--name', help='Folder name to create in --out')
    args = parser.parse_args()
    CommandArgsValidator(**args.__dict__).check()

if __name__ == '__main__':
    main()
