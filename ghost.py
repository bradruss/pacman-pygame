import pygame
import random


class Ghost():
    images_original = [pygame.image.load ("strongGhost.png"),
              pygame.image.load ("weakGhost.png")]
    images = [pygame.transform.rotozoom(images_original[0],0,2),
             pygame.transform.rotozoom(images_original[1],0,0.15)]
        
    def __init__(self):
        self.surface = Ghost.images [0]
        self.weak = False
        self.time = 0
        self.course = 10
        self.rect = self.surface.get_rect()
        self.rect.left = 3
        self.rect.top = 1

    def notVulnerable(self):
        self.surface = Ghost.images [0]
        self.weak = False

    def vulnerable(self):
        self.surface = Ghost.images [1]
        self.weak = True
        self.time = 10

    def reset(self):
        self.surface = Ghost.images [0]
        self.weak = False
        self.time = 0
        self.course = 10
        self.rect.left = 3

    def moveGhosts(self, x, y):
        ver = x - self.rect.left
        hor = y - self.rect.top
        r = random.randint(1,10)
        if r >= 5:
            if ver > 10:
                self.rect.left -= 10
            elif ver < 10:
                self.rect.left += 10
            elif hor > 0:
                self.rect.top -= 10
            elif hor < 0:
                self.rect.top += 10
        elif r == 1:
             self.rect.left -= 1
        elif r == 2:
            self.rect.left += 1
        elif r == 3:
            self.rect.top -= 1
        elif r == 4:
            self.rect.top += 1
        
            
