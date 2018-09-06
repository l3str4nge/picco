from utils import FileSieve
import sys

class Application(object):
    def __init__(self, *args, **kwargs):

        self.sieve = FileSieve(
                kwargs.get('in'),
                kwargs.get('out'),
                kwargs.get('name'),
                kwargs.get('date')
        )

    def run(self):
        sys.stdout.write('Application starts....\n Start cloning files... \n')
        self.sieve.group()
        sys.stdout.write('Cloning ends....\n')
        sys.stdout.write('Statistics:\n')

        sys.stdout.write(f'Files copied: {len(self.sieve.container)}\n')
        sys.stdout.write(f'Files not copied: {self.sieve.container.len_omitted()}\n')

