#Open the OPEN_ME in Max
#run python imbd.py 'Movie Title' in the terminal while in this folder
#Tada -- you should hear the noise

import sys
import re
import urllib
import urlparse

from mechanize import Browser
from bs4 import BeautifulSoup
from OSC import OSCClient, OSCBundle

class Music:

    genreList = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "Film-Noir", "History", "Horror", "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Sport", "Thriller", "War", "Western"]

    def __init__(self, rating, genre):
        self.rating = rating
        self.genre = genre
        self.rating = rating.encode('ascii')
        self.rating = float(self.rating)


        client = OSCClient()
        client.connect(("localhost", 54345))

        ### Initial Ding Bundle:
        initialDing = OSCBundle()
        initialDing.append({'addr': "/frequency", 'args':[440.]})
        initialDing.append({'addr': "/envelope/line", 'args': [1., 20, 0., 1000]})

        client.send(initialDing)

        print('play curtains openning')
        if self.rating < 1:
            print('play sad noise')
            #play SUPER sad noise
        elif self.rating > 9:
            print('play super happy noise')
            #play SUPER happy noise
        elif self.rating < 5:
            print('play ehh noise')
        else:
            print('play neutral happy noise')
        if self.genre == Music.genreList[0]:
            print('action time')
            #play action noise
        elif self.genre == Music.genreList[1]:
            print('adventure time')
            #play adventure noise
        elif self.genre == Music.genreList[2]:
            print('animation time')
            #play animation noise
        else:
            print('mysterious music')
            #play confused noise
        print('play applause')

class MyOpener(urllib.FancyURLopener):
    """Tricking web servers."""
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'

class ImdbRating:
    """Get the rating of a movie."""
    # title of the movie
    title = None
    # IMDB URL of the movie
    url = None
    # IMDB rating of the movie
    rating = None
    # Did we find a result?
    found = False
    
    # constant
    BASE_URL = 'http://www.imdb.com'
    
    def __init__(self, title):
        self.title = title
        self._process()
        
    def _process(self):
        """Start the work."""
        movie = '+'.join(self.title.split())
        br = Browser()
        url = "%s/find?s=tt&q=%s" % (self.BASE_URL, movie)
        br.open(url)

        if re.search(r'/title/tt.*', br.geturl()):
            self.url = "%s://%s%s" % urlparse.urlparse(br.geturl())[:3]
            soup = BeautifulSoup( MyOpener().open(url).read(), 'html.parser')
        else:
            link = br.find_link(url_regex = re.compile(r'/title/tt.*'))
            res = br.follow_link(link)
            self.url = urlparse.urljoin(self.BASE_URL, link.url)
            soup = BeautifulSoup(res.read(), 'html.parser')

        try:
            self.title = soup.find('h1').contents[0].strip()
            for span in soup.findAll('span'):
                if span.has_attr('itemprop') and span['itemprop'] == 'ratingValue':
                    self.rating = span.contents[0]
                    break
            self.found = True
        except:
            pass

        self.genre=[]
        infobar = soup.find('div',{'class':'infobar'})
        r = infobar.find('',{'title':True})['title']
        self.genrelist = infobar.findAll('a',{'href':True})
        
        for i in range(len(self.genrelist)-1):
            self.genrelist[i] = self.genrelist[i].encode('ascii')
            self.genre.append(self.genrelist[i][16:self.genrelist[i].index('?')])
        self.mainGenre = self.genre[0]
# class ImdbRating

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Usage: %s 'Movie title'" % (sys.argv[0])
    else:
        imdb = ImdbRating(sys.argv[1])
        if imdb.found:
            print("")
            print("Movie title: ")
            print sys.argv[1]
            print("")
            print("Rating: ")
            print imdb.rating
            print("")
            print("Genre: ")
            print imdb.mainGenre
            print("")
            print("SOUNDTRACK")
            music = Music(unicode(imdb.rating), imdb.mainGenre)