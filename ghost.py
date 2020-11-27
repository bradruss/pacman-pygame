import pygame 
import random
from pacman import Pacman
import level
import copy
import time

class Ghost():
    weakGhost = pygame.image.load("weakGhost.png")
    images = [pygame.image.load("redGhost.png"), pygame.image.load("blueGhost.png"),
              pygame.image.load("orangeGhost.png"), pygame.image.load("pinkGhost.png")]
        
    def __init__(self, color):
        self.sprite = self.loadGhost(color)
        self.weak = False
        self.x_pos = 0
        self.y_pos = 0
        self.current_level = level.Level('level2')
        self.current_level_int = 1
        self.point_map = copy.deepcopy(self.current_level.p_map)
        self.disp = pygame.display.set_mode((1200, 600))
        self.clock = pygame.time.Clock()
        self.clock.tick(30)
        loop = 0





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
        self.y_pos = 250

    def spawnleft(self):
        self.x_pos = 550
        self.y_pos = 350

    def spawnMiddle(self):
        self.x_pos = 600
        self.y_pos = 350

    def spawnRight(self):
        self.x_pos = 650
        self.y_pos = 350

    def maze(self, color):
        if color == "red":
            for i in range(10):
                self.y_pos -= 5
                self.disp.blit(self.sprite, (self.x_pos, self.y_pos))


    def moveGhost(self, x, y):
        ver = x - self.x_pos
        hor = y - self.y_pos
        if ver > 0 and self.current_level.check_valid(self.x_pos + 5, self.y_pos):
            self.x_pos += 5
        elif ver < 0 and self.current_level.check_valid(self.x_pos - 5, self.y_pos):
            self.x_pos -= 5
        elif hor > 0 and self.current_level.check_valid(self.x_pos, self.y_pos + 5):
            self.y_pos += 5
        elif hor < 0 and self.current_level.check_valid(self.x_pos, self.y_pos - 5):
            self.y_pos -= 5

    def moveRandom(self, x, y):
        ver = x - self.x_pos
        hor = y - self.y_pos
        r = random.randint(1,15)
        move_side_event = pygame.USEREVENT + 1

        # make sure the ghost will chase pacman in the same line
        if ver == 0:
            if hor > 0 and self.current_level.check_valid(self.x_pos, self.y_pos + 5):
                self.y_pos += 5
            elif hor < 0 and self.current_level.check_valid(self.x_pos, self.y_pos - 5):
                self.y_pos -= 5
        if hor == 0:
            if ver > 0 and self.current_level.check_valid(self.x_pos + 5, self.y_pos):
                self.x_pos += 5
            elif ver < 0 and self.current_level.check_valid(self.x_pos - 5, self.y_pos):
                self.x_pos -= 5
        # randomly chase otherwise    
        if r >= 4:
            if ver > 0 and self.current_level.check_valid(self.x_pos + 5, self.y_pos):
                self.x_pos += 5
            elif ver < 0 and self.current_level.check_valid(self.x_pos - 5, self.y_pos):
                self.x_pos -= 5
            elif hor > 0 and self.current_level.check_valid(self.x_pos, self.y_pos + 5):
                self.y_pos += 5
            elif hor < 0 and self.current_level.check_valid(self.x_pos, self.y_pos - 5):
                self.y_pos -= 5
        elif r == 1:
            if self.current_level.check_valid(self.x_pos + 5, self.y_pos):
                self.x_pos += 5
        elif r == 2:
            if self.current_level.check_valid(self.x_pos - 5, self.y_pos):
                self.x_pos -= 5
        elif r == 3:
            if self.current_level.check_valid(self.x_pos, self.y_pos + 5):
                self.y_pos += 5
        elif r == 4:
            if self.current_level.check_valid(self.x_pos, self.y_pos - 5):
                self.y_pos -= 5
            

    def moveLeft(self):
        self.x_pos -= 5
    

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
