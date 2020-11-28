import pygame as pg

class Pacman:
    def __init__(self, icon):
        self.numLives = 5
        self.numCoins = 0
        self.isDangerous = False
        self.sprite = [pg.image.load('pacman/Pacman.png'), pg.image.load('pacman/Pacman2.png'), pg.image.load('pacman/Pacman3.png')]
        if icon == 'biden':
            self.sprite = [pg.image.load('biden/close.png'), pg.image.load('biden/close2.png'), pg.image.load('biden/open.png')]
        elif icon == 'trump':
            self.sprite = [pg.image.load('trump/trump-closed.png'), pg.image.load('trump/trump-open.png'),pg.image.load('trump/trump-closed.png')]
        elif icon == 'pacman':
            self.sprite = [pg.image.load('pacman/Pacman.png'), pg.image.load('pacman/Pacman2.png'), pg.image.load('pacman/Pacman3.png')]


        self.waka = pg.mixer.Sound('Sound/waka.wav')
        self.waka.set_volume(0.5)

    def getNumCoins(self):
        return self.numCoins

    def getIsDangerous(self):
        return self.isDangerous

    def setNumCoins(self, numCoins):
        self.numCoins = numCoins

    def collectCoin(self):
        self.numCoins += 1

    def getNumLives(self):
        return self.numLives

    def setNumLives(self, numlives):
        self.numLives = numlives


    #def endLife(self):
    #


    #add array of string of picture name/Line 24 in game.py
    #needs to be able to die









