import pygame as pg

class Pacman:
    def __init__(self, icon):
        self.numLives = 5
        self.numCoins = 0
        self.isDangerous = False
        if icon == 'biden':
            self.sprite = [pg.image.load('biden/close.png'), pg.image.load('biden/close2.png'), pg.image.load('biden/open.png')]

        # TODO: change the icon paths
        elif icon == 'trump':
            self.sprite = [pg.image.load('pacman/Pacman.png'), pg.image.load('pacman/Pacman2.png'), pg.image.load('pacman/Pacman3.png')]
        else:
            self.sprite = [pg.image.load('pacman/Pacman.png'), pg.image.load('pacman/Pacman2.png'), pg.image.load('pacman/Pacman3.png')]


        self.waka = pg.mixer.Sound('Sound/waka.wav')

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









