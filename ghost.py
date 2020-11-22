import pygame

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
        #self.rect.top = 100

    def notVulnerable(self):
        self.surface = Ghost.images [0]
        self.weak = False

    def vulnerable(self):
        self.surface = Ghost.images [1]
        self.weak = True
        self.time = 10

    def reset(self)
        self.surface = Ghost.images [0]
        self.weak = False
        self.time = 0
        self.course = 10
        self.rect.left = 3

    # def moveGhosts(self, pacman):
    #     ver = pacman.rect.left - self.rect.left
    #     hor = pacman.rect.top - self.rect.top
    #     if ver > 0 and level_one.check_valid(self.rect.left,self.rect.top):
    #         self.rect.left -= 1
    #     elif ver < 0 and level_one.check_valid(self.rect.left,self.rect.top):
    #         self.rect.left +=1
    #     elif hor > 0 and level_one.check_valid(self.rect.left,self.rect.top):
    #         self.rect.top -=1
        
            
