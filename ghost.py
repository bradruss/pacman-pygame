import pygame
import random

class Ghost():
    weakGhost = pygame.image.load("weakGhost.png")
    images = [pygame.image.load("redGhost.png"), pygame.image.load("blueGhost.png"),
              pygame.image.load("orangeGhost.png"), pygame.image.load("pinkGhost.png")]
        
    def __init__(self, color):
        self.sprite = self.loadGhost(color)
        self.weak = False
        self.x_pos = 0
        self.y_pos = 0


    def loadGhost(self, color):
        temp = None
        if color == "red":
            temp = self.images[0]
        elif color == "blue":
            temp = self.images[1]
        elif color == "orange":
            temp = self.images[2]
        elif color == "pink":
            temp = self.images[3]
        else:
            temp = self.images[3]
        return temp


    def notVulnerable(self):
        self.weak = False

    def vulnerable(self):
        self.sprite = self.weakGhost
        self.weak = True

    # inside width = 170px
    # 30 px of move up and down -> 110px
    # spawn box at center of screen


    # after being eaten: middle -> left -> right

    def spawnOutside(self):
        # Designated for red ghost starting position
        # Only called when new level
        self.x_pos = 600
        self.y_pos = 300

    def spawnleft(self):
        self.x_pos = 550
        self.y_pos = 350

    def spawnMiddle(self):
        self.x_pos = 600
        self.y_pos = 350

    def spawnRight(self):
        self.x_pos = 650
        self.y_pos = 350

    def moveGhosts(self, x, y):
        ver = x - self.x_pos
        hor = y - self.y_pos
        if ver > 10 and self.current_level.check_valid(self.x_pos, self.y_pos):
            self.x_pos += 5
        elif ver < 10:
            self.x_pos -= 5
        elif hor > 0:
            self.y_pos += 5
        elif hor < 0:
            self.y_pos -= 5
        #r = random.randint(1,10)
        #if r >=5:
        #      if ver > 10 and self.current_level.check_valid(self.x_pos, self.y_pos):
        #            self.x_pos += 5
        #        elif ver < 10:
        #            self.x_pos -= 5
        #        elif hor > 0:
        #            self.y_pos += 5
        #        elif hor < 0:
        #           self.y_pos -= 5
        #elif r == 1:
        #   self.x_pos += 5
        #elif r == 2:
        #   self.x_pos -+ 5
        #elif r == 3:
        #   self.y_pos += 5
        #elif r == 4:
        #   self.y_pos -= 5
     

      

    # TODO: movement algs
    # movement on new/ fresh level:
        # red ghost spawns outside, right above the box
        # up/down in box before spawn. after 5 seconds have passed, spawn new ghost
        # 3 "slots" total in the box. (if somehow the player gets 4 ghost, make two overlap/ put in same slot)



    # chase, scatter, frigtened
    # ghost only move 1 step ahead in map
        # chase player for 20 secs
            # try to chase pac man
            # get position of pac man


        # scatter for 7 secs
            # go to corners of board


        # fright mode random generated
