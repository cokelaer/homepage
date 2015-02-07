import os
from build import buildAlbum

class buildAllAlbums(object):

    def __init__(self, size=256):
        self.size = size
        self.directories = []
   
    def _get_directories(self):
        self._directories = []
        for x, y, w in os.walk("."):
                self.directories.append(x)

    def run(self):
        self._get_directories()
        for directory in self.directories:
            print("Building thumbnails and contents.html in %s" % directory)
            album = buildAlbum(thumbnail_size=self.size, directory=directory)
            album.build_thumbnails()
            album.save_html()


if __name__ == "__main__":
    b = buildAllAlbums()
    b.run()
