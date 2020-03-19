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

WIKI_URL = "http://en.wikipedia.org/w/index.php?title=Special:Random&printable=yes"
QUOTATION_URL = "http://www.quotationspage.com/random.php"
FLICKR_URL = "https://www.flickr.com/explore/interesting/7days"
FONT_URL = "https://github.com/google/fonts/archive/master.zip"

class AlbumGenerator:

    def __init__(self):
        self.band_name = None
        self.album_name = None
        self.cover_font = None
        self.cover = None
        self.album_url = None


    def get_band_name(self):
        """Get title of a random wikipedia page"""
        print("parsing band name...")
        url = requests.get(WIKI_URL)
        start = url.text.index("title") + 6
        end = url.text.index("<", start, len(url.text))
        band_name = url.text[start:end]
        band_name = band_name.split("-")[0]
        self.band_name = band_name.strip(" ")


    def get_album_name(self):
        """Get random beginning of a quotation"""
        print("parsing album name...")
        album_name = requests.get(QUOTATION_URL)
        start = album_name.text.index("\"/quote/") # find first quote occurence
        start = album_name.text.index(">", start, len(album_name.text)) + 1 # retain beginning index of quote
        end = album_name.text.index("</a>", start, len(album_name.text))
        album_name = album_name.text[start:end].split()

        if len(album_name) > 4:
            album_name = album_name[0:4]

        re.sub(r'\W+', '', album_name[len(album_name)-1])

        self.album_name = ' '.join(album_name)


    def __str__(self):
        return "{} - {}".format(self.band_name, self.album_name)


    def get_cover(self):
        """Download random pics on Flickr"""
        print("search and download album cover")
        addr = requests.get(FLICKR_URL)
        start = addr.text.index("thumb") + 6 # index after the word index
        end = addr.text.index("title", start, len(addr.text))
        pic_addr = addr.text[start+7:end-2] # link to the pic page
        pic_addr = 'https://www.flickr.com'+ pic_addr

        # print("\n\n\n" + pic_addr + "\n\n\n")

        pic = requests.get(pic_addr)
        start = pic.text.index("class=\"low-res-photo\"")
        end = pic.text.index("main-photo is-hidden", start, len(pic.text))
        pic_url = pic.text[start:end-9] # part of the html with the pic link
        pic_url = pic_url.split("src=\"")[1]
        pic_url = "https:" + pic_url

        # print("\n\n\n" + pic_url + "\n\n\n")

        if not os.path.exists("images"):
            os.makedirs("images")

        self.cover = wget.download(pic_url, out="./images")


    def create_album_cover(self):
        print("creating album cover...")
        album_cover = Image.open(str(self.cover))
        width, height = album_cover.size
        max_size = min(width, height)
        album_cover = album_cover.crop((0, 0, max_size, max_size))

        background = self.create_background(max_size)
        bg_size= background.size[0]

        offset = ((bg_size - max_size) // 2, (bg_size - max_size) // 2) # center im
        background.paste(album_cover, offset)


        self.album_url = str(self.band_name)+"-"+str(self.album_name)+'.jpg'

        background.save(str(self.album_url))
        background.close()
        album_cover.close()

    def create_background(self, cover_size):
        """ create a background 100 pixel bigger with band and title
            param: cover_size, int representing size of cover picture
            return: background, Image object
        """
        background = Image.new('RGB', (cover_size + 100, cover_size + 100), color = 'black')

        font = ImageFont.truetype(str(self.cover_font), 15)

        ImageDraw.Draw(background).text((5, 5), str(self.band_name), (255, 255, 255), font=font)
        ImageDraw.Draw(background).text((cover_size / 2, cover_size +50), 
                                         str(self.album_name), 
                                         (255, 255, 255), 
                                         font=font)
        
        return background


    def get_cover_font(self):
        """open and decompress font zipfile, choose a random font
           and set the member font
        """
        if not os.path.exists("fonts"):
            os.makedirs("fonts")
            font = wget.download(FONT_URL, out="./fonts")

        archive = zipfile.ZipFile('fonts/fonts-master.zip', 'r')
        fonts = list(filter(lambda x: ".ttf" in x, archive.namelist()))
        font_nbr = random.randint(0, len(fonts))
        self.cover_font = archive.extract(fonts[font_nbr])
    
    def get_album_url(self):
        return self.album_url


    def display(self):
        im = Image.open(str(self.album_url))
        im.show()
        im.close()


    def create_album(self):
        self.get_band_name()
        self.get_album_name()
        self.get_cover_font()
        self.get_cover()
        self.create_album_cover()
        os.system("rm -rf fonts-master/")
