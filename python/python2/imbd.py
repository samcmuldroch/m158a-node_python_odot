import os
import sys
import re
import urllib
import urlparse
import time
import timeit

from mechanize import Browser
from bs4 import BeautifulSoup
from OSC import OSCClient, OSCBundle
from PIL import Image


class Music:

    genreList = {"Action" : [1., 20, 0., 0], "Adventure" : [1., 0, 0., 40], 
        "Animation" : [1., 20, 0., 200], "Biography" : [.25, 20, 0., 1000], 
            "Documentary" : [.25, 20, 0., 1000], "Drama" : [1., 1500, 0., 0], 
                "Family" : [1., 20, 0., 400], "Fantasy" : [1., 20, 0., 1000], 
                    "Film-Noir" : [1., 5, 0.25, 5, 0, 1000], "History" : [1., 20, 0., 1000], 
                        "Horror" : [1., 300, 0., 3000], "Music" : [0.25, 12, 0.5, 25, 0.75, 50, 1., 100, 0., 1000], 
                            "Musical" : [1., 20, 0., 1000], "Mystery" : [1., 1000, 0., 10], 
                                "Sci-Fi" : [0.25, 100, 0.5, 50, 0.75, 25, 1., 12, 0., 1000], 
                                    "Sport" : [1., 20, 0., 1000], "Thriller" : [0.25, 1000, 1, 20, 0, 100], 
                                        "War" : [0.25, 300, 1, 5, 0, 1000]}
    
    extraGenreList = {"Comedy" : ['start', 1000, 2000, 0], "Crime" : ['start', 0, 1000, 0], "Western" : ['start', 100, 1100, 0], "Romance" : ['start', 0, 1000, 0]}

    keyboardToNoteDictionary = {'w' : 'C#/Db', 'e' : 'D#/Eb', 'u' : 'F#/Gb', 'i' : 'G#/Ab', 'o' : 'A#/Bb', 'a' : 'C', 's' : 'D', 'd' : 'E', 'f' : 'F', 'k' : 'G', 'l' : 'A', ';' : 'B', '1' : 'Octave Up', '2' : 'Octave Down'}
    keyboardToFrequencyDictionary = {'w' : 277.18, 'e' : 311.13, 'u' : 369.99, 'i' : 415.30, 'o' : 466.16, 'a' : 261.63, 's' : 293.66, 'd' : 329.63, 'f' : 349.23, 'k' : 392.00, 'l' : 440.00, ';' : 493.88}

    
    def playNoteFunky(self, frequency, clientNumber):
        if frequency == 0:
            return
        currentNote = OSCBundle()
        playList = Music.extraGenreList[self.genre]
        duration = playList[2] - playList[1]
        playList[3] = (duration * 261.63) / (frequency * self.octave)
        currentNote.append({'addr': "/playListComedy", 'args': Music.extraGenreList["Comedy"]})
        currentNote.append({'addr': "/playListCrime", 'args': Music.extraGenreList["Crime"]})
        currentNote.append({'addr': "/playListWestern", 'args': Music.extraGenreList["Western"]})
        currentNote.append({'addr': "/playListRomance", 'args': Music.extraGenreList["Romance"]})
        if clientNumber == 0:
            self.pianoClientAlternate.send(currentNote)
        if clientNumber == 1:
            self.pianoClientAlternate2.send(currentNote)
        if clientNumber == 2:
            self.pianoClientAlternate3.send(currentNote)

    def playNoteTraditional(self, frequency, clientNumber):
        currentNote = OSCBundle()
        currentNote.append({'addr': "/frequency", 'args':[frequency * self.octave]})
        currentNote.append({'addr': "/envelope/line", 'args': self.envelopeList})
        if clientNumber == 0:
            self.pianoClient.send(currentNote)
        if clientNumber == 1:
            self.pianoClient2.send(currentNote)
        if clientNumber == 2:
            self.pianoClient3.send(currentNote)

    def playNote(self, notes):
        ### Initial Ding Bundle:
        frequency = 0
        for i in range(0, len(notes)):
            note = notes[i]
            if (note in Music.keyboardToFrequencyDictionary):
                frequency = Music.keyboardToFrequencyDictionary[note]
            elif (note == '1'):
                self.octave *= 2
            elif (note == '2'):
                self.octave /= 2
            else:
                print("Invalid Note")
                return
            if self.buffer:
                self.playNoteFunky(frequency, i)
            else:
                self.playNoteTraditional(frequency, i)


    def pianoInstrument(self):
        print("Play some music! When you are done with your song type 'DONE'")
        print("Note Key is as Follows:")
        print(Music.keyboardToNoteDictionary)
        print('You can also reference the image to see the keyboard')
        while True:
            notes = raw_input("Enter the Notes you would like to play ('DONE' to stop): ")
            if (notes == "DONE"):
                break;
            else:
                self.playNote(notes);
        print("Thanks for playing")

    def __init__(self, title, rating, genre):
        self.title = title
        self.timeElapsed = 0
        self.rating = rating
        self.genre = genre
        if title == "The Notebook":
            self.genre = "Romance"
        self.rating = rating.encode('ascii')
        self.rating = float(self.rating)
        self.octave = 1.0
        self.pianoClient = OSCClient()
        self.pianoClient2 = OSCClient()
        self.pianoClient3 = OSCClient()
        self.pianoClientAlternate = OSCClient()
        self.pianoClientAlternate2 = OSCClient()
        self.pianoClientAlternate3 = OSCClient()
        self.envelopeList = [1., 20, 0., 1000]
        self.buffer = False

        self.pianoClient.connect(("localhost", 54360))
        self.pianoClient2.connect(("localhost", 54361))
        self.pianoClient3.connect(("localhost", 54362))
        self.pianoClientAlternate.connect(("localhost", 54370))
        self.pianoClientAlternate2.connect(("localhost", 54371))
        self.pianoClientAlternate3.connect(("localhost", 54372))

        initialDingClient = OSCClient()
        initialDingClient.connect(("localhost", 54345))

        ### Initial Ding Bundle:
        print("Turning on the movie")
        initialDing = OSCBundle()
        initialDing.append({'addr': "/frequency", 'args':[440.]})
        initialDing.append({'addr': "/envelope/line", 'args': [1., 20, 0., 1000]})
        self.timeElapsed += 1.02

        initialDingClient.send(initialDing)

        
        
        print('Curtains Openning')
        self.timeElapsed += 16 #note this currently plays right after the initial ding
        time.sleep(self.timeElapsed)
        self.timeElapsed = 0


        for genre in Music.genreList:
            if self.genre == genre:
                self.envelopeList = Music.genreList[genre] 
        for genre in Music.extraGenreList:
            if self.genre == genre:
                self.buffer = True


        startTime = timeit.timeit()
        im = Image.open("keyboard.jpg")
        im.show()
        self.pianoInstrument()
        endTime = timeit.timeit()
        self.timeElapsed += startTime - endTime
        self.timeElapsed += 0.5

        time.sleep(self.timeElapsed)
        self.timeElapsed = 0
        if self.rating < 2: 
            print('Yikes...')
            sadClient = OSCClient()
            sadClient.connect(("localhost", 54346))

            #Sad Ding Bundle:
            sadDing = OSCBundle()
            sadDing.append({'addr': "/start", 'args':[1]})

            sadClient.send(sadDing)
            self.timeElapsed += 4.25
        else:
            print('TADA')
            tadaClient = OSCClient()
            tadaClient.connect(("localhost", 54380))

            tada = OSCBundle()
            tada.append({'addr': "/amplitude", 'args':[self.rating/10]})
            tada.append({'addr': "/startValue", 'args': ['start', 0]})
            tadaClient.send(tada)
            self.timeElapsed += 1.5


        time.sleep(self.timeElapsed)
        
        print('APPLAUSE')
        #applause based on rating
        endingClient = OSCClient()
        endingClient.connect(("localhost", 54350))
        ending = OSCBundle()
        ending.append({'addr': "/amplitude", 'args':[self.rating/10]})
        durationOfApplause = ((10 - self.rating) / 10) * 6000
        ending.append({'addr': "/startValue", 'args': ['start', durationOfApplause]})
        endingClient.send(ending)



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
            music = Music(sys.argv[1], unicode(imdb.rating), imdb.mainGenre)