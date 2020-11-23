import pygame

class Ghost():
    weakGhost = pygame.image.load("weakGhost.png")
    images = [pygame.image.load("redGhost.png"), pygame.image.load("blueGhost.png")]

        
    def __init__(self, color):
        # Color selection
        if color == "red":
            self.surface = self.images[0]

        elif color == "blue":
            self.surface = self.images[1]


        self.weak = False



        # self.time = 0
        # self.course = 10
        # self.rect = self.surface.get_rect()
        # self.rect.left = 3
        # #self.rect.top = 100


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
        
            
