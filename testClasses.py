#import pytest
import unittest

import pacman as Pacman

class TestingClasses(unittest.TestCase):

    def setUp(self):
        self.pacmanObj = Pacman.Pacman(10, True, 5)
        #Pacman.Pacman.getNumCoins()

    #Test the functionality of the pacman contructor
    def test_pacMan(self):
        self.assertTrue(self.pacmanObj.getNumCoins(), 10)
        self.assertTrue(self.pacmanObj.getNumLives(), 5)
        self.assertTrue(self.pacmanObj.getIsDangerous(), True)

    #tests the functionality
    def test_pacManSetters(self):
        self.pacmanObj.setNumCoins(20)
        self.assertTrue(self.pacmanObj.getNumCoins(), 20)
        self.pacmanObj.setNumLives(25)
        self.assertTrue(self.pacmanObj.getNumLives(), 25)




if __name__ == '__main__':
    unittest.main()

