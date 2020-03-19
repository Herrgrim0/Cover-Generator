# Cover-Generator
generating album cover thanks to [wikipedia][1], [quotationspage][2] and [Flickr][3] on a website

## installation
1. setup a virtualenv
2. activate virtualenv (`source VIRTUALENV_DIRECTORY/bin/activate` or other)
3. ```pip install -r requirements.txt```
4. setup flask ```echo "env FLASK_APP=main.py" > .flaskenv```
5. run it ```flask run```

# TODO:
[X] add pretty font

~~text color adaptation~~

[X] create a website that display a new album when you reload it
[ ] enhance website
[ ] enhance title detection
[ ] trump mode (cc mino)


[1]: http://en.wikipedia.org/w/index.php?title=Special:Random&printable=yes
[2]: http://www.quotationspage.com/random.php
[3]: https://www.flickr.com/explore/interesting/7days
