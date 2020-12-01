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
    trump = [pygame.image.load("TrumpGhosts/TrumpGhost.png"), pygame.image.load("TrumpGhosts/GuilianiGhost.png"),
              pygame.image.load("TrumpGhosts/PenceGhost.png"), pygame.image.load("TrumpGhosts/SessionsGhost.png")]
    weakTrump = [pygame.image.load("TrumpGhosts/TrumpGhostWeak.png"), pygame.image.load("TrumpGhosts/GuilianiGhostWeak.png"),
                 pygame.image.load("TrumpGhosts/PenceGhostWeak.png"), pygame.image.load("TrumpGhosts/SessionsGhostWeak.png")]
    biden = [pygame.image.load("BidenGhosts/BidenGhost.png"), pygame.image.load("BidenGhosts/HarrisGhost.png"),
             pygame.image.load("BidenGhosts/ObamaGhost.png"), pygame.image.load("BidenGhosts/SandersGhost.png")]
    weakBiden = [pygame.image.load("BidenGhosts/BidenGhostWeak.png"),
                 pygame.image.load("BidenGhosts/HarrisGhostWeak.png"),
                 pygame.image.load("BidenGhosts/ObamaGhostWeak.png"),
                 pygame.image.load("BidenGhosts/SandersGhostWeak.png")]

    def __init__(self, color, level_num):
        self.color = color
        self.sprite = self.loadGhost(color)
        self.weak = False
        self.x_pos = 0
        self.y_pos = 0
        self.current_level = level.Level(level_num)
        self.current_level_int = 1
        self.point_map = copy.deepcopy(self.current_level.p_map)
        self.current_direction = None
        self.chase_iterations = 0
        self.random_iterations = -1
        self.death_iterations = 0
        self.dead = False
        self.type = "pacman"
        r = random.randint(1, 4)
        if r == 1:
            self.current_direction = "up"
        elif r == 2:
            self.current_direction = "down"
        elif r == 3:
            self.current_direction = "right"
        else:
            self.current_direction = "left"
        loop = 0

    def resetGhost(self):
        self.current_direction = None
        self.chase_iterations = 0
        self.random_iterations = -1
        r = random.randint(1, 4)
        if r == 1:
            self.current_direction = "up"
        elif r == 2:
            self.current_direction = "down"
        elif r == 3:
            self.current_direction = "right"
        else:
            self.current_direction = "left"

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

    def loadTrumpGhosts(self, color):
        self.type = "trump"
        if color == "red":
            self.sprite = self.trump[0]
        elif color == "blue":
            self.sprite = self.trump[1]
        elif color == "orange":
            self.sprite = self.trump[2]
        elif color == "pink":
            self.sprite = self.trump[3]
        else:
            self.sprite = self.trump[3]
            
    def loadTrumpWeakGhosts(self, color):
        if color == "red":
            self.sprite = self.weakTrump[0]
        elif color == "blue":
            self.sprite = self.weakTrump[1]
        elif color == "orange":
            self.sprite = self.weakTrump[2]
        elif color == "pink":
            self.sprite = self.weakTrump[3]
        else:
            self.sprite = self.weakTrump[3]

    def loadBidenGhosts(self, color):
        self.type = "biden"
        if color == "red":
            self.sprite = self.biden[0]
        elif color == "blue":
            self.sprite = self.biden[1]
        elif color == "orange":
            self.sprite = self.biden[2]
        elif color == "pink":
            self.sprite = self.biden[3]
        else:
            self.sprite = self.biden[3]
    
    def loadBidenWeakGhosts(self, color):
        if color == "red":
            self.sprite = self.weakBiden[0]
        elif color == "blue":
            self.sprite = self.weakBiden[1]
        elif color == "orange":
            self.sprite = self.weakBiden[2]
        elif color == "pink":
            self.sprite = self.weakBiden[3]
        else:
            self.sprite = self.weakBiden[3]

    def notVulnerable(self):          
        if self.type == "biden":
            self.loadBidenGhosts(self.color)
        elif self.type == "trump":
            self.loadTrumpGhosts(self.color)
        else:
            self.sprite = self.loadGhost(self.color)
        self.weak = False

        if self.x_pos % 5 != 0:

            possible_right = self.x_pos + (5 - (self.x_pos % 5))
            possible_left = self.x_pos - (self.x_pos % 5)

            if possible_right > 1150 or possible_right < 0:
                self.x_pos = possible_left
            else:
                self.x_pos = possible_right

        if self.y_pos % 5 != 0:
            possible_down = self.y_pos + (5 - (self.y_pos % 5))
            possible_up = self.y_pos - (self.y_pos % 5)

            if possible_down > 550 or possible_down < 0:
                self.y_pos = possible_up
            else:
                self.y_pos = possible_down


    def vulnerable(self):
        if self.type == "biden":
            self.loadBidenWeakGhosts(self.color)
        elif self.type == "trump":
            self.loadTrumpWeakGhosts(self.color)
        else:
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

    def spawnLeft(self):
        self.x_pos = 550
        self.y_pos = 400

    def spawnMiddle(self):
        self.x_pos = 600
        self.y_pos = 400

    def spawnRight(self):
        self.x_pos = 650
        self.y_pos = 400

    def spawnMiddleBack(self):
        self.x_pos = 600
        self.y_pos = 450

    def maze(self, color):
        if color == "red":
            for i in range(10):
                self.y_pos -= 5
                self.disp.blit(self.sprite, (self.x_pos, self.y_pos))

    def moveChase(self, x, y):
        ver = x - self.x_pos
        hor = y - self.y_pos
        if hor > 0 and self.current_level.check_valid(self.x_pos, self.y_pos + 5):
            self.y_pos += 5
        elif hor < 0 and self.current_level.check_valid(self.x_pos, self.y_pos - 5):
            self.y_pos -= 5
        elif ver > 0 and self.current_level.check_valid(self.x_pos + 5, self.y_pos):
            self.x_pos += 5
        elif ver < 0 and self.current_level.check_valid(self.x_pos - 5, self.y_pos):
            self.x_pos -= 5

    def moveRandom(self):
        # print(self.current_direction)
        if self.current_direction == "up" and self.current_level.check_valid(self.x_pos, self.y_pos - 5):
            self.y_pos -= 5
        elif self.current_direction == "down" and self.current_level.check_valid(self.x_pos, self.y_pos + 5):
            self.y_pos += 5
        elif self.current_direction == "right" and self.current_level.check_valid(self.x_pos + 5, self.y_pos):
            self.x_pos += 5
        elif self.current_direction == "left" and self.current_level.check_valid(self.x_pos - 5, self.y_pos):
            self.x_pos -= 5

        else:
            r = random.randint(1, 4)
            # test if up is good
            if r == 1 and self.current_level.check_valid(self.x_pos, self.y_pos - 5):
                self.current_direction = "up"
                self.y_pos -= 5
            elif r == 2 and self.current_level.check_valid(self.x_pos, self.y_pos + 5):
                self.current_direction = "down"
                self.y_pos += 5
            elif r == 3 and self.current_level.check_valid(self.x_pos + 5, self.y_pos):
                self.current_direction = "right"
                self.x_pos += 5
            elif r == 4 and self.current_level.check_valid(self.x_pos - 5, self.y_pos):
                self.current_direction = "left"
                self.x_pos -= 5
        
    def moveRandomSlow(self):
        # print(self.current_direction)
        if self.current_direction == "up" and self.current_level.check_valid(self.x_pos, self.y_pos - 3):
            self.y_pos -= 3
        elif self.current_direction == "down" and self.current_level.check_valid(self.x_pos, self.y_pos + 3):
            self.y_pos += 3
        elif self.current_direction == "right" and self.current_level.check_valid(self.x_pos + 3, self.y_pos):
            self.x_pos += 3
        elif self.current_direction == "left" and self.current_level.check_valid(self.x_pos - 3, self.y_pos):
            self.x_pos -= 3

        else:
            r = random.randint(1, 4)
            # test if up is good
            if r == 1 and self.current_level.check_valid(self.x_pos, self.y_pos - 3):
                self.current_direction = "up"
                self.y_pos -= 3
            elif r == 2 and self.current_level.check_valid(self.x_pos, self.y_pos + 3):
                self.current_direction = "down"
                self.y_pos += 3
            elif r == 3 and self.current_level.check_valid(self.x_pos + 3, self.y_pos):
                self.current_direction = "right"
                self.x_pos += 3
            elif r == 4 and self.current_level.check_valid(self.x_pos - 3, self.y_pos):
                self.current_direction = "left"
                self.x_pos -= 3

    def checkDeath(self,x,y):
        if (self.x_pos <= (x + 25) <= self.x_pos + 50) and (self.y_pos <= (y + 25) <= self.y_pos + 50):
            return True

        else:
            return False


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