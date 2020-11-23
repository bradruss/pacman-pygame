from pacman import Pacman
from ghost import Ghost
import pygame as pg
import level
import copy

# Global Constants
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1200

# Graphics Constants
WHITE = (255, 255, 255)
WIDTH = 50

class Game:
    """
    Setup window
    """
    def __init__(self):
        # Set Game Level
        self.current_level = level.Level('level1')
        self.point_map = copy.deepcopy(self.current_level.p_map)
        print(self.point_map)
        self.current_level_total_points = self.current_level.total_points

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
        levelOver = False
        while not levelOver:
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

            self.check_points(x, y)
            self.current_level.draw_level(self.disp, self.point_map)

            # 30 fps
            self.clock.tick(30)
            ghosts_array = [Ghost()]

            # Display static ghost
            for g in ghosts_array:
                self.disp.blit(g.surface, g.rect)

            pg.display.update()

            if self.pacman.numCoins == self.current_level_total_points:
                levelOver = True

            # Pacman pos debugging
            #print("x is " + str(x) + " and y is " + str(y))

        if(self.pacman.numCoins == self.current_level_total_points):
            return 0
        else:
            return 1

    def runGame(self):
        return_code = self.runLevel()
        if return_code == 0:
            while True:
                self.disp.blit(self.background, (0, 0))
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        quit()
                        break
                self.loadYouPassed()
                self.clock.tick(30)
                pg.display.update()



    def check_points(self, x, y):
        midx = x + WIDTH / 2
        midy = y + WIDTH / 2

        left_edge = x  # This is the left edge of pacman
        right_edge = x + WIDTH  # This is the right edge of pacman

        top_edge = y  # This is the top edge of pacman
        bottom_edge = y + WIDTH  # This is the bottom edge of pacman

        # locationh1 = str(right_edge) + "," + str(midy)
        # locationh2 = str(left_edge) + "," + str(midy)
        #
        # locationv1 = str(midx) + "," + str(top_edge)
        # locationv2 = str(midx) + "," + str(bottom_edge)

        location = str(midx) + ","  +str(midy)

        # if locationh1 in self.point_map:
        #     del self.point_map[locationh1]
        #
        # if locationh2 in self.point_map:
        #     del self.point_map[locationh2]
        #
        # if locationv1 in self.point_map:
        #     del self.point_map[locationv1]
        #
        # if locationv2 in self.point_map:
        #     del self.point_map[locationv2]

        print(midx)
        print(midy)
        if (midx, midy) in self.point_map:
            del self.point_map[(midx, midy)]
            print("point removed")
            self.pacman.collectCoin()
        if (midx + (5 - (midx % 5)), midy) in self.point_map:
            del self.point_map[(midx + (5 - (midx % 5)), midy)]
            self.pacman.collectCoin()
        if (midx, midy + (5 - (midx % 5))) in self.point_map:
            del self.point_map[(midx, midy + (5 - (midx % 5)))]
            self.pacman.collectCoin()



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

        coins = self.pacman.getNumCoins()
        score_text = 'SCORE: ' +  str(coins)
        text = self.FONT.render(score_text, False, WHITE)
        # text = self.FONT.render('SCORE:', False, WHITE)
        self.disp.blit(text, (500, 5))

    def loadYouPassed(self):
        score_text = "YOU PASSED LEVEL 1!"
        text = self.FONT.render(score_text, False, WHITE)
        self.disp.blit(text, (500, 5))


if __name__ == '__main__':
    g = Game()
    g.runGame()

