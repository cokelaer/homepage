#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

header = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">

    <title>Thomas Cokelaer.org::photoalbum</title>

    <link rel="stylesheet" type="text/css" href="css/style.css" media="screen" />
    <script type='text/javascript' src='https://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js?ver=1.6.1'></script>
    <script type='text/javascript' src='config_slider.js'></script>

    <script type='text/javascript' src='js/custom.js'></script>
    <script type='text/javascript' src='jquery.nivo.slider.pack.js'></script>

    <link href='http://fonts.googleapis.com/css?family=Oswald' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="css/main.css">
    <script src="js/modernizr-2.0.6.min.js"></script>


    <!-- Le styles -->
    <!-- .cokelaer {
        font-family: "Overlock", "Myriad Pro", "Gill Sans", "Gill Sans MT", Calibri, "Helvetica Neue", Helvetica, sans-serif;
        font-weight: 700;
    } -->
    <link href="./bootstrap/css/bootstrap.css" rel="stylesheet">
    <style>
      /* thumbnail hover */
      a.gallery, a.play {position: relative; display: block;}
      a.gallery .button, a.play .button {position: absolute; top: 50%; left: 50%;
                                         font-size: 48px; color: #fff; opacity: 0.8; text-decoration: none;
                                         display: none;}
      a.gallery .button.dark, a.play .button.dark {color: #555;}
      a.gallery:hover .button, a.play:hover .button {display: block;}

      
.caption p {margin-bottom: 0px;}

    </style>
    <link href="./bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
    <link href="./bootstrap/css/colorbox.css" rel="stylesheet">
    <link href="./bootstrap/css/font-awesome.css" rel="stylesheet">




  </head>
"""

nav = """

    <body class="home">
    <div id="outer-container">
        <div id="inner">
            <div id="myHeader"></div>
                <script> $('#myHeader').load('header.html'); </script>
            <div id="top-nav"></div>
                <script> $('#top-nav').load('nav.html'); </script>
        </div>

        <div id="main" role="main">
            <div class="inner">

    """

footer = """
      <div class="row">
        <div class="span9">
          <p>&copy; <a href="mailto:cokelaer at gmail dot com">Thomas Cokelaer</a> 2013 — last modified on %(date)s</p>
        </div>
      </div>
    </div>
    </div>
    </div>


    <footer id="footer">
        <script> $('#footer').load('footer.html'); </script>
    </footer>


    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="./bootstrap/js/jquery.min.js"></script>
    <script src="./bootstrap/js/bootstrap.min.js"></script>
    <script src="./bootstrap/js/jquery.colorbox.js"></script>

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
    Scans all directories recursively

    """
    def __init__(self):
        self.directories = []
        self.get_directories()
        self.params = {"title":"MISC", "main":"./albums"}
        self.debug = False
    
    def get_directories(self):
        self.directories = []
        import os
        for x, y, w in os.walk("."):
            if "contents.html" in w:
                self.directories.append(x)
        self.directories = sorted(self.directories)
        # now, re arrange the directories. We search for years 2013,2012, ... and sort them
        # others will be added at the end.

    def _get_title(self):
        title = "My main gallery"
        return title
    title = property(_get_title)

    def get_html(self):
        import datetime
        d = datetime.datetime.now()
        html = header + nav
        html += self.get_body()
        date = "/".join([str(d.year), "%02d"%d.month, "%02d"%d.day])
        html += footer % {"date": date}
        return html

    def get_body(self):
        titles = list(set(([x.split("/")[2] for x in self.directories])))
        titles = sorted(titles)
        titles.reverse()
        body = """<div class="container">"""

        for title in titles:
            if self.debug: print "------------------------", title
            body += """\n<h1><a href="#%s">%s<a></h1>""" % (title,title )
            body += """\n<hr/>"""
            body += """\n<ul class="thumbnails">"""
            for i, directory in enumerate(self.directories):
                if self.debug: print directory, self.params["main"] + os.sep + title,
                if directory.startswith(self.params["main"] + os.sep + title)==False:
                    if self.debug: print "skip ", directory
                    continue
                if self.debug: print "deal with " + directory
                thistitle = directory.replace("./albums/", "")
                body += """\n<li class="span3">"""
                body += """\n<div class="thumbnail">"""
                body += """\n<a class="play" href="%s/contents.html" title="%s">""" % (directory, thistitle)
                body += """ \n<img src="%s/thumb.jpg"/><i class="icon-camera button"></i>""" % directory
                body += """ \n </a>"""
                body += """ \n </div>"""
                body += """\n</li>"""
            body += """\n</ul>"""


        return body


if __name__ == "__main__":

    a = buildAlbum() 
    text = a.get_html()
    print text



