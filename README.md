# Pac-Man pygame implementation
# Requirement
Pac-Man depends entirely on pygame so pygame needs to be installed first before running.
If you use PyCharm, pygame can be installed directly via the terminal using "pip install pygame" or by
adding a package through the Project Python Interpreter settings.

To install manually, go to https://www.pygame.org/wiki/GettingStarted

To run the game, run game.py

# Play
When you boot up game.py, there will be 5 options presented: "Play", "Play your own level",
"leaderboard", "settings" and "quit."

To navigate through these options, use the up/down arrow keys.

Hitting enter/return will enter the selected mode (highlighted in blue).

# Rules
- The player needs to control pacman and get as many coins as possible where each coin is worth 10 points.     
- The player also needs to avoid the ghost which will chase you on and off for a certain amount of time.   
- The ghost will jump into the maze from their resting spot one by one after a certain amount of time.    
- Player will only have five lives and if any of the ghosts touch the player while the player is vulnerable, 
the player will lose 1 life and the position of the player and all the ghosts will be reset to their original positions.  
- Eating a large coin will make ghosts vulnerable for a certain time and player can eats ghosts to get extra points. Ghost will be respawn after 5 seconds and  
collecting all the coins will move the player to the next level.  

# Play your own Level
By entering the "play your own level" mode, the user can type in the terminal which level they want to play.  
You can create your own levels in LevelCreator (see the other readme) and you can run an existing level by typing something in like levels/level3.
The level input should be a valid level file.

# Leaderboard
Go into the Leaderboard via the start menu to see the high score for the top 20 players.  
The Leaderboard will update the top scores on submission if the new score qualifies for the top 20.  

# Setting
The settings function allows you to choose various Pac-Man sprites.
There are 3 different skins to choose from: Pac-Man, Biden and Trump.  
By choosing Biden or Trump, the Pac-Man sprite, the points sprite, and the ghost sprites will change.

# Quit
Hitting the quit button will exit the game.  

