#!/usr/bin/env python3

"""
Idea came from : http://www.noiseaddicts.com/2009/03/random-band-name-cover-album/
author: Herrgrim0
date: 02/10/2018
"""

# api_key = u' cf8a547fe7fe1b8855ba1eb5ba37b0a5 '
# api_secret = u' b6472fff4d399bac '
# "https://www.flickr.com/explore/interesting/7days/"
import requests
import re
import wget

class AlbumGenerator:
    band_name = None
    album_name = None
    album_cover = None

    def get_band_name(self):
        band_name = requests.get("http://en.wikipedia.org/w/index.php?title=Special:Random&printable=yes")
        band_name = band_name.text.split("title")[1] # parse page title
        band_name = band_name.split("-")[0]
        band_name = band_name.strip(">")
        self.band_name = band_name.strip(" ")

    def get_album_name(self):
        album_name = requests.get("http://www.quotationspage.com/random.php")
        album_name = album_name.text.split("quote")[-4]
        album_name = re.split("<|>", album_name)[1]
        self.album_name = ' '.join(album_name.split()[0:5])

    def __str__(self):
        return "{} - {}".format(self.band_name, self.album_name)

    def get_cover(self):
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
        wget.download(self.cover, out=".")

    def create_album_cover(self):
        pass

    def get_writings(self):
        self.get_band_name()
        self.get_album_name()
        self.get_cover()

if __name__ == '__main__':
    gen = AlbumGenerator()
    gen.get_writings()
    print(gen)
