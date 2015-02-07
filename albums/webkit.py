import os

class Scan(object):

    def __init__(self):
        self.directories = []
   
    def _get_directories(self):
        self._directories = []
        for x, y, w in os.walk("."):
                self.directories.append(x)

