import os
from unittest import TestCase
from src.validators import CommandArgsValidator

class TestCommandArgsValidator(TestCase):
    def setUp(self):
        kwargs = {
                'in': '/home/zawadeusz',
                'out': '/home/zawadeusz',
                'name': 'Test'
        }

        self.validator = CommandArgsValidator(**kwargs)

    def test_path_exist(self):
        self.assertTrue(os.path.join('/tmp/'))
        self.assertTrue(os.path.join('/home/mateusz/'))
        self.assertTrue(os.path.join('/not_exist/'))

    def test_check(self):
        self.assertTrue(self.validator.check())
        self.validator.kwargs['in'] = None
        self.assertFalse(self.validator.check())

        self.validator.kwargs['in'] = '/tmp'
        self.validator.kwargs['out'] = '/tmp'
        self.validator.kwargs['name'] = 'elo'
        self.assertTrue(self.validator.check())

