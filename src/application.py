
class Application(object):
    def __init__(self, *args, **kwargs):
        print(kwargs)
        self.name = 'test'

    def run(self):
        for a in range(9): print(a)
