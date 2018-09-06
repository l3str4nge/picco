import os
from unittest import TestCase
from src.validators import *

class TestDateRangeValidator(TestCase):
    def test_date_range_validator(self):
        # everything is OK
        test_date_range = '201702021010-201702021212'
        validator = DateRangeValidator(test_date_range)
        self.assertTrue(validator.is_valid())

        # empty rangedate
        validator.param = None
        self.assertTrue(validator.is_valid())

        # not corrected datetime
        validator.param = '201702021010'
        self.assertFalse(validator.is_valid())

        # start date > end date
        validator.param = '201802021010-201702021010'
        self.assertFalse(validator.is_valid())

class TestNameValidator(TestCase):
    def test_name(self):
        # everithing is OK
        name = 'TEST'
        validator = NameValidator(name)
        self.assertTrue(validator.is_valid())

        # empty name
        validator.param = None
        self.assertFalse(validator.is_valid())

class TestPathValidator(TestCase):
    def test_path_exists(self):
        # everything ok
        path = '/tmp'
        validator = PathValidator(path)
        self.assertTrue(validator.is_valid())

        # weird path
        validator.param = '/TEST_THAT_NOT_EXISTS'
        self.assertFalse(validator.is_valid())

class TestFileValidator(TestCase):
    FILE_OK = '/home/zawadeusz/Documents/picco/tests/testing_file_OK.txt'
    FILE_BAD = '/home/zawadeusz/Documents/picco/tests/testing_file_BAD.txt'

    def test_file_exists(self):
        validator = FileValidator(self.FILE_OK)
        self.assertTrue(validator.is_valid())

        validator = FileValidator('/TEST_NOT_EXISTS')
        self.assertFalse(validator.is_valid())

    def test_file_content(self):
        self.assertFalse(FileValidator('/TEST_NOT_EXISTS').is_valid())
        self.assertTrue(FileValidator(self.FILE_OK).is_valid())
        self.assertFalse(FileValidator(self.FILE_BAD).is_valid())

