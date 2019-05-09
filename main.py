#!/usr/bin/env python3

import random_band_generator

if __name__ == '__main__':
    Album = random_band_generator.AlbumGenerator()
    Album.create_album()
    print(Album)
