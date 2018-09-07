import os
import sys
import shutil
from unittest import TestCase
from src.utils import (
  FileCloner, FileSieve,
  ImageObject, FileContainer,
  FileCompressor
)

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
        if os.path.exists('/tmp/FINAL'):
            shutil.rmtree('/tmp/FINAL')

    def test_group(self):
        date_range = '201705151001-201710101010'
        sieve = FileSieve('/tmp/TO_CLONE', '/tmp', 'FINAL', date_range)
        sieve.group()
        print(os.listdir('/tmp/FINAL'))
        shutil.rmtree('/tmp/FINAL')

    def test_group_with_real_images(self):
        test_path = '/home/zawadeusz/Documents/picco/tests/images'
        date_range = '201705151001-201710101010'
        sievie = FileSieve(test_path, '/tmp', 'FINAL', date_range)
        sievie.group()
        print('realimages', os.listdir('/tmp/FINAL'))
        shutil.rmtree('/tmp/FINAL')

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

class TestFileCompressor(TestCase):
    def test_compress_files(self):
        path = '/home/zawadeusz/Documents/picco/tests/images'
        container = FileContainer(path)
        compressor = FileCompressor(container, '/tmp', 'ZIPPPED')
        compressor.compress_files()

