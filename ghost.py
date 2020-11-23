import pygame

class Ghost():
    weakGhost = pygame.image.load("weakGhost.png")
    images = [pygame.image.load("redGhost.png"), pygame.image.load("blueGhost.png"),
              pygame.image.load("orangeGhost.png"), pygame.image.load("pinkGhost.png")]
        
    def __init__(self, color):
        # Color selection
        self.sprite = self.loadGhost(color)
        self.weak = False


        # self.time = 0
        # self.course = 10
        # self.rect = self.surface.get_rect()
        # self.rect.left = 3
        # #self.rect.top = 100

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
        self.surface = self.weakGhost
        self.weak = True
        #self.time = 10

    # def moveGhosts(self, pacman):
    #     ver = pacman.rect.left - self.rect.left
    #     hor = pacman.rect.top - self.rect.top
    #     if ver > 0 and level_one.check_valid(self.rect.left,self.rect.top):
    #         self.rect.left -= 1
    #     elif ver < 0 and level_one.check_valid(self.rect.left,self.rect.top):
    #         self.rect.left +=1
    #     elif hor > 0 and level_one.check_valid(self.rect.left,self.rect.top):
    #         self.rect.top -=1
        

    # chase, scatter,
    # ghost only move 1 step ahead in map
        # chase player for 20 secs
            # try to chase pac man
            # get position of pac man
            #

        # scatter for 7 secs
            # go to corners of board



