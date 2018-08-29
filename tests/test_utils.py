import os
import sys
import shutil
from unittest import TestCase
from src.utils import FileCloner, FileSieve, ImageObject

class BaseTest(TestCase):
    FILES_NUMBER = 9

    def setUp(self):
        """ Create test dir with files """
        self.dir_name = 'TEST'
        self.dir_to_clone = 'TO_CLONE'

        # TODO: change to real image dataset
        os.mkdir(os.path.join('/tmp', self.dir_to_clone))

        for _ in range(self.FILES_NUMBER):
            file_name = f'{_}.txt'
            os.mknod(os.path.join('/tmp', self.dir_to_clone, file_name))

    def tearDown(self):
        shutil.rmtree(os.path.join('/tmp', self.dir_to_clone))
        shutil.rmtree(os.path.join('/tmp', self.dir_name))


class TestFileCloner(BaseTest):

    def test_clone(self):
        self.cloner = FileCloner(self.dir_name)
        src = os.path.join('/tmp', self.dir_to_clone)
        dest = os.path.join('/tmp', self.dir_name)
        self.assertTrue(self.cloner.clone(src, dest))
        self.assertEqual(len(os.listdir(dest)), self.FILES_NUMBER)


class TestFileSieve(BaseTest):
    def setUp(self):
        super().setUp()
        self.dest_name= 'COLECTED'
        os.mkdir(os.path.join('/tmp', self.dir_name))
        os.mkdir(os.path.join('/tmp', self.dest_name))

    def tearDown(self):
        super().tearDown()
        shutil.rmtree(os.path.join('/tmp', self.dest_name))

    def test_group(self):
        sieve = FileSieve('/tmp/TO_CLONE', '/tmp', 'FINAL', [])
        sieve.group()
        print(os.listdir('/tmp/FINAL'))
        shutil.rmtree('/tmp/FINAL')

"""

    def test_group(self):
        out = os.path.join('/tmp', self.dir_to_clone)
        dest = os.path.join('/tmp', self.dest_name)
        sieve = FileSieve(out, dest, 'ELO', None)
        sieve.group()
"""

class TestImageObject(TestCase):

    def test_get_extension(self):
        obj = ImageObject('Name.txt', 'TEST')
        self.assertEqual(obj.get_extension(), 'txt')

        obj = ImageObject('Name-eld.txt', 'TEST')
        self.assertEqual(obj.get_extension(), 'txt')

        obj = ImageObject('dd.Name-eld.png', 'TEST')
        self.assertEqual(obj.get_extension(), 'png')

    def test_exif_data(self):
        path_object = '/home/zawadeusz/Documents/picco/tests/images'
        obj = ImageObject('TEST1.jpg', path_object)
        print(obj.created())

