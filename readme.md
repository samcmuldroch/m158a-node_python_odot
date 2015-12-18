Sydney McMuldroch
Music 158A
12/18/15
Final Project

SYDNEY'S MUSICAL KEYBOARD VIDEOGAME FINAL PROJECT

Instalations Required
- Python 2.7.9
- Pip 1.5.6 (not sure how much this matters, but for reference this is what I used)
- Pygame compatible with Python 2.7.9
      ---HOW TO INSTALL PYGAME FOR A MAC (Disclaimer: I installed it on my Windows so this is only a guess, I haved actually tested how to install pygame on a mac)
            --> open terminal
        	--> run the following commands
        			brew install sdl sdl_image sdl_mixer sdl_ttf portmidi 
					sudo pip install hg+http://bitbucket.org/pygame/pygame
			--> IF THAT FAILS
			     --> Maybe try installing using pip?
			           pip install hg+http://bitbucket.org/pygame/pygame
			--> SORRY IF NONE OF THAT WORKS! I think it should!!


How To Run the Program
1. Open the OPEN_ME file in Max
2. Turn on the Speaker in Max
3. Run the following comands
		cd python
		cd pyhon2
		python grid.py


Tips on Game Play
--The keys displaying on your screen are to be clicked when they reach the bottom row of the grid
--If you don't click the key before it reaches the bottom of your screen all your combo points will be set to 0
--If you click a key not currently on the screen a nasty error will play
--The closer you can play the key to the bottom of the screen the better you did and therefore the louder that note will play
--Start with playing game 1 as it is easiest, just a simple C Scale
--If you are really struggling go into the code of grid.py and find the clock.tick line
		--Setting the clock.tick line to 2 will slow it down to make it easier
		--Setting the clock.tick line to 1 will slow it down even further to make it super easy
--The louder the applause the better you did, good luck and hope you enjoyed!!!!!




Props to Ilya for all the starter files on sending code from python to Max!





