import os
import shutil
import logging
import sys
from datetime import datetime
from zipfile import ZipFile

from PIL import Image

logger = logging.getLogger(__name__)

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
    VALID_MOVIE_FORMATS = ['3gp', 'avi', 'mp4']
    DATE_CODE = 36867

    def __init__(self, name, dir_path):
        self.name = name
        self.path = os.path.join(dir_path, name)
        self.instance = self.open()

    def open(self):
        try:
            return Image.open(self.path)
        except Exception as e:
            # TODO: add logging when ready
            print("Cannot open this file", e)

    def get_extension(self):
        return self.name.split('.')[-1]

    def is_valid_extension(self):
        return self.get_extension() in self.VALID_FORMATS

    def is_valid(self, date_range):
        return self.get_extension() and self.in_range(date_range)

    def in_range(self, date_range):
        """
            by default:
            201801011520-201801012000
            more date ranges in the future ....
            exif is like: %YYYY:%m%d %H%M%S
        """

        if not date_range:
            # we allow to not hae date_range to clone whole files
            return True

        date_format = '%Y%m%d%H%M'
        exif_date_format = '%Y:%m:%d %H:%M:%S'
        splitted = date_range.split('-')
        date_start = datetime.strptime(splitted[0], date_format)
        date_end = datetime.strptime(splitted[1], date_format)

        date_created = self.created()
        if not date_created:
            return False

        date_created = date_created.replace(':', '').replace(' ', '')[:-2]
        date_created = datetime.strptime(date_created, date_format)
        return date_start <= date_created <= date_end

    def get_exif_data(self):
        if self.instance:
            exif = self.instance._getexif() or {}
            self.instance.close()
            return exif

        return {}

    def created(self):
        return self.get_exif_data().get(self.DATE_CODE, None)

    def __eq__(self, other):
        if not isinstance(other, ImageObject):
            return False

        return self.get_exif_data() == other.get_exif_data()

    def __str__(self):
        return self.name

class ImageCollector:
    @staticmethod
    def collect(path):
        for root, dirs, files in os.walk(path):
            for f in files:
                yield ImageObject(f, path)

class FileContainer:
    def __init__(self, dest_path):
        self.dest_path = dest_path
        self.files = self.get_files()
        self.files_omitted= []

    def get_files(self):
        return [x for x in ImageCollector.collect(self.dest_path)]

    def __contains__(self, image_obj):
        return image_obj in self.files

    def __len__(self):
        return len(self.files)

    def len_omitted(self):
        return len(self.files_omitted)

    def add(self, image_obj):
        self.files.append(image_obj)

    def omit(self, image_obj):
        self.files_omitted.append(image_obj)

    def get_copied(self):
        for item in self.files:
            yield item

    def get_omitted(self):
        for item in self.files_omitted:
            yield item

    def sort(self):
        sorted_files = sorted(self.files, key=lambda k: k.created())
        for i, f in enumerate(sorted_files):
            # TODO: rename all files and sort it by date
            # TODO add sorting after firsts tests
            pass

class FileSieve:
    def __init__(self, out, dest, dir_name, date_range):
        self.out_path = os.path.join(out)
        self.dest_path = os.path.join(dest, dir_name)
        self.dir_name = dir_name
        self.date_range = date_range
        self.cloner = FileCloner(dir_name)
        self.container = FileContainer(self.dest_path)

    def group(self):
        if not os.path.exists(self.dest_path):
            sys.stdout.write('{self.dest_path} does not exists... created.\n')
            os.mkdir(self.dest_path)

        for i, img_obj in enumerate(ImageCollector.collect(self.out_path)):
            sys.stdout.write(f'{i}) Copy {img_obj.path} to {self.dest_path}\n')
            if img_obj.is_valid(self.date_range):
                img_obj.name = f'{self.dir_name}_{img_obj.created()}.{img_obj.get_extension()}'
                new_file_path = os.path.join(self.dest_path, img_obj.name)

                if not img_obj in self.container:
                    self.cloner.clone_single_file(img_obj.path, new_file_path)
                    img_obj.path = new_file_path
                    self.container.add(img_obj)
                else:
                    self.container.omit(img_obj)
                    sys.stdout.write('File ommited because it is exists in destination directory\n')
            else:
                sys.stdout.write('File is not valid, ommited.... added to not copied files...\n')
                self.container.omit(img_obj)
            sys.stdout.write('------------------------------------------------------------------\n')
        self.container.sort()


class FileCompressor:
    def __init__(self, container, path, name):
        self.container = container
        self.path = path
        self.name = f'{name}.zip'
        self.file_path = os.path.join(self.path, self.name)

    def compress_files(self):
        with ZipFile(self.file_path, 'w') as zip_file:
            for obj in self.container.get_copied():
                zip_file.write(obj.path, obj.name)

    def get_compressed_size(self):
        return os.path.getsize(self.file_path)

    def get_compressed_size_in_mb(self):
        return round(self.get_compressed_size() / 1024 / 1024, 2)

