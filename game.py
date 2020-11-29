from pacman import Pacman
from ghost import Ghost
import pygame as pg
import level
import copy

# Global Constants
WINDOW_HEIGHT = 650
WINDOW_WIDTH = 1200

# Graphics Constants
WHITE = (255, 255, 255)
YELLOW = (248, 252, 13)
BLUE = (13, 45, 252)
WIDTH = 50

class Game:
    # Setup window
    def __init__(self):
        self.num_iterations = 0
        # Set Game Level
        self.level = 'levels/level1'
        self.current_level = level.Level(self.level)
        self.current_level_int = 1
        self.max_level = 10
        self.icon = ""
        self.point_sprite = ""

        self.point_map = copy.deepcopy(self.current_level.p_map)
        print(self.point_map)

        # Initialize window
        pg.init()
        self.disp = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Static Font Family
        self.FONT = pg.font.Font('joystix.monospace.ttf', 20)
        self.FONT_LARGE = pg.font.Font('joystix.monospace.ttf', 30)

        # Set window title
        pg.display.set_caption("Pac-Man")

        # Create timer for frames
        self.clock = pg.time.Clock()

        # Hearts
        self.heart_sprite = pg.image.load('heart.png')

        pg.display.set_icon(pg.image.load('pacman/Pacman3.png'))
        self.in_motion = False
        self.play_waka = False
        self.motion_type = None
        self.red_ghost = Ghost("red", self.level)
        self.blue_ghost = Ghost("blue", self.level)
        self.orange_ghost = Ghost("orange", self.level)
        self.pink_ghost = Ghost("pink", self.level)


        # Load background
        self.background = pg.image.load('background.jpg')

        # Display the background image
        self.disp.blit(self.background, (0, 0))

        self.intro_sound = pg.mixer.Sound("Sound/intro.wav")
        self.intro_sound.set_volume(0.2)

        self.death_sound = pg.mixer.Sound("Sound/death.wav")
        self.death_sound.set_volume(0.2)

    def load_new_level(self):
        if 0 < self.current_level_int <= 10:
            self.current_level_int += 1
            text = self.FONT.render('Level ' + str(self.current_level_int), False, WHITE)
            for i in range(0, 150):
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        quit()
                        break
                self.disp.blit(self.background, (0, 0))
                self.disp.blit(text, (500, 300))
                self.clock.tick(30)
                pg.display.update()

            self.pacman_respawn()
            current_level_str = 'levels/level' + str(self.current_level_int)
            self.level = current_level_str
            self.current_level = level.Level(self.level)
            self.point_map = copy.deepcopy(self.current_level.p_map)

            #update ghosts' levels
            self.red_ghost.current_level = self.current_level
            self.blue_ghost.current_level = self.current_level
            self.orange_ghost.current_level = self.current_level
            self.pink_ghost.current_level = self.current_level

            return 0
        else:
            text = self.FONT.render('YOU BEAT THE GAME! ', False, WHITE)
            for i in range(0, 500):
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        quit()
                        break
                self.disp.blit(self.background, (0, 0))
                self.disp.blit(text, (500, 300))
                self.clock.tick(30)
                pg.display.update()
            return -1



    def setIcon(self, icon):
        self.icon = icon

    def red_ghost_move(self, num_iterations, x, y):
        if num_iterations < 0 :
            pass
        else:
            if self.red_ghost.chase_iterations <= 200 and self.red_ghost.chase_iterations != -1:
                self.red_ghost.moveChase(x, y)
                self.red_ghost.chase_iterations += 1
                if self.red_ghost.chase_iterations > 200:
                    self.red_ghost.chase_iterations = -1
                    self.red_ghost.random_iterations = 0

            if self.red_ghost.random_iterations <= 150 and self.red_ghost.random_iterations != -1:
                self.red_ghost.moveRandom()
                self.red_ghost.random_iterations += 1
                if self.red_ghost.random_iterations > 150:
                    self.red_ghost.random_iterations = -1
                    self.red_ghost.chase_iterations = 0

    def orange_ghost_move(self, num_iterations, x, y):
        if num_iterations < 500 :
            pass
        
        elif num_iterations == 500:
            self.orange_ghost.spawnOutside()
            
        else:
            if self.orange_ghost.chase_iterations <= 200 and self.orange_ghost.chase_iterations != -1:
                self.orange_ghost.moveChase(x, y)
                self.orange_ghost.chase_iterations += 1
                if self.orange_ghost.chase_iterations > 200:
                    self.orange_ghost.chase_iterations = -1
                    self.orange_ghost.random_iterations = 0

            if self.orange_ghost.random_iterations <= 150 and self.orange_ghost.random_iterations != -1:
                self.orange_ghost.moveRandom()
                self.orange_ghost.random_iterations += 1
                if self.orange_ghost.random_iterations > 150:
                    self.orange_ghost.random_iterations = -1
                    self.orange_ghost.chase_iterations = 0

    def blue_ghost_move(self, num_iterations, x, y):
        if num_iterations < 1000:
            pass

        elif num_iterations == 1000:
            self.blue_ghost.spawnOutside()

        else:
            if self.blue_ghost.chase_iterations <= 200 and self.blue_ghost.chase_iterations != -1:
                self.blue_ghost.moveChase(x, y)
                self.blue_ghost.chase_iterations += 1
                if self.blue_ghost.chase_iterations > 200:
                    self.blue_ghost.chase_iterations = -1
                    self.blue_ghost.random_iterations = 0

            if self.blue_ghost.random_iterations <= 150 and self.blue_ghost.random_iterations != -1:
                self.blue_ghost.moveRandom()
                self.blue_ghost.random_iterations += 1
                if self.blue_ghost.random_iterations > 150:
                    self.blue_ghost.random_iterations = -1
                    self.blue_ghost.chase_iterations = 0

    def pink_ghost_move(self, num_iterations, x, y):
        if num_iterations < 1500:
            pass

        elif num_iterations == 1500:
            self.pink_ghost.spawnOutside()

        else:
            if self.pink_ghost.chase_iterations <= 200 and self.pink_ghost.chase_iterations != -1:
                self.pink_ghost.moveChase(x, y)
                self.pink_ghost.chase_iterations += 1
                if self.pink_ghost.chase_iterations > 200:
                    self.pink_ghost.chase_iterations = -1
                    self.pink_ghost.random_iterations = 0

            if self.pink_ghost.random_iterations <= 150 and self.pink_ghost.random_iterations != -1:
                self.pink_ghost.moveRandom()
                self.pink_ghost.random_iterations += 1
                if self.pink_ghost.random_iterations > 150:
                    self.pink_ghost.random_iterations = -1
                    self.pink_ghost.chase_iterations = 0

    def check_death(self, x, y):
        return self.red_ghost.checkDeath(x, y) or self.blue_ghost.checkDeath(x, y) or self.pink_ghost.checkDeath(x, y) or self.orange_ghost.checkDeath(x, y)


    def runLevel(self):
        """
        Run the pacman game
        """
        self.pacman = Pacman(self.icon)
        # Set initial Pacman point
        x = 0
        y = 50

        # Pacman sprite array index
        pacman_image = 0

        # Rotation in degrees
        rotation = 0

        # Keep track of previous frame for wall collision
        previous_pacman_image = pacman_image

        # Used for pac man display
        isLeft = False

        new_game = True

        # music stuff
        channel = pg.mixer.Channel(1)


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
                if not channel.get_busy():
                    channel.play(self.pacman.waka)

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
                    if y >= 50 and self.current_level.check_valid(x, y - 5):
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

                    if y <= 600 and self.current_level.check_valid(x, y + 5):
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
                channel.stop()
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
            self.current_level.draw_level(self.disp, self.point_map, self.point_sprite)

            self.red_ghost_move(self.num_iterations, x, y)
            self.blue_ghost_move(self.num_iterations, x, y)
            self.orange_ghost_move(self.num_iterations, x, y)
            self.pink_ghost_move(self.num_iterations, x, y)


            # 30 fps
            self.clock.tick(30)

            pg.display.update()


            if self.check_death(x, y):
                pg.mixer.Sound.play(self.death_sound)
                self.show_death(rotation, x, y)
                self.pacman.setNumLives(self.pacman.numLives - 1)

                if self.pacman.numLives == 0:
                    self.game_over()
                    break

                else:
                    self.red_ghost.resetGhost()
                    self.blue_ghost.resetGhost()
                    self.orange_ghost.resetGhost()
                    self.pink_ghost.resetGhost()
                    self.pacman_respawn()
                    self.num_iterations = 0
                    rotation = 0
                    x = 0
                    y = 50

            if len(self.point_map) == 0:
                return_val = self.load_new_level()
                self.red_ghost.resetGhost()
                self.blue_ghost.resetGhost()
                self.orange_ghost.resetGhost()
                self.pink_ghost.resetGhost()
                self.pacman_respawn()
                self.num_iterations = 0
                rotation = 0
                x = 0
                y = 50
                if return_val == -1:
                    break

            self.num_iterations += 1

            # Pacman pos debugging
            #print("x is " + str(x) + " and y is " + str(y))

    def pacman_respawn(self):
        # Set initial Pacman point
        x = 0
        y = 50

        # Pacman sprite array index
        pacman_image = 0

        # Rotation in degrees
        rotation = 0

        for i in range(0, 64):
            # Display pacman and background
            self.disp.blit(self.background, (0, 0))
            self.loadLives()
            self.loadScore()
            self.loadLevelText()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    break

            self.disp.blit(pg.transform.rotate(self.pacman.sprite[pacman_image], rotation), (x, y))
            self.current_level.draw_level(self.disp, self.point_map, self.point_sprite)

            # put ghosts at fixed pos
            self.red_ghost.spawnOutside()
            self.disp.blit(self.red_ghost.sprite, (self.red_ghost.x_pos, self.red_ghost.y_pos))

            self.blue_ghost.spawnleft()
            self.disp.blit(self.blue_ghost.sprite, (self.blue_ghost.x_pos, self.blue_ghost.y_pos))

            self.pink_ghost.spawnMiddle()
            self.disp.blit(self.pink_ghost.sprite, (self.pink_ghost.x_pos, self.pink_ghost.y_pos))

            self.orange_ghost.spawnRight()
            self.disp.blit(self.orange_ghost.sprite, (self.orange_ghost.x_pos, self.orange_ghost.y_pos))


            self.clock.tick(30)
            pg.display.update()


    def show_death(self, rotation, x, y):

        self.disp.blit(pg.transform.rotate(self.pacman.death[0 // 10], rotation), (x, y))

        for i in range(0, 64):
            # Display pacman and background
            self.disp.blit(self.background, (0, 0))
            self.loadLives()
            self.loadScore()
            self.loadLevelText()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    break


            self.disp.blit(self.red_ghost.sprite, (self.red_ghost.x_pos, self.red_ghost.y_pos))
            self.disp.blit(self.blue_ghost.sprite, (self.blue_ghost.x_pos, self.blue_ghost.y_pos))
            self.disp.blit(self.pink_ghost.sprite, (self.pink_ghost.x_pos, self.pink_ghost.y_pos))
            self.disp.blit(self.orange_ghost.sprite, (self.orange_ghost.x_pos, self.orange_ghost.y_pos))

            self.disp.blit(pg.transform.rotate(self.pacman.death[i // 8], 0), (x, y))
            self.current_level.draw_level(self.disp, self.point_map, self.point_sprite)

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

        # print(midx)
        # print(midy)
        if (midx, midy) in self.point_map:
            del self.point_map[(midx, midy)]
            # print("point removed")
            self.pacman.collectCoin()
        if (midx + (5 - (midx % 5)), midy) in self.point_map:
            del self.point_map[(midx + (5 - (midx % 5)), midy)]
            self.pacman.collectCoin()
        if (midx, midy + (5 - (midx % 5))) in self.point_map:
            del self.point_map[(midx, midy + (5 - (midx % 5)))]
            self.pacman.collectCoin()

    def game_over(self):
        text = self.FONT.render('Game Over', False, WHITE)
        for i in range(0, 600):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    break
            self.disp.blit(self.background, (0, 0))
            self.disp.blit(text, (500, 300))
            self.clock.tick(30)
            pg.display.update()



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


    # TODO: most likely want to use a separate file here...
    def loadLeaderboard(self):
        print()

    def loadSettings(self):
        # Load previous setting
        current = 0
        if self.icon == "biden":
            default_color = WHITE
            biden_color = BLUE
            trump_color = WHITE
            back_color = WHITE
            current = 1

        elif self.icon == "trump":
            default_color = WHITE
            biden_color = WHITE
            trump_color = BLUE
            back_color = WHITE
            current = 2

        else:
            default_color = BLUE
            biden_color = WHITE
            trump_color = WHITE
            back_color = WHITE

        while True:
            # Change pac man icon to pac man, biden or trump
            self.disp.blit(self.background, (0, 0))

            text = self.FONT.render('SKIN SELECTION:', False, WHITE)
            self.disp.blit(text, (490, 200))

            text = self.FONT.render('DEFAULT', False, default_color)
            self.disp.blit(text, (550, 250))

            text = self.FONT.render('BIDEN', False, biden_color)
            self.disp.blit(text, (560, 300))

            text = self.FONT.render('TRUMP', False, trump_color)
            self.disp.blit(text, (560, 350))

            text = self.FONT.render('BACK TO MENU', False, back_color)
            self.disp.blit(text, (510, 400))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    break

            keys_pressed = pg.key.get_pressed()
            if keys_pressed[pg.K_ESCAPE]:
                quit()

            elif keys_pressed[pg.K_UP]:
                if current == 0:
                    default_color = WHITE
                    back_color = BLUE
                    current = 3

                elif current == 1:
                    biden_color = WHITE
                    default_color = BLUE
                    current = 0

                elif current == 2:
                    trump_color = WHITE
                    biden_color = BLUE
                    current = 1

                elif current == 3:
                    back_color = WHITE
                    trump_color = BLUE
                    current = 2

            elif keys_pressed[pg.K_DOWN]:
                if current == 0:
                    default_color = WHITE
                    biden_color = BLUE
                    current = 1
                elif current == 1:
                    biden_color = WHITE
                    trump_color = BLUE
                    current = 2

                elif current == 2:
                    trump_color = WHITE
                    back_color = BLUE
                    current = 3

                elif current == 3:
                    back_color = WHITE
                    default_color = BLUE
                    current = 0

            elif keys_pressed[pg.K_RETURN]:
                # TODO: add point sprite change here
                if current == 0:
                    self.icon = "pacman"

                elif current == 1:
                    self.icon = "biden"
                    self.point_sprite = "biden"

                elif current == 2:
                    self.icon = "trump"
                    self.point_sprite = "trump"

                elif current == 3:
                    break


            self.clock.tick(10)
            pg.display.update()






    def loadMenu(self):
        pg.mixer.Sound.play(self.intro_sound)
        # Set current selection
        current = 0
        play_color = BLUE
        leaderboard_color = WHITE
        settings_color = WHITE
        quit_color = WHITE
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    break

            self.disp.blit(self.background, (0, 0))

            self.disp.blit(pg.image.load('pacman/Pacman3.png'), (510, 165))

            text = self.FONT_LARGE.render('Pac-Man', False, YELLOW)
            self.disp.blit(text, (570, 170))

            text = self.FONT.render('PLAY', False, play_color)
            self.disp.blit(text, (590, 250))

            text = self.FONT.render('LEADERBOARD', False, leaderboard_color)
            self.disp.blit(text, (540, 300))

            text = self.FONT.render('SETTINGS', False, settings_color)
            self.disp.blit(text, (560, 350))

            text = self.FONT.render('QUIT', False, quit_color)
            self.disp.blit(text, (590, 400))

            keys_pressed = pg.key.get_pressed()
            if keys_pressed[pg.K_ESCAPE]:
                quit()

            elif keys_pressed[pg.K_UP]:
                if current == 0:
                    play_color = WHITE
                    quit_color = BLUE
                    current = 3

                elif current == 1:
                    leaderboard_color = WHITE
                    play_color = BLUE
                    current = 0

                elif current == 2:
                    settings_color = WHITE
                    leaderboard_color = BLUE
                    current = 1

                elif current == 3:
                    quit_color = WHITE
                    settings_color = BLUE
                    current = 2

            elif keys_pressed[pg.K_DOWN]:
                if current == 0:
                    play_color = WHITE
                    leaderboard_color = BLUE
                    current = 1
                elif current == 1:
                    leaderboard_color = WHITE
                    settings_color = BLUE
                    current = 2

                elif current == 2:
                    settings_color = WHITE
                    quit_color = BLUE
                    current = 3

                elif current == 3:
                    quit_color = WHITE
                    play_color = BLUE
                    current = 0

            elif keys_pressed[pg.K_RETURN]:
                if current == 0:
                    break
                elif current == 1:
                    # TODO: implement firebase leaderboard
                    print('leaderboard selected')
                    break
                elif current == 2:
                    self.loadSettings()
                elif current == 3:
                    quit()


            self.clock.tick(10)
            pg.display.update()

        if current == 0:
            g.runLevel()


if __name__ == '__main__':
    g = Game()
    g.loadMenu()


