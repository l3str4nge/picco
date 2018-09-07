from utils import FileSieve, FileCompressor
import sys

class Application(object):
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        self.multiple = False # flag to cloning images from file
        self.to_zip = False
        self.to_upload = False

        if self.kwargs.get('file'):
            self.multiple = True

        if self.kwargs.get('zip'):
            self.to_zip = True

        if self.kwargs.get('upload'):
            self.to_upload = True

    def run(self):
        sys.stdout.write('Application starts....\n Start cloning files... \n')

        if not self.multiple:
            params = [self.kwargs['in'], self.kwargs['out'],
                      self.kwargs['name'], self.kwargs['date']]
            self.run_single(*params)
        else:
            self.run_multiple()

        sys.stdout.write('Cloning ends....\n')
        sys.stdout.write('Statistics:\n')
        sys.stdout.write(f'Files copied: {len(self.sieve.container)}\n')
        sys.stdout.write(f'Files not copied: {self.sieve.container.len_omitted()}\n')

    def run_single(self, *args):
        self.sieve = FileSieve(*args)
        self.sieve.group()

        """ Checking flags for zip containers and upload them to Google Drive """
        if self.to_zip:
            sys.stdout.write('Start compressing files...\n')
            container = self.sieve.container
            compressor = FileCompressor(container, self.kwargs['out'], self.kwargs['name'])
            compressor.compress_files()
            sys.stdout.write(f'Compressing ends, file name: {compressor.name}, file size: {compressor.get_compressed_size_in_mb()} mb\n')

        if self.to_upload:
            # TODO: self.to_zip == True
            pass

    def run_multiple(self):
        file_path = self.kwargs.get('file')
        with open(file_path, 'r') as input_file:
            for i, line in enumerate(input_file):
                params = line.rstrip().split(' ')
                sys.stdout.write(f'Line {i} ---> parameters: {params}\n')
                self.run_single(*params)
                sys.stdout.write('.'*80 + '\n')
