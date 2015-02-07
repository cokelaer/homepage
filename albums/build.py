#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
import json

import easydev

header = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">

    <title>Thomas Cokelaer.org::photoalbum</title>

    <link rel="stylesheet" type="text/css" href="%(path)s/css/style.css" media="screen" />
    <script type='text/javascript' src='https://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js?ver=1.6.1'></script>
    <script type='text/javascript' src='%(path)s/config_slider.js'></script>

    <script type='text/javascript' src='%(path)s/js/custom.js'></script>
    <script type='text/javascript' src='%(path)s/jquery.nivo.slider.pack.js'></script>

    <link href='http://fonts.googleapis.com/css?family=Oswald' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="%(path)s/css/main.css">
    <script src="%(path)s/js/modernizr-2.0.6.min.js"></script>


    <!-- Le styles -->
    <!-- .cokelaer {
        font-family: "Overlock", "Myriad Pro", "Gill Sans", "Gill Sans MT", Calibri, "Helvetica Neue", Helvetica, sans-serif;
        font-weight: 700;
    } -->
    <link href="%(path)s/bootstrap/css/bootstrap.css" rel="stylesheet">
    <style>
      body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
      }

      /* thumbnail hover */
      a.gallery, a.play {position: relative; display: block;}
      a.gallery .button, a.play .button {position: absolute; top: 50%%; left: 50%%;
                                         font-size: 48px; color: #fff; opacity: 0.8; text-decoration: none;
                                         display: none;}
      a.gallery .button.dark, a.play .button.dark {color: #555;}
      a.gallery:hover .button, a.play:hover .button {display: block;}

      
.caption p {margin-bottom: 0px;}

    </style>
    <link href="%(path)s/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
    <link href="%(path)s/bootstrap/css/colorbox.css" rel="stylesheet">
    <link href="%(path)s/bootstrap/css/font-awesome.css" rel="stylesheet">


   </head>
"""



nav = """

    <body class="home">
    <div id="outer-container">
        <div id="inner">
            <div id="myHeader"></div>
                <script> $('#myHeader').load('%(path)s/header.html'); </script>
            <div id="top-nav" ></div>
                <script> $('#top-nav').load('%(path)s/nav.html'); </script>
        </div>

        <div id="main" role="main">
            <div class="inner">

    """

footer = """
    </div>

    <footer id="footer">
        <script> $('#footer').load('%(path)s/footer.html'); </script>
    </footer>

</div>

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="%(path)s/bootstrap/js/jquery.min.js"></script>
    <script src="%(path)s/bootstrap/js/bootstrap.min.js"></script>
    <script src="%(path)s/bootstrap/js/jquery.colorbox.js"></script>

        <script>
        $(document).ready(function() {
            jQuery('a.gallery').colorbox({rel:'gallery',maxWidth:'90%%',opacity:'0.50',maxWidth:'100%%',maxHeight:'100%%'});
            jQuery('.thumbnail .button').each(function() {
                var x_size = $(this).width();
                var y_size = $(this).height();

                $(this).css('margin-top',-0.5*y_size);
                $(this).css('margin-left',-0.5*x_size);
            });
        });
      
      
        </script>
  </body>
</html>"""


class buildAlbum(object):
    """

        scans the directory and get the images
        creates thumbnails
        if thumb.png not present, copy the first thumbnail into it (random selection)

    """
    def __init__(self, title="undefined", directory="", thumbnail_size=256):
        self.extensions = ["jpg", "JPG", "png", "PNG", "jpeg", "JPEG"]
        self.thumbnails = True
        self.directory = directory
        self.thumbnail_size = thumbnail_size
        self.loadmeta(title)

    def loadmeta(self, title):
        # if there is a metadata file, try to load data from it
        filename = self.directory + os.sep + "metadata.json"
        self.params = {}

        # if found, read title and whatever would be needed
        if os.path.isfile(filename):
            print "Reading " +  filename
            metadata = json.load(open(filename))
            if "title" in metadata.keys():
                self.params['title'] = str(metadata['title'])
        else:
            print "no metadata.json found"
            self.params = {"title":title}

    def build_thumbnails(self):
        """Builds all thumbnails.

        .. warning:: overwrite them if they exists
        """
        filenames = self._get_files()
        print filenames
        for filename in filenames:
            self._convert(filename)
        # find thumb.jpg
        pattern = "thumb.jpg"
        if self.directory != "":
            pattern = self.directory + os.sep + pattern
            
        if len(glob.glob(pattern)) == 0:
            # if not found, create a link
            thumb_names = self._get_thumbnails()
            if len(thumb_names):
                thumb_name = thumb_names[0]
                dr, filename = os.path.split(thumb_name)
                cmd = "ln \"%s\" \"%s\"" % (thumb_name, dr + os.sep + "thumb.jpg")
                easydev.shellcmd(cmd)

    def _convert(self, filename):
        size = self.thumbnail_size
        drive, filename = os.path.split(filename)
        thumb_filename = os.sep.join([drive, "thumb_" + filename ])
        filename = drive + os.sep + filename

        ret = easydev.shellcmd("convert \"%s\" -resize %sx%s \"%s\"" % 
                (filename, size, size, thumb_filename))
    
    def _get_thumbnails(self):
        filenames = []
        for extension in self.extensions:
            pattern = "*." + extension
            if self.directory != "":
                pattern = self.directory + os.sep + pattern
            for this in glob.glob(pattern):
                drive, filename = os.path.split(this)
                if filename.startswith("thumb") == True:
                    filenames.append(this)
        return filenames

    def _get_files(self):
        filenames = []
        for extension in self.extensions:
            pattern = "*." + extension
            if self.directory != "":
                pattern = self.directory + os.sep + pattern
            for this in glob.glob(pattern):
                dr, filename = os.path.split(this)
                if filename.startswith("thumb") == False:
                    filenames.append(this)
        return filenames

    def create_html(self):
        print("entering directory : " + self.directory)
        if self.directory.endswith("/") == False:
            L = self.directory.count("/") + 1
        else:
            L = self.directory.count("/")
        params  = {"path": "/".join([".."]*L)}
        for k,v in self.params.iteritems():
            params[k] = v
        html = header % params + nav % params
        html += self.get_body()
        html += footer % params
        return html
    
    def save_html(self, filename="contents.html"):
        files = self._get_files()
        if len(files):
            text = self.create_html()
            if self.directory != "":
                filename = self.directory + os.sep + filename
            fh = open(filename, "w")
            fh.write(text)
            fh.close()

    def get_body(self):
        filenames = self._get_files()
        if self.directory.endswith("/") == False:
            L = self.directory.count("/") + 1
        else:
            L = self.directory.count("/")
        params  = {"path": "/".join([".."]*L)}
        params['title'] = self.params['title']


        spaces = "    "
        body = spaces + """<div class="container">\n"""
        body += spaces + """<h1>%(title)s</h1>\n"""  % params
        #body += """<p> [2013/05/19]</p>"""
        body += spaces + """<hr/>\n"""
        body += spaces + """<ul class="thumbnails">\n"""
        for i, filename in enumerate(filenames):
            dr, filename = os.path.split(filename)
            thumb_filename = "thumb_" + filename
            body += spaces + """<li class="span3">\n"""
            body += spaces + """<div class="thumbnail">\n"""
            body += spaces + """<a class="gallery" href="%s" title="">\n""" % filename
            body += spaces + """ <img src="%s"/><i></i>\n""" % thumb_filename
            body += spaces + """  </a>\n"""
            body += spaces + """  <div class="caption">\n"""
            body += spaces + """     <p>%s/%s <br/> </p>\n""" % (i+1, len(filenames))
            #body += """     <p>%s/%s <br/> description</p>""" % (i+1, len(filenames))
            body += spaces + """   </div>\n"""
            body += spaces + """  </div>\n"""
            body += spaces + """</li>\n"""
        body += spaces + """</ul>\n"""
        body += spaces + """<div class="row back">
            <p class="span12"><a href="%(path)s/gallery.html">Back</a> to galleries.</p>
        </div>
        </div>
      <hr/>""" % params
        return body


if __name__ == "__main__":
    import sys
    if "--directory" in sys.argv:
        index = sys.argv.index("--directory")
        directory = sys.argv[index+1]
    else:
        directory = ""

    if "--size" in sys.argv:
        index = sys.argv.index("--size")
        size = sys.argv[index+1]
    else:
        size = 256

    a = buildAlbum(directory=directory, thumbnail_size=size)
    a.build_thumbnails() 
    a.save_html("contents.html")



