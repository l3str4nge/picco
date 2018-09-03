from utils import FileSieve

class Application(object):
    def __init__(self, *args, **kwargs):

        self.sieve = FileSieve(
                kwargs.get('in'),
                kwargs.get('out'),
                kwargs.get('name'),
                kwargs.get('date')
        )

    def run(self):
        self.sieve.group()
