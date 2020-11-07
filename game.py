import pacman
import ghost
import pygame as pg
import level

# Global Constants for window size
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1200

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

        # Set window title
        pg.display.set_caption("Pac-man")

        # Create timer for frames
        self.clock = pg.time.Clock()

        # hearts
        self.heart_sprite = pg.image.load('heart.png')

        # Pacman sprite array
        self.pacman_sprite = [pg.image.load('pacman/Pacman.png'), pg.image.load('pacman/Pacman2.png'),
                         pg.image.load('pacman/Pacman3.png')]

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
                    self.disp.blit(pg.transform.rotate(self.pacman_sprite[pacman_image], rotation), (x, y))

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
                    self.disp.blit(pg.transform.rotate(self.pacman_sprite[pacman_image], rotation), (x, y))

            elif keys_pressed[pg.K_LEFT]:
                if x >= 5 and self.current_level.check_valid(x - 5, y):
                    x -= 5
                    if pacman_image < 2:
                        pacman_image += 1
                    else:
                        pacman_image = 0

                    isLeft = True

                    # Flip params = (image, X axis flip bool, Y axis flip bool)
                    temp = pg.transform.flip(pg.transform.rotate(self.pacman_sprite[pacman_image], 0), True, False)
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
                    self.disp.blit(pg.transform.rotate(self.pacman_sprite[pacman_image], rotation), (x, y))

            elif keys_pressed[pg.K_ESCAPE]:
                quit()

            else:
                # Dont set rotation - occurs when key left
                if isLeft:
                    temp = pg.transform.flip(pg.transform.rotate(self.pacman_sprite[pacman_image], 0), True, False)
                    self.disp.blit(temp, (x, y))

                # Set rotation - occurs when key up, down, and right
                else:
                    self.disp.blit(pg.transform.rotate(self.pacman_sprite[pacman_image], rotation), (x, y))

            self.current_level.draw_level(self.disp)
            # 30 fps
            self.clock.tick(30)
            pg.display.update()
            print("x is " + str(x) + " and y is " + str(y))


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
        print()



if __name__ == '__main__':
    g = Game()
    g.runLevel()