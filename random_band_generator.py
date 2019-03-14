#!/usr/bin/env python3

"""
Idea came from : http://www.noiseaddicts.com/2009/03/random-band-name-cover-album/
author: Herrgrim0
date: 02/10/2018
"""

import requests
import re
import wget
import os
import random
import zipfile
from PIL import Image, ImageFont, ImageDraw

class AlbumGenerator:
    band_name = None
    album_name = None
    cover_font = None
    cover = None

    def get_band_name(self):
        """Get title of a random wikipedia page"""
        print("parsing band name...")
        url = requests.get("http://en.wikipedia.org/w/index.php?title=Special:Random&printable=yes")
        start = url.text.index("title") + 6
        end = url.text.index("<", start, len(url.text))
        band_name = url.text[start:end]
        band_name = band_name.split("-")[0]
        self.band_name = band_name.strip(" ")

    def get_album_name(self):
        """Get random beginning of a quotation"""
        print("parsing album name...")
        album_name = requests.get("http://www.quotationspage.com/random.php")
        start = album_name.text.index("\"/quote/") # find first quote occurence
        start = album_name.text.index(">", start, len(album_name.text)) + 1 # retain beginning index of quote
        end = album_name.text.index("</a>", start, len(album_name.text))
        album_name = album_name.text[start:end].split()

        if len(album_name) > 4:
            album_name = album_name[0:4]

        # re.sub(r'\W+', '', album_name[-1])

        self.album_name = ' '.join(album_name)

    def __str__(self):
        return "{} - {}".format(self.band_name, self.album_name)

    def get_cover(self):
        """Download random pics on Flickr"""
        print("search and download album cover")
        addr = requests.get("https://www.flickr.com/explore/interesting/7days")
        start = addr.text.index("thumb") + 6 # index after the word index
        end = addr.text.index("title", start, len(addr.text))
        addr = addr.text[start+7:end-2] # link to the pic page
        addr = 'https://www.flickr.com/'+ addr

        pic = requests.get(addr)
        start = pic.text.index("class=\"low-res-photo\"")
        end = pic.text.index("main-photo is-hidden", start, len(pic.text))
        pic_url = pic.text[start:end-9] # part of the html with the pic link
        pic_url = pic_url.split("src=\"")[1]
        pic_url = 'http:'+ pic_url

        if not os.path.exists("images"):
            os.makedirs("images")

        self.cover = wget.download(pic_url, out="./images")


    def create_album_cover(self):
        print("creating album cover...")
        im = Image.open(str(self.cover))
        font = ImageFont.truetype(str(self.cover_font), 15)
        name = str(self.band_name)+"-"+str(self.album_name)+'.jpg'

        ImageDraw.Draw(im).text((5, 5), str(self.band_name), (0, 0, 0), font=font)
        ImageDraw.Draw(im).text((100, 100), str(self.album_name), (0, 0, 0), font=font)

        im.save(str(name))
        im.close()

    def get_cover_font(self):
        if not os.path.exists("fonts"):
            os.makedirs("fonts")
            font = wget.download("https://github.com/google/fonts/archive/master.zip", out="./fonts")

        archive = zipfile.ZipFile('fonts/fonts-master.zip', 'r')
        fonts = list(filter(lambda x: ".ttf" in x, archive.namelist()))
        font_nbr = random.randint(0, len(fonts))
        self.cover_font = archive.extract(fonts[font_nbr])


    def create(self):
        self.get_band_name()
        self.get_album_name()
        print(self)
        self.get_cover_font()
        self.get_cover()
        self.create_album_cover()
        print("Album cover created !")
        os.system("rm -rf fonts-master/")

if __name__ == '__main__':
    gen = AlbumGenerator()
    gen.create()
    os.system("rm -rf fonts-master/")
    print(gen)
