from pacman import Pacman
from ghost import Ghost
import pygame as pg
import level

# Global Constants
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1200

# Graphics Constants
WHITE = (255, 255, 255)

class Game:
    """
    Setup window
    """
    def __init__(self):
        # Set Game Level
        self.current_level = level.Level('level1')

        # Initialize window
        pg.init()
        self.disp = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Static Font Family
        self.FONT = pg.font.Font('joystix.monospace.ttf', 20)

        # Set window title
        pg.display.set_caption("Pac-man")

        # Create timer for frames
        self.clock = pg.time.Clock()

        # hearts
        self.heart_sprite = pg.image.load('heart.png')

        # Create pacman
        self.pacman = Pacman()

        # Load background
        self.background = pg.image.load('background.jpg')

        # Display the background image
        self.disp.blit(self.background, (0, 0))

    def runLevel(self):
        """
        Run the pacman game
        """
        # Set initial Pacman point
        x = 0
        y = 0

        # Pacman sprite array index
        pacman_image = 0

        # Rotation in degrees
        rotation = 0

        # Used for pac man display
        isLeft = False
        while True:
            # Display pacman and background
            self.disp.blit(self.background, (0, 0))
            self.loadLives()
            self.loadScore()
            '''
            Below loop doesnt work for input but
            is required for the keys_pressed
            '''
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    break

            # Use the following code for keyboard operations
            keys_pressed = pg.key.get_pressed()
            if keys_pressed[pg.K_UP]:
                if y >= 5 and self.current_level.check_valid(x, y - 5):
                    y -= 5
                    if pacman_image < 2:
                        pacman_image += 1
                    else:
                        pacman_image = 0

                    # Rotate Pacman 90 degrees
                    rotation = 90
                    isLeft = False
                    self.disp.blit(pg.transform.rotate(self.pacman.sprite[pacman_image], rotation), (x, y))

            elif keys_pressed[pg.K_DOWN]:

                if y <= 460 and self.current_level.check_valid(x, y + 5):
                    y += 5
                    if pacman_image < 2:
                        pacman_image += 1
                    else:
                        pacman_image = 0

                    # Rotate Pacman -90 degrees
                    rotation = -90
                    isLeft = False
                    self.disp.blit(pg.transform.rotate(self.pacman.sprite[pacman_image], rotation), (x, y))

            elif keys_pressed[pg.K_LEFT]:
                if x >= 5 and self.current_level.check_valid(x - 5, y):
                    x -= 5
                    if pacman_image < 2:
                        pacman_image += 1
                    else:
                        pacman_image = 0

                    isLeft = True

                    # Flip params = (image, X axis flip bool, Y axis flip bool)
                    temp = pg.transform.flip(pg.transform.rotate(self.pacman.sprite[pacman_image], 0), True, False)
                    self.disp.blit(temp, (x, y))

            elif keys_pressed[pg.K_RIGHT]:
                if x <= 1075 and self.current_level.check_valid(x + 5, y):
                    x += 5
                    if pacman_image < 2:
                        pacman_image += 1
                    else:
                        pacman_image = 0
                    rotation = 0
                    isLeft = False
                    self.disp.blit(pg.transform.rotate(self.pacman.sprite[pacman_image], rotation), (x, y))

            elif keys_pressed[pg.K_ESCAPE]:
                quit()

            else:
                # Dont set rotation - occurs when key left
                if isLeft:
                    temp = pg.transform.flip(pg.transform.rotate(self.pacman.sprite[pacman_image], 0), True, False)
                    self.disp.blit(temp, (x, y))

                # Set rotation - occurs when key up, down, and right
                else:
                    self.disp.blit(pg.transform.rotate(self.pacman.sprite[pacman_image], rotation), (x, y))

            self.current_level.draw_level(self.disp)

            # 30 fps
            self.clock.tick(30)
            ghosts_array = [Ghost()]

            # Display static ghost
            for g in ghosts_array:
                self.disp.blit(g.surface, g.rect)

            pg.display.update()

            # Pacman pos debugging
            #print("x is " + str(x) + " and y is " + str(y))


    def setLevel(self, lvl):
        """
        Set the current level
        Modifies class var current_level
        """
        self.current_level = level.Level(lvl)

    def loadLives(self):
        """
        Updates game with current lives
        """
        x = 950
        y = 0

        text = self.FONT.render('LIVES:', False, WHITE)
        self.disp.blit(text, (850, 5))

        for i in range(self.pacman.numLives):
            temp = pg.transform.scale(self.heart_sprite, (30,30))
            self.disp.blit(temp, (x, y))
            x += 30

    def loadScore(self):
        """
        Updates game with current score
        """
        # TODO: implement current score

        text = self.FONT.render('SCORE:', False, WHITE)
        self.disp.blit(text, (500, 5))


if __name__ == '__main__':
    g = Game()
    g.runLevel()

