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
                return False

        if not self.path_exist(self.kwargs['in']):
            return False

        if not self.path_exist(self.kwargs['out']):
            return False

        return True

    def path_exist(self, dir_path):
        if not os.path.exists(os.path.join(dir_path)):
            sys.stdout.write(f'{dir_path } does not exists.\n')
            return False

        return True

