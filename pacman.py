
class Pacman:


    def __init__(self, numCoins, isDangerous):
        self.numCoins = numCoins
        self.isDangerous = isDangerous

    def getNumCoins(self):
        return self.numCoins

    def getIsDangerous(self):
        return self.isDangerous

    def setNumCoins(self, numCoins):
        self.numCoins = numCoins

    def collectCoin(self):
        self.numCoins += 1

    

