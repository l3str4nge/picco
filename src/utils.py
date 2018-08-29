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

    def clone_single_file(self, source, dest):
        shutil.copy2(source, dest)

    def remove_temp_dir(self):
        shutil.rmtree(self.temporary_path())

    @property
    def temporary_path(self):
        return os.path.join(self.TMP)



class ImageObject:
    VALID_FORMATS = ['jpg', 'png']
    DATE_CODE = 36867

    def __init__(self, name, dir_path):
        self.name = name
        self.path = os.path.join(dir_path, name)
        self.instance = self.open()
        self.extension = None # TODO: extensions!

    def open(self):
        try:
            return Image.open(self.path)
        except Exception as e:
            # TODO: error handling
            pass

    def get_extension(self):
        return self.name.split('.')[-1]

    def is_valid_extension(self):
        return self.get_extension in self.VALID.FORMATS

    def in_range(self):
        #TODO: check if self is in range of dates
        pass

    def get_exif_data(self):
        return self.instance._getexif()

    def created(self):
        return self.get_exif_data().get(self.DATE_CODE, None)

    def __eq__(self, other):
        if not isinstance(other, ImageObject):
            return False

        return self.get_exif_data == other.get_exif_data

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
        self.dest_path = os.path.join(dest, dir_name)
        self.dir_name = dir_name
        self.date_range = date_range
        self.cloner = FileCloner(dir_name)


    def group(self):
        os.mkdir(self.dest_path)

        for image_obj in ImageCollector.collect(self.out_path):
            new_file_path = os.path.join(self.dest_path, image_obj.name)
            self.cloner.clone_single_file(image_obj.path, new_file_path)

            # TODO: clone object, check extension, rename etc etc
            # check extension
            # check range of date, if not group to others
            # check if exists in new folder
            # clone


