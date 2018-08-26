import os
import shutil
from unittest import TestCase
from src.utils import FileCloner

class TestFileCloner(TestCase):
    FILES_NUMBER = 9
    def setUp(self):
        self.dir_name = 'TEST'
        self.cloner = FileCloner(self.dir_name)

        """ Create test dir with files """
        self.dir_to_clone = 'TO_CLONE'

        os.mkdir(os.path.join('/tmp', self.dir_to_clone))

        for _ in range(self.FILES_NUMBER):
            file_name = f'{_}.txt'
            os.mknod(os.path.join('/tmp', self.dir_to_clone, file_name))


    def tearDown(self):
        shutil.rmtree(os.path.join('/tmp', self.dir_to_clone))
        shutil.rmtree(os.path.join('/tmp', self.dir_name))


    def test_clone(self):
        src = os.path.join('/tmp', self.dir_to_clone)
        dest = os.path.join('/tmp', self.dir_name)
        self.assertTrue(self.cloner.clone(src, dest))
        self.assertEqual(len(os.listdir(dest)), self.FILES_NUMBER)

