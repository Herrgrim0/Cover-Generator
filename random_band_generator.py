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
from PIL import Image, ImageFont, ImageDraw

class AlbumGenerator:
    band_name = None
    album_name = None
    album_cover = None

    def get_band_name(self):
        """Get title of a random wikipedia page"""
        print("parsing band name...")
        band_name = requests.get("http://en.wikipedia.org/w/index.php?title=Special:Random&printable=yes")
        band_name = band_name.text.split("title")[1] # parse page title
        band_name = band_name.split("-")[0]
        band_name = band_name.strip(">")
        self.band_name = band_name.strip(" ")

    def get_album_name(self):
        """Get random beginning of a quotation"""
        print("parsing album name...")
        album_name = requests.get("http://www.quotationspage.com/random.php")
        album_name = album_name.text.split("quote")[-4]
        album_name = re.split("<|>", album_name)[1]
        self.album_name = ' '.join(album_name.split()[0:5])

    def __str__(self):
        return "{} - {}".format(self.band_name, self.album_name)

    def get_cover(self):
        """Download random pics on Flickr"""
        print("search and download album cover")
        addr = requests.get("https://www.flickr.com/explore/interesting/7days")
        addr = addr.text.split("</table>")[1]
        addr = addr.split("td")[5]
        addr = re.split("<|>", addr)[4]
        addr = addr.split()[2]
        addr = addr.split("\"")[1]
        addr = 'https://www.flickr.com'+ addr
        r = requests.get(addr)
        r = r.text.split("img")[67]
        r = r.split()[2]
        r = r.split("\"")[1]
        self.cover = 'http:'+ r
        if not os.path.exists("images"):
            os.makedirs("images")

        self.cover = wget.download(self.cover, out="./images")


    def create_album_cover(self):
        print("creating album cover...")
        im = Image.open(str(self.cover))
        name = str(self.band_name)+"-"+str(self.album_name)+'.jpg'

        ImageDraw.Draw(im).text((5, 5), str(self.band_name), (0, 0, 0))
        ImageDraw.Draw(im).text((100, 100), str(self.album_name), (0, 0, 0))

        im.save(str(name))
        im.close()


    def create(self):
        self.get_band_name()
        self.get_album_name()
        self.get_cover()
        self.create_album_cover()
        print("Album cover created !")

if __name__ == '__main__':
    gen = AlbumGenerator()
    gen.create()
    print(gen)
