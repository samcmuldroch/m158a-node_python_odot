import pygame
from pygame.locals import *
from pygame.compat import unichr_, unicode_
import locale
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

#FIX THE GOING UP TO THE NEXT OCTAVE
#error noise should be based on the frequency
#implement combo
#playing multiple notes at same time (need to play each note quieter)
#figure-out notes for a song
#possibly have 3 differen't song options
#have actual song playing in background which gets quieter/louder depending on current score


print("Enter the Song you would like to play.")
print("1--Easy Song")
print("2--Medium Song")
print("3--Difficult Song")
whichKeyboard = "False"
while True:
    whichKeyboard = raw_input("Enter the key corresponding to which song you want to play (NONE if you would like quit): ")
    if (whichKeyboard == "NONE"):
        break;
    if (whichKeyboard == "1"):
        break;
    if (whichKeyboard == "2"):
        break;
    if (whichKeyboard == "3"):
        break;

combo = 0
maxCombo = 0



class cFontManager:
    '''
    A simple class used to manage Font objects and provide a simple way to use
    them to draw text on any surface.
 
    Directly import this file to use the class, or run this file from the
    command line to see a trivial sample.
 
    Written by Scott O. Nelson  
    '''
    def __init__(self, listOfFontNamesAndSizesAsTuple):
        '''
        Pass in a tuple of 2-item tuples.  Each 2-item tuple is a fontname / 
        size pair. To use the default font, pass in a None for the font name.
        Font objects are created for each of the pairs and can then be used
        to draw text with the Draw() method below.
        
        Ex: fontMgr = cFontManager(((None, 24), ('arial', 18), ('arial', 24),
            ('courier', 12), ('papyrus', 50)))
 
        TODO: add support for bold & italics
        '''
        self._fontDict = {}
        for pair in listOfFontNamesAndSizesAsTuple:
            assert len(pair) == 2, \
                "Pair must be composed of a font name and a size - ('arial', 24)"
            if pair[0]:
                fontFullFileName = pygame.font.match_font(pair[0])
            else:
                fontFullFileName = None # use default font
            self._fontDict[pair] = pygame.font.Font(fontFullFileName, pair[1])
 
    def Draw(self, surface, fontName, size, text, rectOrPosToDrawTo, color,
            alignHoriz='left', alignVert='top', antialias=False):
        '''
        Draw text with the given parameters on the given surface.
        
        surface - Surface to draw the text onto.
        
        fontName - Font name that identifies what font to use to draw the text.
        This font name must have been specified in the cFontManager 
        
        rectOrPosToDrawTo - Where to render the text at.  This can be a 2
        item tuple or a Rect.  If a position tuple is used, the align
        arguments will be ignored.
        
        color - Color to draw the text with.
        
        alignHoriz - Specifies horizontal alignment of the text in the
        rectOrPosToDrawTo Rect.  If rectOrPosToDrawTo is not a Rect, the
        alignment is ignored.
        
        alignVert - Specifies vertical alignment of the text in the
        rectOrPosToDrawTo Rect.  If rectOrPosToDrawTo is not a Rect, the
        alignment is ignored.
 
        antialias - Whether to draw the text anti-aliased or not.
        '''
        pair = (fontName, size)
        assert pair in self._fontDict, \
            'Font: %s Size: %d is not available in cFontManager.' % pair
        fontSurface = self._fontDict[(fontName, size)].render(text,
            antialias, color)
        if isinstance(rectOrPosToDrawTo, tuple):
            surface.blit(fontSurface, rectOrPosToDrawTo)
        elif isinstance(rectOrPosToDrawTo, pygame.Rect):
            fontRect = fontSurface.get_rect()
            # align horiz
            if alignHoriz == 'center':
                fontRect.centerx = rectOrPosToDrawTo.centerx
            elif alignHoriz == 'right':
                fontRect.right = rectOrPosToDrawTo.right
            else:
                fontRect.x = rectOrPosToDrawTo.x  # left
            # align vert
            if alignVert == 'center':
                fontRect.centery = rectOrPosToDrawTo.centery
            elif alignVert == 'bottom':
                fontRect.bottom = rectOrPosToDrawTo.bottom
            else:
                fontRect.y = rectOrPosToDrawTo.y  # top
                
            surface.blit(fontSurface, fontRect)
 
def DrawRect(color, key, dimOne, dimTwo, dimThree, dimFour):
    '''A simple demo of the use of the cFontManager class'''
    screen = pygame.display.get_surface()
    fontMgr = cFontManager(((None, 24), (None, 48), ('arial', 24)))
    rect = pygame.Rect(dimOne, dimTwo, dimThree, dimFour)
    pygame.draw.rect(screen, color, rect) 
    rect2 = pygame.Rect(dimOne, dimTwo-4, dimThree, dimFour)       
    fontMgr.Draw(screen, 'arial', 24, key, rect2, BLACK,
        'center', 'top')



pygame.init()

resolution = 400, 200
screen = pygame.display.set_mode(resolution)

fg = 250, 240, 230
bg = 5, 5, 5
wincolor = 40, 40, 90

#fill background
screen.fill(wincolor)

#load font, prepare values
font = pygame.font.Font(None, 80)
text = 'Fonty'
size = font.size(text)

ren = font.render(text, 0, fg, bg)
screen.blit(ren, (10, 10))


octave = 1.0
pianoClient1 = OSCClient()
pianoClient2 = OSCClient()
pianoClient3 = OSCClient()
pianoClient4 = OSCClient()
pianoClient5 = OSCClient()
envelopeList = [1., 20, 0., 1000]
pianoClient1.connect(("localhost", 54310))
pianoClient2.connect(("localhost", 54320))
pianoClient3.connect(("localhost", 54330))
pianoClient4.connect(("localhost", 54340))
pianoClient5.connect(("localhost", 54350))

### Initial Ding Bundle:
initialDingClient = OSCClient()
initialDingClient.connect(("localhost", 54345))
print("Turning on")
initialDing = OSCBundle()
initialDing.append({'addr': "/frequency", 'args':[440.]})
initialDing.append({'addr': "/envelope/line", 'args': [1., 20, 0., 1000]})
initialDingClient.send(initialDing)



keyboardToNoteDictionary = {'w' : 'C#/Db', 'e' : 'D#/Eb', 'u' : 'F#/Gb', 'i' : 'G#/Ab', 'o' : 'A#/Bb', 'a' : 'C', 's' : 'D', 'd' : 'E', 'f' : 'F', 'k' : 'G', 'l' : 'A', ';' : 'B', '1' : 'Octave Up', '2' : 'Octave Down'}
keyboardToFrequencyDictionary = {'w' : 277.18, 'e' : 311.13, 'u' : 369.99, 'i' : 415.30, 'o' : 466.16, 'a' : 261.63, 's' : 293.66, 'd' : 329.63, 'f' : 349.23, 'k' : 392.00, 'l' : 440.00, ';' : 493.88}
numberToNoteDictionary = {1 : 'a', 2 : 'w', 3 : 's', 4 : 'e', 5 : 'd', 6 : 'f', 7 : 'u', 8 : 'i', 9 : 'o', 10 : 'k', 11 : 'l', 12 : ';', 13 : '1', 14 : '2'}
keyNumberToNumberDictionary = {97 : 1, 119 : 2, 115 : 3, 101 : 4, 100 : 5, 102 : 6, 117 : 7, 105 : 8, 111 : 9, 107 : 10, 108 : 11, 59 : 12, 49 : 13, 50 : 14}

print(keyboardToNoteDictionary)

def playNote(key, row, noteindex, good, length, combo):
    #print(combo)
    combo += 1
    print("Current Combo:"),
    print(combo)
    if key == 13 or key == 14:
        return combo
    note = numberToNoteDictionary[key]
    frequency = keyboardToFrequencyDictionary[note]
    currentNote = OSCBundle()
    #USE LENGTH TO DETERMINE AMPLITUDE SO IT DOESNT SOUND SHITTY PLAYING ALL THE NOTES AT ONCE
    #print(row)
    if row == 8 or row == 9:
        envelopeList[0] = 1
    else:
        envelopeList[0] = 0.5 + 0.5*(row/8)
    if good:
        currentNote.append({'addr': "/frequency", 'args':[frequency * octave]})
        currentNote.append({'addr': "/envelope/line", 'args': envelopeList})
    else:
        currentNote.append({'addr': "/frequency", 'args':[frequency * octave]})
        currentNote.append({'addr': "/envelope/line", 'args': envelopeList})
    if noteindex == 1:
        pianoClient1.send(currentNote)
    if noteindex == 2:
        pianoClient2.send(currentNote)
    if noteindex == 3:
        pianoClient3.send(currentNote)
    if noteindex == 4:
        pianoClient4.send(currentNote)
    if noteindex == 5:
        pianoClient5.send(currentNote)
    return combo

def playError():
    print("Oops!")
    combo = 0
    errorClient = OSCClient()
    errorClient.connect(("localhost", 54200))
    error = OSCBundle()
    error.append({'addr': "/startValue", 'args': ['start']})
    errorClient.send(error)


 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 153)
YELLOWGREEN = (204, 255, 153)
GREEN = (153, 255, 153)
BLUEGREEN = (153, 255, 204)
BLUE = (153, 255, 255)
DARKBLUE = (153, 204, 255)
BLUEPURPLE = (153, 153, 255)
PURPLE = (204, 153, 255)
PINK = (255, 153, 255)
HOTPINK = (255, 153, 204)
RED = (255, 153, 153)
ORANGE = (255, 204, 153)
LIGHTYELLOW = (255, 255, 204)
LIGHTGREEN = (229, 255, 204)



 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20
 
# This sets the margin between each cell
MARGIN = 5
 
# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(14):
        grid[row].append(0)  # Append a cell
 
# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)



musicGrid = []

if whichKeyboard == "NONE":
    musicGrid = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]
if whichKeyboard == "1":
    musicGrid = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,11,0,0,0],
        [0,0,0,0,0,5,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,11,0,13,0],
        [0,0,0,0,0,0,0,0,0,0,11,0,0,14],
        [0,0,0,0,0,5,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,11,0,0,13],
        [0,0,0,0,0,0,0,0,0,0,11,0,0,14],
        [0,0,0,0,0,0,0,0,0,0,11,0,0,0],
        [0,0,0,0,0,5,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,6,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,11,0,0,0],
        [0,0,0,0,0,5,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,6,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]
    maxCombo = 17
if whichKeyboard == "2":
    musicGrid = []
if whichKeyboard == "3":
    musicGrid = [
        [1,0,0,4,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,0,0,4,0,0,0,0,0,10,11,12,0,0],
        [0,0,3,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,4,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,5,0,0,0,0,0,0,0,0,0],
        [0,0,0,4,0,0,0,0,0,0,11,0,0,0],
        [0,0,3,0,0,0,0,0,0,0,0,0,0,0],
        [1,0,0,4,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,6,7,0,0,0,0,0,0,0],
        [1,1,2,3,0,0,0,0,0,0,0,0,0,0],
        [1,1,2,3,0,0,0,0,0,0,0,12,0,0],
        [1,0,0,3,0,0,0,0,0,0,0,0,0,0],
        [0,0,2,3,0,0,0,0,0,0,0,0,0,0],
        [0,1,2,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,13,14],
        [1,0,2,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,8,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,8,0,0,0,0,0,0],
        [1,2,3,4,5,6,7,8,9,10,11,12,0,0], #LAST LINE ACTUALLY REACHED
        [0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0]
    ]

musicGridRow = 0
 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [355, 255]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Array Backed Grid")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

keysClicked = []
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        #keysClicked = []
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key in keyNumberToNumberDictionary.keys():
                kay = keyNumberToNumberDictionary[event.key]
                if kay == 13:
                    print("ocatve up")
                    octave = octave * 2
                    keysClicked.append(kay)
                elif kay == 14:
                    print("octave down")
                    octave = octave / 2
                    keysClicked.append(kay)
                else:
                    keysClicked.append(kay)
 
    # Set the screen background
    screen.fill(BLACK)
    newgrid = []
    for roww in range(10):
        # Add an empty array that will hold each cell
        # in this row
        newgrid.append([])
        for columnn in range(14):
            newgrid[roww].append(0)  # Append a cell

    # Draw the grid

    for row in [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]:
        for column in range(14):
            color = WHITE
            keyy = ''
            newKeysClicked = []
            keyIndex = 1
            for key in keysClicked:
                if grid[row][column] == key:
                    combo = playNote(key, row, keyIndex, True, len(keysClicked), combo)
                    grid[row][column] = 0
                    keyIndex += 1
                else:
                    newKeysClicked.append(key)
            keysClicked = newKeysClicked
            if grid[row][column] == 1:
                color = YELLOW
                keyy = 'a'
            if grid[row][column] == 2:
                color = YELLOWGREEN
                keyy = 'w'
            if grid[row][column] == 3:
                color = GREEN
                keyy = 's'
            if grid[row][column] == 4:
                color = BLUEGREEN
                keyy = 'e'
            if grid[row][column] == 5:
                color = BLUE
                keyy = 'd'
            if grid[row][column] == 6:
                color = DARKBLUE
                keyy = 'f'
            if grid[row][column] == 7:
                color = BLUEPURPLE
                keyy = 'u'
            if grid[row][column] == 8:
                color = PURPLE
                keyy = 'i'
            if grid[row][column] == 9:
                color = PINK
                keyy = 'o'
            if grid[row][column] == 10:
                color = HOTPINK
                keyy = 'k'
            if grid[row][column] == 11:
                color = RED
                keyy = 'l'
            if grid[row][column] == 12:
                color = ORANGE
                keyy = ';'
            if grid[row][column] == 13:
                color = LIGHTYELLOW
                keyy = '1'
            if grid[row][column] == 14:
                color = LIGHTGREEN
                keyy = '2'
            if row == 9:
                row1 = 0
            else:
                row1 = row + 1
                newgrid[row1][column] = grid[row][column]
                DrawRect(color, keyy, (MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row1 + MARGIN, WIDTH, HEIGHT)

    keyIndexx = 1
    for key in newKeysClicked:
        playError()

    musicGridRow += 1
    if musicGridRow >= len(musicGrid)-1:
        grid = newgrid
    else:
        newgrid[0] = musicGrid[musicGridRow]
        grid = newgrid
 
    keysClicked = []

    # Limit to 60 frames per second
    clock.tick(3)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
print('APPLAUSE')
if maxCombo == 0:
    maxCombo = combo
#applause based on rating
endingClient = OSCClient()
endingClient.connect(("localhost", 54300))
ending = OSCBundle()
ending.append({'addr': "/amplitude", 'args':[combo/maxCombo]})
durationOfApplause = ((maxCombo - combo) / maxCombo) * 6000
ending.append({'addr': "/startValue", 'args': ['start', durationOfApplause]})
endingClient.send(ending)

pygame.quit()