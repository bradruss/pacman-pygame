import pygame

class Ghost ():
    window_height = 600
    window_width = 1200
    pygame.init()
    disp = pygame.display.set_mode((window_width,window_height))
    images_original = [pygame.image.load ("strongGhost.png").convert_alpha(),
              pygame.image.load ("weakGhost.png").convert_alpha()]
    image = [pygame.transform.rotozoom(images_original[0],0,0.1),
             pygame.transform.rotozoom(images_original[1],0,0.1)]
    background = pygame.image.load('background.jpg')

    disp.blit(background,(0,0))
        
    def init(self):
        self.surface = Ghost.images [0]
        self.weak = False
        self.time = 0
        self.course = [0] * (50 / self.speed)
        x = 0
        y = 0
        disp.blit(self.surface,(x,y))

    def addGhost(self, ghost):
        ghosts.append(Ghost)

    def notVulnerable(self):
        self.surface = Ghost.images [0]
        self.weak = False

    def vulnerable(self):
        self.surface = Ghost.images [1]
        self.weak = True
        self.time = 10

    def moveGhosts(self, pacman):
        ver = pacman.rect.left - self.rect.left
        hor = pacman.rect.top - self.rect.top
        if ver > 0:
            self.rect.left -= 1
        elif ver < 0:
            self.rect.left +=1
            
        
            
