#!/usr/bin/python
import os
import argparse
import sys
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class BaseValidator(ABC):
    def __init__(self, param):
        self.param = param

    @abstractmethod
    def is_valid(self):
        pass

class DateRangeValidator(BaseValidator):
    def is_valid(self):
        date_range = self.param

        if not date_range:
            logger.info('Date range is not defined, all files will be cloned...\n')
            return True

        date_format = '%Y%m%d%H%M'
        splitted = date_range.split('-')

        if len(splitted) != 2:
            sys.stdout.write('daterange is not correctly\n')
            logger.info('Date range is not specified correctly\n')
            return False

        date_start = datetime.strptime(splitted[0], date_format)
        date_end = datetime.strptime(splitted[1], date_format)

        if date_start > date_end:
            logger.info('Date end cannot be bigger than date start\n')
            return False

        return True

class PathValidator(BaseValidator):
    def is_valid(self):
        self.dir_path = self.param
        return self.path_exist()

    def path_exist(self):
        if not self.dir_path:
             sys.stdout.write(f'Path cannot be empty\n')
             return False

        if not os.path.exists(os.path.join(self.dir_path)):
             sys.stdout.write(f'Directory {self.dir_path} does not exists.\n')
             return False

        return True

class NameValidator(BaseValidator):
    def is_valid(self):
        self.name = self.param
        if not self.name:
            sys.stdout.write('Name is not defined, please try again...\n')
            return False

        return True

class CommandArgsValidator:
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        self.validators = [
                PathValidator(self.kwargs['in']),
                PathValidator(self.kwargs['out']),
                NameValidator(self.kwargs['name']),
                DateRangeValidator(self.kwargs['date']),
        ]

    def check(self):
        for validator in self.validators:
            if not validator.is_valid():
                return False



        """
        for key, value in self.kwargs.items():
            if not value:
                sys.stdout.write(f'--{key} is not defined! Try again.\n')
                return False

        if not self.path_exist(self.kwargs['in']):
            return False

        if not self.path_exist(self.kwargs['out']):
            return False

        if not DateRangeValidator(self.kwargs).is_valid():
            return False
        """

        logger.info('Arguments are valid!')
        return True

    def path_exist(self, dir_path):
        if not os.path.exists(os.path.join(dir_path)):
            sys.stdout.write(f'Directory {dir_path} does not exists.\n')
            return False

        return True


