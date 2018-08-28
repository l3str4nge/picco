import os
import shutil
import logging

from PIL import Image

logger = logging.getLogger(__name__)

""" RENAME IT TO TEMP CLONER """
class FileCloner:
    TMP = '/tmp'

    def __init__(self, temp_dir_name):
        self.temp_dir_name = temp_dir_name

    def clone(self, src, dest):
        dest = os.path.join(self.TMP, self.temp_dir_name)
        logger.info('Start copying file to temporary directory')
        try:
            shutil.copytree(os.path.join(src), os.path.join(dest))
            return True
        except Exception as e:
            logger.error('Error while copying to temp', e)
            return False

    def remove_temp_dir(self):
        shutil.rmtree(self.temporary_path())

    @property
    def temporary_path(self):
        return os.path.join(self.TMP)



class ImageObject:
    def __init__(self, name, dir_path):
        self.name = name
        self.image_path = os.path.join(dir_path, name)
        self.instance = self.open()
        self.extension = None # TODO: extensions!

    def open(self):
        try:
            return Image.open(self.image_path)
        except Exception as e:
            # TODO: error handling
            pass

    def get_extension(self):
        return self.name.split('.')[-1]

    def is_valid_extension(self):
        return True



    def get_exif_data(self):
        return self.instance._getexif()

    def __str__(self):
        return self.name

class ImageCollector:
    @staticmethod
    def collect(path):
        for root, dirs, files in os.walk(path):
            for f in files:
                yield ImageObject(f, path)

class FileSieve:
    def __init__(self, out, dest, dir_name, date_range):
        self.out_path = os.path.join(out)
        self.dest_path = os.path.join(dest)
        self.dir_name = dir_name
        self.date_range = date_range
        self.cloner = FileCloner(dir_name)


    def group(self):
        grouped_dir_path = os.path.join(self.dest_path, self.dir_name)
        os.mkdir(grouped_dir_path)

        for image_obj in ImageCollector.collect(self.out_path):
            print(image_obj)


