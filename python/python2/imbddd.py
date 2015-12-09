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

    def playNoteTraditional(self, frequency, clientNumber):
        currentNote = OSCBundle()
        currentNote.append({'addr': "/frequency", 'args':[frequency * self.octave]})
        currentNote.append({'addr': "/envelope/line", 'args': self.envelopeList})
        if clientNumber == 0:
            self.pianoClient1.send(currentNote)
        if clientNumber == 1:
            self.pianoClient2.send(currentNote)
        if clientNumber == 2:
            self.pianoClient3.send(currentNote)

    def playNote(self, notes):
        ### Initial Ding Bundle:
        ### NOTES NEEDS TO COME FROM PYGAME
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
            self.envelopeList = [1., 1500, 0., 0]
            self.playNoteTraditional(frequency, i)


    def __init__(self):
        print(Music.keyboardToNoteDictionary)
        self.title = title
        self.timeElapsed = 0
        self.rating = rating
        self.genre = genre
        if title == "The Notebook":
            self.genre = "Romance"
        self.rating = rating.encode('ascii')
        self.rating = float(self.rating)
        self.octave = 1.0
        self.pianoClient1 = OSCClient()
        self.pianoClient2 = OSCClient()
        self.pianoClient3 = OSCClient()
        self.pianoClientLab1 = OSCClient()
        self.pianoClientLab2 = OSCClient()
        self.pianoClientLab3 = OSCClient()
        self.pianoClientLab4 = OSCClient()
        self.pianoClientLab5 = OSCClient()
        self.pianoClientLab6 = OSCClient()
        self.pianoClientAlternate = OSCClient()
        self.pianoClientAlternate2 = OSCClient()
        self.pianoClientAlternate3 = OSCClient()
        self.envelopeList = [1., 20, 0., 1000]
        self.buffer = False
        self.pedal = False

        self.pianoClient1.connect(("localhost", 54400))
        self.pianoClient2.connect(("localhost", 54361))
        self.pianoClient3.connect(("localhost", 54362))
        self.pianoClientLab1.connect(("localhost", 54380))
        self.pianoClientLab2.connect(("localhost", 54381))
        self.pianoClientLab3.connect(("localhost", 54382))
        self.pianoClientLab1.connect(("localhost", 54500))
        self.pianoClientLab2.connect(("localhost", 54501))
        self.pianoClientLab3.connect(("localhost", 54502))
        self.pianoClientAlternate.connect(("localhost", 54360))
        self.pianoClientAlternate2.connect(("localhost", 54361))
        self.pianoClientAlternate3.connect(("localhost", 54362))

        initialDingClient = OSCClient()
        initialDingClient.connect(("localhost", 54345))

        self.labSynthsAndSounds = True


        ### Initial Ding Bundle:
        #print("Turning on the movie")
        #initialDing = OSCBundle()
        #initialDing.append({'addr': "/frequency", 'args':[440.]})
        #initialDing.append({'addr': "/envelope/line", 'args': [1., 20, 0., 1000]})
        #self.timeElapsed += 1.02

        #initialDingClient.send(initialDing)

        
        
        #print('Curtains Openning')
        #self.timeElapsed += 16 #note this currently plays right after the initial ding
        #time.sleep(self.timeElapsed)
        #self.timeElapsed = 0


        for genre in Music.genreList:
            if self.genre == genre:
                self.envelopeList = Music.genreList[genre] 
        for genre in Music.extraGenreList:
            if self.genre == genre:
                self.buffer = True


        startTime = timeit.timeit()
        #im = Image.open("keyboard.jpg")
        #im.show()
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