import os
import shutil
import logging

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

    @property
    def temporary_path(self):
        return os.path.join(self.TMP)

