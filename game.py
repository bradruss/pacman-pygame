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
        self.current_level = level.Level('level2')
        self.current_level_int = 1

        self.point_map = copy.deepcopy(self.current_level.p_map)
        print(self.point_map)

        # Initialize window
        pg.init()
        self.disp = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Static Font Family
        self.FONT = pg.font.Font('joystix.monospace.ttf', 20)

        # Set window title
        pg.display.set_caption("Pac-man")

        # Create timer for frames
        self.clock = pg.time.Clock()

        # Hearts
        self.heart_sprite = pg.image.load('heart.png')

        self.pacman = Pacman()
        self.in_motion = False
        self.motion_type = None
        self.red_ghost = Ghost("red")
        self.blue_ghost = Ghost("blue")
        self.orange_ghost = Ghost("orange")
        self.pink_ghost = Ghost("pink")

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

        # Keep track of previous frame for wall collision
        previous_pacman_image = pacman_image

        # Used for pac man display
        isLeft = False

        new_game = True


        # TODO: make it so when you press left or right when going up or down, it constantly checks to see if barrier is there

        while True:
            # Display pacman and background
            self.disp.blit(self.background, (0, 0))
            self.loadLives()
            self.loadScore()
            self.loadLevelText()

            # TODO: dont forget about movement algs
            if new_game:
                # put ghosts at fixed pos
                self.red_ghost.spawnOutside()
                self.disp.blit(self.red_ghost.sprite, (self.red_ghost.x_pos, self.red_ghost.y_pos))

                self.blue_ghost.spawnleft()
                self.disp.blit(self.blue_ghost.sprite, (self.blue_ghost.x_pos, self.blue_ghost.y_pos))

                self.pink_ghost.spawnMiddle()
                self.disp.blit(self.pink_ghost.sprite, (self.pink_ghost.x_pos, self.pink_ghost.y_pos))

                self.orange_ghost.spawnRight()
                self.disp.blit(self.orange_ghost.sprite, (self.orange_ghost.x_pos, self.orange_ghost.y_pos))

            else:
                # put ghosts at their respective positions
                self.disp.blit(self.red_ghost.sprite, (self.red_ghost.x_pos, self.red_ghost.y_pos))
                self.disp.blit(self.blue_ghost.sprite, (self.blue_ghost.x_pos, self.blue_ghost.y_pos))
                self.disp.blit(self.pink_ghost.sprite, (self.pink_ghost.x_pos, self.pink_ghost.y_pos))
                self.disp.blit(self.orange_ghost.sprite, (self.orange_ghost.x_pos, self.orange_ghost.y_pos))

            new_game = False

            '''
            Below loop doesnt work for input but
            is required for the keys_pressed
            '''
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    break
            if self.in_motion:
                keys_pressed = pg.key.get_pressed()

                if keys_pressed[pg.K_UP] and self.current_level.check_valid(x, y - 5) and self.motion_type != "up":
                    self.motion_type = "up"
                    self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))

                elif keys_pressed[pg.K_DOWN] and self.current_level.check_valid(x, y + 5) and self.motion_type != "down":
                    self.motion_type = "down"
                    self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))

                elif keys_pressed[pg.K_RIGHT] and self.current_level.check_valid(x + 5, y) and self.motion_type != "right":
                    self.motion_type = "right"
                    self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))

                elif keys_pressed[pg.K_LEFT] and self.current_level.check_valid(x - 5, y) and self.motion_type != "left":
                    self.motion_type = "left"
                    self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))

                elif self.motion_type == "up":
                    if y >= 0 and self.current_level.check_valid(x, y - 5):
                        y -= 5
                        self.in_motion = True
                        self.motion_type = "up"
                        if pacman_image < 2:
                            previous_pacman_image = pacman_image
                            pacman_image += 1
                        else:
                            previous_pacman_image = pacman_image
                            pacman_image = 0

                        # Rotate Pacman 90 degrees
                        rotation = 90
                        isLeft = False
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[pacman_image], rotation), (x, y))
                    else:
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))
                        self.in_motion = False

                elif self.motion_type == "down":

                    if y <= 550 and self.current_level.check_valid(x, y + 5):
                        y += 5
                        self.in_motion = True
                        self.motion_type = "down"
                        if pacman_image < 2:
                            previous_pacman_image = pacman_image
                            pacman_image += 1
                        else:
                            previous_pacman_image = pacman_image
                            pacman_image = 0

                        # Rotate Pacman -90 degrees
                        rotation = -90
                        isLeft = False
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[pacman_image], rotation), (x, y))
                    else:
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))
                        self.in_motion = False

                elif self.motion_type == "left":
                    if x >= 0 and self.current_level.check_valid(x - 5, y):
                        self.in_motion = True
                        self.motion_type = "left"
                        x -= 5
                        if pacman_image < 2:
                            previous_pacman_image = pacman_image
                            pacman_image += 1
                        else:
                            previous_pacman_image = pacman_image
                            pacman_image = 0

                        isLeft = True

                        # Flip params = (image, X axis flip bool, Y axis flip bool)
                        temp = pg.transform.flip(pg.transform.rotate(self.pacman.sprite[pacman_image], 0), True, False)
                        self.disp.blit(temp, (x, y))
                    else:
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))
                        self.in_motion = False

                elif self.motion_type == "right":
                    if x <= 1150 and self.current_level.check_valid(x + 5, y):
                        x += 5
                        self.in_motion = True
                        self.motion_type = "right"
                        if pacman_image < 2:
                            previous_pacman_image = pacman_image
                            pacman_image += 1
                        else:
                            previous_pacman_image = pacman_image
                            pacman_image = 0
                        rotation = 0
                        isLeft = False
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[pacman_image], rotation), (x, y))
                    else:
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))
                        self.in_motion = False

                else:
                    self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))
                    self.in_motion = False

            else:


                # Use the following code for keyboard operations
                keys_pressed = pg.key.get_pressed()
                if keys_pressed[pg.K_UP]:
                    if y >= 0 and self.current_level.check_valid(x, y - 5):
                        y -= 5
                        self.in_motion = True
                        self.motion_type = "up"
                        if pacman_image < 2:
                            previous_pacman_image = pacman_image
                            pacman_image += 1
                        else:
                            previous_pacman_image = pacman_image
                            pacman_image = 0

                        # Rotate Pacman 90 degrees
                        rotation = 90
                        isLeft = False
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[pacman_image], rotation), (x, y))
                    else:
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))


                elif keys_pressed[pg.K_DOWN]:

                    if y <= 550 and self.current_level.check_valid(x, y + 5):
                        y += 5
                        self.in_motion = True
                        self.motion_type = "down"
                        if pacman_image < 2:
                            previous_pacman_image = pacman_image
                            pacman_image += 1
                        else:
                            previous_pacman_image = pacman_image
                            pacman_image = 0

                        # Rotate Pacman -90 degrees
                        rotation = -90
                        isLeft = False
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[pacman_image], rotation), (x, y))
                    else:
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))

                elif keys_pressed[pg.K_LEFT]:
                    if x >= 0 and self.current_level.check_valid(x - 5, y):
                        self.in_motion = True
                        self.motion_type = "left"
                        x -= 5
                        if pacman_image < 2:
                            previous_pacman_image = pacman_image
                            pacman_image += 1
                        else:
                            previous_pacman_image = pacman_image
                            pacman_image = 0

                        isLeft = True

                        # Flip params = (image, X axis flip bool, Y axis flip bool)
                        temp = pg.transform.flip(pg.transform.rotate(self.pacman.sprite[pacman_image], 0), True, False)
                        self.disp.blit(temp, (x, y))
                    else:
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))

                elif keys_pressed[pg.K_RIGHT]:
                    if x <= 1150 and self.current_level.check_valid(x + 5, y):
                        x += 5
                        self.in_motion = True
                        self.motion_type = "right"
                        if pacman_image < 2:
                            previous_pacman_image = pacman_image
                            pacman_image += 1
                        else:
                            previous_pacman_image = pacman_image
                            pacman_image = 0
                        rotation = 0
                        isLeft = False
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[pacman_image], rotation), (x, y))
                    else:
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))

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

            pg.display.update()

            # Pacman pos debugging
            #print("x is " + str(x) + " and y is " + str(y))


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
        # TODO: make it so when you want to change levels, change current level int then call setLevel
        self.current_level = level.Level('level' + str(self.current_level_int))

    def loadLives(self):
        x = 950
        y = 0

        text = self.FONT.render('LIVES', False, WHITE)
        self.disp.blit(text, (850, 5))

        semi_colon = self.FONT.render(':', False, WHITE)
        self.disp.blit(semi_colon, (930, 7))

        for i in range(self.pacman.numLives):
            temp = pg.transform.scale(self.heart_sprite, (30, 30))
            self.disp.blit(temp, (x, y))
            x += 30


    def loadScore(self):
        coins = self.pacman.getNumCoins()

        text = self.FONT.render('SCORE', False, WHITE)
        self.disp.blit(text, (500, 5))

        text2 = ':'
        text_semi = self.FONT.render(text2, False, WHITE)
        self.disp.blit(text_semi, (580, 7))

        text3 = str(coins)
        text_score = self.FONT.render(text3, False, WHITE)
        self.disp.blit(text_score, (600, 5))

    def loadLevelText(self):
        # Updates game with current level rendered
        text = self.FONT.render('LEVEL', False, WHITE)
        self.disp.blit(text, (350, 5))

        semi_colon = self.FONT.render(':', False, WHITE)
        self.disp.blit(semi_colon, (430, 7))

        text2 = self.FONT.render(str(self.current_level_int), False, WHITE)
        self.disp.blit(text2, (450, 5))


if __name__ == '__main__':
    g = Game()
    g.runLevel()

