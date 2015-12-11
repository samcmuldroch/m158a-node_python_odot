"""
 Example program to show using an array to back a grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame
from pygame.locals import *

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

pygame.init()

#error noise should be based on the frequency
#implement combo
#playing multiple notes at same time (need to play each note quieter)
#figure-out notes for a song
#possibly have 3 differen't song options

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
numberToNoteDictionary = {1 : 'a', 2 : 'w', 3 : 's', 4 : 'e', 5 : 'd', 6 : 'f', 7 : 'u', 8 : 'i', 9 : 'o', 10 : 'k', 11 : 'l', 12 : ';'}

print(keyboardToNoteDictionary)

def playNote(key, row, noteindex, good, length):
    note = numberToNoteDictionary[key]
    frequency = keyboardToFrequencyDictionary[note]
    currentNote = OSCBundle()
    #USE LENGTH TO DETERMINE AMPLITUDE SO IT DOESNT SOUND SHITTY PLAYING ALL THE NOTES AT ONCE
    #print(row)
    envelopeList[0] = 1/(10-row)
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

def playError():
    errorClient = OSCClient()
    errorClient.connect(("localhost", 54200))
    error = OSCBundle()
    error.append({'addr': "/amplitude", 'args':[1]})
    durationOfError = 1000
    error.append({'addr': "/startValue", 'args': ['start', durationOfError]})
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
    for column in range(12):
        grid[row].append(0)  # Append a cell
 
# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)


musicGrid = [
    [1,0,0,4,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,4,0,0,0,0,0,10,11,12],
    [0,0,3,0,0,0,0,0,0,0,0,0],
    [0,0,0,4,0,0,0,0,0,0,0,0],
    [0,0,0,0,5,0,0,0,0,0,0,0],
    [0,0,0,4,0,0,0,0,0,0,11,0],
    [0,0,3,0,0,0,0,0,0,0,0,0],
    [1,0,0,4,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,6,7,0,0,0,0,0],
    [1,1,2,3,0,0,0,0,0,0,0,0],
    [1,1,2,3,0,0,0,0,0,0,0,12],
    [1,0,0,3,0,0,0,0,0,0,0,0],
    [0,0,2,3,0,0,0,0,0,0,0,0],
    [0,1,2,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,2,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,8,0,0,0,0],
    [0,0,0,0,0,0,0,8,0,0,0,0],
    [1,2,3,4,5,6,7,8,9,10,11,12], #LAST LINE ACTUALLY REACHED
    [0,0,0,0,0,0,0,8,0,0,0,0]
]

musicGridRow = 0
 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [305, 255]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Array Backed Grid")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        keysClicked = []
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to zero
            grid[row][column] = 1
            print("Click ", pos, "Grid coordinates: ", row, column)
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[K_a]:
                keysClicked.append(1)
            if keys[K_w]:
                keysClicked.append(2)
            if keys[K_s]:
                keysClicked.append(3)
            if keys[K_e]:
                keysClicked.append(4)
            if keys[K_d]:
                keysClicked.append(5)
            if keys[K_f]:
                keysClicked.append(6)
            if keys[K_u]:
                keysClicked.append(7)
            if keys[K_i]:
                keysClicked.append(8)
            if keys[K_o]:
                keysClicked.append(9)
            if keys[K_k]:
                keysClicked.append(10)
            if keys[K_l]:
                keysClicked.append(11)
            if keys[K_SEMICOLON]:
                keysClicked.append(12)
                #https://www.pygame.org/docs/ref/key.html
 
    # Set the screen background
    print(keysClicked)
    screen.fill(BLACK)
    newgrid = []
    for roww in range(10):
        # Add an empty array that will hold each cell
        # in this row
        newgrid.append([])
        for columnn in range(12):
            newgrid[roww].append(0)  # Append a cell

    # Draw the grid

    for row in [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]:
        for column in range(12):
            color = WHITE
            newKeysClicked = []
            keyIndex = 1
            for key in keysClicked:
                if grid[row][column] == key:
                    playNote(key, row, keyIndex, True, len(keysClicked))
                    grid[row][column] = 0
                    keyIndex += 1
                else:
                    newKeysClicked.append(key)
            keysClicked = newKeysClicked
            if grid[row][column] == 1:
                color = YELLOW
            if grid[row][column] == 2:
                color = YELLOWGREEN
            if grid[row][column] == 3:
                color = GREEN
            if grid[row][column] == 4:
                color = BLUEGREEN
            if grid[row][column] == 5:
                color = BLUE
            if grid[row][column] == 6:
                color = DARKBLUE
            if grid[row][column] == 7:
                color = BLUEPURPLE
            if grid[row][column] == 8:
                color = PURPLE
            if grid[row][column] == 9:
                color = PINK
            if grid[row][column] == 10:
                color = HOTPINK
            if grid[row][column] == 11:
                color = RED
            if grid[row][column] == 12:
                color = ORANGE
            if row == 9:
                #something important about top row
                row1 = 0
                if grid[row][column] > 0:
                    playError()
            else:
                row1 = row + 1
                newgrid[row1][column] = grid[row][column]
                pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row1 + MARGIN,
                              WIDTH,
                              HEIGHT])

    keyIndexx = 1
    for key in newKeysClicked:
        playNote(key, -1, keyIndexx, False, len(newKeysClicked))
        keyIndexx += 1

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
#applause based on rating
endingClient = OSCClient()
endingClient.connect(("localhost", 54300))
ending = OSCBundle()
rating = 10 #RATING SHOULD BE BASED ON COMBO SCORE SHOULD BE NUMBER BETWEEN 1 AND 10
ending.append({'addr': "/amplitude", 'args':[rating/10]})
durationOfApplause = ((10 - rating) / 10) * 6000
ending.append({'addr': "/startValue", 'args': ['start', durationOfApplause]})
endingClient.send(ending)

pygame.quit()