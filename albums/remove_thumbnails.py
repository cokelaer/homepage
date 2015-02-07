import os
from build import buildAlbum
import webkit
import glob

class RemoveThumbnails(webkit.Scan):

    def __init__(self):
        super(RemoveThumbnails, self).__init__()

    def run(self):
        self._get_directories()
        for directory in self.directories:
            print("Removing thumnails and contents.html in %s" % directory)
            filenames = glob.glob(directory + os.sep + "*thumb*png")
            for filename in filenames:
                print(filename)
                os.remove(filename)

if __name__ == "__main__":
    b = RemoveThumbnails()
    b.run()
