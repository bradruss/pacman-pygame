import pygame as pg

class Pacman:
    def __init__(self, icon):
        self.numLives = 5
        self.numCoins = 0
        self.isDangerous = False
        self.sprite = [pg.image.load('pacman/Pacman.png'), pg.image.load('pacman/Pacman2.png'), pg.image.load('pacman/Pacman3.png')]
        # TODO: Create custom death animations for trump and biden
        if icon == 'biden':
            self.sprite = [pg.image.load('biden/close.png'), pg.image.load('biden/close2.png'), pg.image.load('biden/open.png')]
            self.death = [pg.image.load('pacman/pacman-death-1.png'), pg.image.load('pacman/pacman-death-2.png'), pg.image.load('pacman/pacman-death-3.png'), pg.image.load('pacman/pacman-death-4.png'),
                          pg.image.load('pacman/pacman-death-5.png'), pg.image.load('pacman/pacman-death-6.png'), pg.image.load('pacman/pacman-death-7.png'), pg.image.load('pacman/pacman-death-8.png')]
        elif icon == 'trump':
            self.sprite = [pg.image.load('trump/trump-closed.png'), pg.image.load('trump/trump-open.png'),pg.image.load('trump/trump-closed.png')]
            self.death = [pg.image.load('pacman/pacman-death-1.png'), pg.image.load('pacman/pacman-death-2.png'), pg.image.load('pacman/pacman-death-3.png'), pg.image.load('pacman/pacman-death-4.png'),
                          pg.image.load('pacman/pacman-death-5.png'), pg.image.load('pacman/pacman-death-6.png'), pg.image.load('pacman/pacman-death-7.png'), pg.image.load('pacman/pacman-death-8.png')]
        elif icon == 'pacman':
            self.sprite = [pg.image.load('pacman/Pacman.png'), pg.image.load('pacman/Pacman2.png'), pg.image.load('pacman/Pacman3.png')]
            self.death = [pg.image.load('pacman/pacman-death-1.png'), pg.image.load('pacman/pacman-death-2.png'), pg.image.load('pacman/pacman-death-3.png'), pg.image.load('pacman/pacman-death-4.png'),
                          pg.image.load('pacman/pacman-death-5.png'), pg.image.load('pacman/pacman-death-6.png'), pg.image.load('pacman/pacman-death-7.png'), pg.image.load('pacman/pacman-death-8.png')]
        else:
            self.sprite = [pg.image.load('pacman/Pacman.png'), pg.image.load('pacman/Pacman2.png'), pg.image.load('pacman/Pacman3.png')]
            self.death = [pg.image.load('pacman/pacman-death-1.png'), pg.image.load('pacman/pacman-death-2.png'), pg.image.load('pacman/pacman-death-3.png'), pg.image.load('pacman/pacman-death-4.png'),
                          pg.image.load('pacman/pacman-death-5.png'), pg.image.load('pacman/pacman-death-6.png'), pg.image.load('pacman/pacman-death-7.png'), pg.image.load('pacman/pacman-death-8.png')]


        self.waka = pg.mixer.Sound('Sound/waka.wav')
        self.waka.set_volume(0.5)

    def getNumCoins(self):
        return self.numCoins

    def getIsDangerous(self):
        return self.isDangerous

    def setNumCoins(self, numCoins):
        self.numCoins = numCoins

    def collectCoin(self):
        self.numCoins += 10

    def getNumLives(self):
        return self.numLives

    def setNumLives(self, numlives):
        self.numLives = numlives

    def showDeath(self, disp, rotation, x, y):
        clock = pg.time.Clock()
        for i in range(0, 8):
            disp.blit(pg.transform.rotate(self.death[i], rotation), (x, y))
            clock.tick(100000)
            pg.display.update()




    #def endLife(self):
    #


    #add array of string of picture name/Line 24 in game.py
    #needs to be able to die









