from pacman import Pacman
from ghost import Ghost
import pygame as pg
import level
import copy
from leaderboard import Leaderboard
import os.path
from os import path

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
        self.max_level = 5
        self.icon = ""
        self.point_sprite = ""
        self.has_loaded_leader_board = False

        # Load points/coins map
        self.point_map = copy.deepcopy(self.current_level.p_map)
        print(self.point_map)

        # Initialize window
        pg.init()
        self.disp = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Fonts
        self.FONT = pg.font.Font('joystix.monospace.ttf', 20)
        self.FONT_LARGE = pg.font.Font('joystix.monospace.ttf', 30)

        # Set window title
        pg.display.set_caption("Pac-Man")

        # Create timer for frames
        self.clock = pg.time.Clock()

        # Hearts
        self.heart_sprite = pg.image.load('heart.png')

        # Window icon
        pg.display.set_icon(pg.image.load('pacman/Pacman3.png'))

        # Is the sprite in motion?
        self.in_motion = False
        self.play_waka = False
        self.motion_type = None
        self.red_ghost = Ghost("red", self.level)
        self.blue_ghost = Ghost("blue", self.level)
        self.orange_ghost = Ghost("orange", self.level)
        self.pink_ghost = Ghost("pink", self.level)
        self.red_move = False
        self.blue_move = False
        self.orange_move = False
        self.pink_move = False
        self.dead_ghosts = []

        self.powerup_iterations = 0

        # Load background
        self.background = pg.image.load('background.jpg')

        # Display the background image
        self.disp.blit(self.background, (0, 0))

        # Sounds
        self.intro_sound = pg.mixer.Sound("Sound/intro.wav")
        self.intro_sound.set_volume(0.2)
        self.death_sound = pg.mixer.Sound("Sound/death.wav")
        self.death_sound.set_volume(0.2)

        # Load leaderboard and intro sound
        self.leaderboard = Leaderboard()
        pg.mixer.Sound.play(self.intro_sound)

    # Lets users load in custom level to play
    def load_player_level(self):
        text = self.FONT.render('Please Type Valid File Name In Terminal', False, WHITE)
        for i in range(0, 3):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    break
            self.disp.blit(self.background, (0, 0))
            self.disp.blit(text, (280, 300))
            self.clock.tick(30)
            pg.display.update()

        file_exists = False
        file_path = None
        while not file_exists:
            print("Please Enter a Valid Level File, or type in 'quit' to exit")
            file_path = input(": ")
            if file_path == "quit":
                return 0
            file_exists = path.exists(file_path)
            if not file_exists:
                continue
            curr_level_check = level.Level(file_path)
            if curr_level_check.file_reader() == -1:
                file_exists = False

        self.current_level_int = 5
        text = self.FONT.render('Player Created Level', False, WHITE)
        for i in range(0, 50):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    break
            self.disp.blit(self.background, (0, 0))
            self.disp.blit(text, (500, 300))
            self.clock.tick(30)
            pg.display.update()

        current_level_str = file_path
        self.level = current_level_str
        self.current_level = level.Level(self.level)
        self.point_map = copy.deepcopy(self.current_level.p_map)

        # update ghosts' levels
        self.red_ghost.current_level = self.current_level
        self.blue_ghost.current_level = self.current_level
        self.orange_ghost.current_level = self.current_level
        self.pink_ghost.current_level = self.current_level

        self.run_level()

        return 0

    # Loads the next level
    def load_new_level(self):
        # If there is another level to load in
        if 0 < self.current_level_int < self.max_level:
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

            # update ghosts' levels
            self.red_ghost.current_level = self.current_level
            self.blue_ghost.current_level = self.current_level
            self.orange_ghost.current_level = self.current_level
            self.pink_ghost.current_level = self.current_level

            return 0
        # If its the last level
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
            self.submit_score()
            return -1

    # Method for red ghost movement
    def red_ghost_move(self, num_iterations, x, y):
        # If just reset
        if num_iterations < 0:
            pass
        else:
            # If ghost is vulnerable
            if self.red_ghost.weak:
                self.red_ghost.move_random_slow()

            # If invulnerable
            else:
                if self.red_ghost.chase_iterations <= 200 and self.red_ghost.chase_iterations != -1:
                    self.red_ghost.move_chase(x, y)
                    self.red_ghost.chase_iterations += 1
                    if self.red_ghost.chase_iterations > 200:
                        self.red_ghost.chase_iterations = -1
                        self.red_ghost.random_iterations = 0

                if self.red_ghost.random_iterations <= 150 and self.red_ghost.random_iterations != -1:
                    self.red_ghost.move_random()
                    self.red_ghost.random_iterations += 1
                    if self.red_ghost.random_iterations > 150:
                        self.red_ghost.random_iterations = -1
                        self.red_ghost.chase_iterations = 0

    # Orange ghost movement method
    def orange_ghost_move(self, num_iterations, x, y):
        # Do nothing
        if num_iterations < 500:
            pass

        # After 500 iterations, spawn
        elif num_iterations == 500:
            self.orange_ghost.spawn_outside()

        else:
            if self.orange_ghost.weak:
                self.orange_ghost.move_random_slow()
            else:
                if self.orange_ghost.chase_iterations <= 200 and self.orange_ghost.chase_iterations != -1:
                    self.orange_ghost.move_chase(x, y)
                    self.orange_ghost.chase_iterations += 1
                    if self.orange_ghost.chase_iterations > 200:
                        self.orange_ghost.chase_iterations = -1
                        self.orange_ghost.random_iterations = 0

                if self.orange_ghost.random_iterations <= 150 and self.orange_ghost.random_iterations != -1:
                    self.orange_ghost.move_random()
                    self.orange_ghost.random_iterations += 1
                    if self.orange_ghost.random_iterations > 150:
                        self.orange_ghost.random_iterations = -1
                        self.orange_ghost.chase_iterations = 0

    # Blue ghost movement method
    def blue_ghost_move(self, num_iterations, x, y):
        # Do nothing for 999 iterations
        if num_iterations < 1000:
            pass

        # After 1000 iterations, spawn
        elif num_iterations == 1000:
            self.blue_ghost.spawn_outside()

        else:
            if self.blue_ghost.weak:
                self.blue_ghost.move_random_slow()
            else:
                if self.blue_ghost.chase_iterations <= 200 and self.blue_ghost.chase_iterations != -1:
                    self.blue_ghost.move_chase(x, y)
                    self.blue_ghost.chase_iterations += 1
                    if self.blue_ghost.chase_iterations > 200:
                        self.blue_ghost.chase_iterations = -1
                        self.blue_ghost.random_iterations = 0

                if self.blue_ghost.random_iterations <= 150 and self.blue_ghost.random_iterations != -1:
                    self.blue_ghost.move_random()
                    self.blue_ghost.random_iterations += 1
                    if self.blue_ghost.random_iterations > 150:
                        self.blue_ghost.random_iterations = -1
                        self.blue_ghost.chase_iterations = 0

    # Pink ghost movement method
    def pink_ghost_move(self, num_iterations, x, y):
        if num_iterations < 1500:
            pass

        # Spawn after 1500 iterations
        elif num_iterations == 1500:
            self.pink_ghost.spawn_outside()

        else:
            if self.pink_ghost.weak:
                self.pink_ghost.move_random_slow()
            else:
                if self.pink_ghost.chase_iterations <= 200 and self.pink_ghost.chase_iterations != -1:
                    self.pink_ghost.move_chase(x, y)
                    self.pink_ghost.chase_iterations += 1
                    if self.pink_ghost.chase_iterations > 200:
                        self.pink_ghost.chase_iterations = -1
                        self.pink_ghost.random_iterations = 0

                if self.pink_ghost.random_iterations <= 150 and self.pink_ghost.random_iterations != -1:
                    self.pink_ghost.move_random()
                    self.pink_ghost.random_iterations += 1
                    if self.pink_ghost.random_iterations > 150:
                        self.pink_ghost.random_iterations = -1
                        self.pink_ghost.chase_iterations = 0

    # Checks for pac man death based on x and y positions
    def check_death(self, x, y):
        if not self.red_ghost.weak and self.red_ghost.check_death(x, y):
            return True
        elif not self.blue_ghost.weak and self.blue_ghost.check_death(x, y):
            return True
        elif not self.orange_ghost.weak and self.orange_ghost.check_death(x, y):
            return True
        elif not self.pink_ghost.weak and self.pink_ghost.check_death(x, y):
            return True
        else:
            return False

    # Checks for ghost death based on x and y positions
    def check_ghost_death(self, x, y):
        return_val = False
        if self.red_ghost.weak and self.red_ghost.check_death(x, y):
            return_val = True
            self.dead_ghosts.append(self.red_ghost)

        if self.blue_ghost.weak and self.blue_ghost.check_death(x, y):
            return_val = True
            self.dead_ghosts.append(self.blue_ghost)

        if self.orange_ghost.weak and self.orange_ghost.check_death(x, y):
            return_val = True
            self.dead_ghosts.append(self.orange_ghost)

        if self.pink_ghost.weak and self.pink_ghost.check_death(x, y):
            return_val = True
            self.dead_ghosts.append(self.orange_ghost)

        return return_val

    # Loads the game
    def run_level(self):
        """
        Run the pacman game
        """
        self.pacman = Pacman(self.icon)
        self.pacman.num_coins = 0
        self.remove_power_up_state()
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
        is_left = False

        # Used for displaying ghosts
        new_game = True

        # music stuff
        channel = pg.mixer.Channel(1)

        while True:
            # Display pacman and background
            self.disp.blit(self.background, (0, 0))
            self.load_lives()
            self.load_score()
            self.load_level_text()

            if new_game:
                # put ghosts at fixed pos
                self.red_ghost.spawn_outside()
                self.disp.blit(self.red_ghost.sprite, (self.red_ghost.x_pos, self.red_ghost.y_pos))

                self.blue_ghost.spawn_left()
                self.disp.blit(self.blue_ghost.sprite, (self.blue_ghost.x_pos, self.blue_ghost.y_pos))

                self.pink_ghost.spawn_middle()
                self.disp.blit(self.pink_ghost.sprite, (self.pink_ghost.x_pos, self.pink_ghost.y_pos))

                self.orange_ghost.spawn_right()
                self.disp.blit(self.orange_ghost.sprite, (self.orange_ghost.x_pos, self.orange_ghost.y_pos))

            else:
                # put ghosts at their respective positions
                self.disp.blit(self.red_ghost.sprite, (self.red_ghost.x_pos, self.red_ghost.y_pos))
                self.disp.blit(self.blue_ghost.sprite, (self.blue_ghost.x_pos, self.blue_ghost.y_pos))
                self.disp.blit(self.pink_ghost.sprite, (self.pink_ghost.x_pos, self.pink_ghost.y_pos))
                self.disp.blit(self.orange_ghost.sprite, (self.orange_ghost.x_pos, self.orange_ghost.y_pos))

            new_game = False

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    break
            # Plays waka sound if pacman is moving
            if self.in_motion:
                keys_pressed = pg.key.get_pressed()
                if not channel.get_busy():
                    channel.play(self.pacman.waka)

                # Displays pacman movement with rotations
                if keys_pressed[pg.K_UP] and self.current_level.check_valid(x, y - 5) and self.motion_type != "up":
                    self.motion_type = "up"
                    self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))

                elif keys_pressed[pg.K_DOWN] and self.current_level.check_valid(x,
                                                                                y + 5) and self.motion_type != "down":
                    self.motion_type = "down"
                    self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))

                elif keys_pressed[pg.K_RIGHT] and self.current_level.check_valid(x + 5,
                                                                                 y) and self.motion_type != "right":
                    self.motion_type = "right"
                    self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))

                elif keys_pressed[pg.K_LEFT] and self.current_level.check_valid(x - 5,
                                                                                y) and self.motion_type != "left":
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
                        is_left = False
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
                        is_left = False
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

                        is_left = True

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
                        is_left = False
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[pacman_image], rotation), (x, y))
                    else:
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))
                        self.in_motion = False

                else:
                    self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))
                    self.in_motion = False
            else:
                # If pacman isnt in motion
                channel.stop()
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
                        is_left = False
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
                        is_left = False
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

                        is_left = True

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
                        is_left = False
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[pacman_image], rotation), (x, y))
                    else:
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[previous_pacman_image], rotation), (x, y))

                elif keys_pressed[pg.K_ESCAPE]:
                    quit()

                else:
                    # Dont set rotation - occurs when key left
                    if is_left:
                        temp = pg.transform.flip(pg.transform.rotate(self.pacman.sprite[pacman_image], 0), True, False)
                        self.disp.blit(temp, (x, y))

                    # Set rotation - occurs when key up, down, and right
                    else:
                        self.disp.blit(pg.transform.rotate(self.pacman.sprite[pacman_image], rotation), (x, y))

            self.check_points(x, y)
            self.current_level.draw_level(self.disp, self.point_map, self.point_sprite, self.current_level_int)

            # Movement For the Ghosts
            if self.red_ghost.death_iterations > 100:
                self.red_ghost.dead = False
                self.red_ghost.death_iterations = 0
                self.red_ghost.spawn_outside()
            elif self.red_ghost.dead:
                self.red_ghost.death_iterations += 1
            else:
                self.red_ghost_move(self.num_iterations, x, y)

            if self.blue_ghost.death_iterations > 100:
                self.blue_ghost.dead = False
                self.blue_ghost.death_iterations = 0
                self.blue_ghost.spawn_outside()
            elif self.blue_ghost.dead:
                self.blue_ghost.death_iterations += 1
            else:
                self.blue_ghost_move(self.num_iterations, x, y)

            if self.orange_ghost.death_iterations > 100:
                self.orange_ghost.dead = False
                self.orange_ghost.death_iterations = 0
                self.orange_ghost.spawn_outside()
            elif self.orange_ghost.dead:
                self.orange_ghost.death_iterations += 1
            else:
                self.orange_ghost_move(self.num_iterations, x, y)

            if self.pink_ghost.death_iterations > 100:
                self.pink_ghost.dead = False
                self.pink_ghost.death_iterations = 0
                self.pink_ghost.spawn_outside()
            elif self.pink_ghost.dead:
                self.pink_ghost.death_iterations += 1
            else:
                self.pink_ghost_move(self.num_iterations, x, y)

            # 30 fps
            self.clock.tick(30)

            pg.display.update()

            print(self.powerup_iterations)

            # If pac man dies
            if self.check_death(x, y):
                pg.mixer.Sound.play(self.death_sound)
                self.show_death(rotation, x, y)
                self.pacman.set_num_lives(self.pacman.num_lives - 1)

                if self.pacman.num_lives == 0:
                    self.game_over()
                    break

                else:
                    self.red_ghost.reset_ghost()
                    self.blue_ghost.reset_ghost()
                    self.orange_ghost.reset_ghost()
                    self.pink_ghost.reset_ghost()
                    self.red_ghost.not_vulnerable()
                    self.blue_ghost.not_vulnerable()
                    self.orange_ghost.not_vulnerable()
                    self.pink_ghost.not_vulnerable()
                    self.pacman_respawn()
                    self.num_iterations = 0
                    self.powerup_iterations = 0
                    rotation = 0
                    x = 0
                    y = 50

            # If a ghost has died, reset it to invulnerable
            if self.check_ghost_death(x, y):
                for i in range(0, len(self.dead_ghosts)):
                    self.pacman.num_coins += 30
                    curr_ghost = self.dead_ghosts[i]
                    color = curr_ghost.color
                    if color == 'red':
                        curr_ghost.spawn_middle_back()
                        curr_ghost.dead = True
                        curr_ghost.not_vulnerable()
                        self.dead_ghosts.remove(curr_ghost)
                    if color == 'blue':
                        curr_ghost.spawn_left()
                        curr_ghost.dead = True
                        curr_ghost.not_vulnerable()
                        self.dead_ghosts.remove(curr_ghost)
                    if color == 'orange':
                        curr_ghost.spawn_right()
                        curr_ghost.dead = True
                        curr_ghost.not_vulnerable()
                        self.dead_ghosts.remove(curr_ghost)
                    if color == 'pink':
                        curr_ghost.spawn_middle()
                        curr_ghost.dead = True
                        curr_ghost.not_vulnerable()
                        self.dead_ghosts.remove(curr_ghost)

            if len(self.point_map) == 0:
                return_val = self.load_new_level()
                self.red_ghost.reset_ghost()
                self.blue_ghost.reset_ghost()
                self.orange_ghost.reset_ghost()
                self.pink_ghost.reset_ghost()
                self.red_ghost.not_vulnerable()
                self.blue_ghost.not_vulnerable()
                self.orange_ghost.not_vulnerable()
                self.pink_ghost.not_vulnerable()
                self.pacman_respawn()
                self.num_iterations = 0
                self.powerup_iterations = 0
                rotation = 0
                x = 0
                y = 50
                if return_val == -1:
                    break

            # check the powerup iterations to time powerup
            if self.powerup_iterations > 700 and self.pacman.is_dangerous:
                self.red_ghost.not_vulnerable()
                self.blue_ghost.not_vulnerable()
                self.orange_ghost.not_vulnerable()
                self.pink_ghost.not_vulnerable()
                self.powerup_iterations = 0
                self.pacman.is_dangerous = False
            elif self.pacman.is_dangerous:
                self.powerup_iterations += 1

            self.num_iterations += 1

            # Pacman pos debugging
            # print("x is " + str(x) + " and y is " + str(y))

        # Close leaderboard file
        if self.leaderboard.file is not None:
            self.leaderboard.file.close()

    # Respawn pacman to the top left of the map and ghosts
    def pacman_respawn(self):
        # Set initial Pacman point
        x = 0
        y = 50

        # Pacman sprite array index
        pacman_image = 0

        # Rotation in degrees
        rotation = 0

        for i in range(0, 64):
            self.disp.blit(self.background, (0, 0))
            self.load_lives()
            self.load_score()
            self.load_level_text()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    break

            self.disp.blit(pg.transform.rotate(self.pacman.sprite[pacman_image], rotation), (x, y))
            self.current_level.draw_level(self.disp, self.point_map, self.point_sprite, self.current_level_int)

            # put ghosts at fixed pos
            self.red_ghost.spawn_outside()
            self.disp.blit(self.red_ghost.sprite, (self.red_ghost.x_pos, self.red_ghost.y_pos))

            self.blue_ghost.spawn_left()
            self.disp.blit(self.blue_ghost.sprite, (self.blue_ghost.x_pos, self.blue_ghost.y_pos))

            self.pink_ghost.spawn_middle()
            self.disp.blit(self.pink_ghost.sprite, (self.pink_ghost.x_pos, self.pink_ghost.y_pos))

            self.orange_ghost.spawn_right()
            self.disp.blit(self.orange_ghost.sprite, (self.orange_ghost.x_pos, self.orange_ghost.y_pos))

            self.clock.tick(30)
            pg.display.update()

    # Plays the death animation
    def show_death(self, rotation, x, y):

        self.disp.blit(pg.transform.rotate(self.pacman.death[0 // 10], rotation), (x, y))

        for i in range(0, 64):
            # Display pacman and background
            self.disp.blit(self.background, (0, 0))
            self.load_lives()
            self.load_score()
            self.load_level_text()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    break

            self.disp.blit(self.red_ghost.sprite, (self.red_ghost.x_pos, self.red_ghost.y_pos))
            self.disp.blit(self.blue_ghost.sprite, (self.blue_ghost.x_pos, self.blue_ghost.y_pos))
            self.disp.blit(self.pink_ghost.sprite, (self.pink_ghost.x_pos, self.pink_ghost.y_pos))
            self.disp.blit(self.orange_ghost.sprite, (self.orange_ghost.x_pos, self.orange_ghost.y_pos))

            self.disp.blit(pg.transform.rotate(self.pacman.death[i // 8], 0), (x, y))
            self.current_level.draw_level(self.disp, self.point_map, self.point_sprite, self.current_level_int)

            self.clock.tick(30)
            pg.display.update()

    # Sets pacman to invulnerable and ghosts to vulnerable
    def load_power_up_state(self):
        self.pacman.is_dangerous = True

        self.red_ghost.vulnerable()
        self.blue_ghost.vulnerable()
        self.pink_ghost.vulnerable()
        self.orange_ghost.vulnerable()

    # Sets pacman to vulnerable state and ghosts to invulnerable
    def remove_power_up_state(self):
        self.pacman.is_dangerous = False
        self.red_ghost.not_vulnerable()
        self.blue_ghost.not_vulnerable()
        self.pink_ghost.not_vulnerable()
        self.orange_ghost.not_vulnerable()

    # Checks for pacman point collision
    def check_points(self, x, y):
        midx = x + WIDTH / 2
        midy = y + WIDTH / 2

        if (midx, midy) in self.point_map:

            if self.point_map[(midx, midy)].is_power_up == True:
                self.load_power_up_state()
            del self.point_map[(midx, midy)]
            # print("point removed")
            self.pacman.collect_coin()

        if (midx + (5 - (midx % 5)), midy) in self.point_map:
            if self.point_map[(midx + (5 - (midx % 5)), midy)].is_power_up == True:
                self.load_power_up_state()
            del self.point_map[(midx + (5 - (midx % 5)), midy)]
            self.pacman.collect_coin()

        if (midx, midy + (5 - (midx % 5))) in self.point_map:
            if self.point_map[(midx, midy + (5 - (midx % 5)))].is_power_up == True:
                self.load_power_up_state()
            del self.point_map[(midx, midy + (5 - (midx % 5)))]
            self.pacman.collect_coin()

    # Loads the submit score menu
    def submit_score(self):
        text = ""
        flag = True
        while flag:
            self.disp.blit(self.background, (0, 0))
            text1 = self.FONT.render('Type your initials', False, WHITE)
            self.disp.blit(text1, (460, 150))

            text1 = self.FONT.render('Press enter when finished', False, WHITE)
            self.disp.blit(text1, (420, 200))

            pg.draw.line(self.disp, WHITE, (540, 290), (650, 290), 3)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    break

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        text = text.upper()
                        temp1 = []
                        temp1.append(text)
                        temp1.append(self.pacman.num_coins)
                        self.leaderboard.update_leaderboard(temp1)
                        self.has_loaded_leader_board = True
                        flag = False

                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        # Prevents users from submitting more than 3 letters/symbols
                        if len(text) < 3:
                            text += event.unicode

            text1 = self.FONT_LARGE.render(text, False, YELLOW)
            self.disp.blit(text1, (560, 250))

            self.clock.tick(10)
            pg.display.update()

        g.load_menu()

    # Loads the game over screen
    def game_over(self):
        current = 0
        play_again_color = BLUE
        submit_color = WHITE
        quit_color = WHITE

        while True:
            self.disp.blit(self.background, (0, 0))
            text = self.FONT_LARGE.render('Game Over', False, WHITE)
            self.disp.blit(text, (490, 150))

            text = self.FONT.render("Total Score:", False, WHITE)
            self.disp.blit(text, (510, 225))

            text = self.FONT.render(str(self.pacman.num_coins), False, WHITE)
            self.disp.blit(text, (560, 260))

            text = self.FONT.render('PLAY AGAIN?', False, play_again_color)
            self.disp.blit(text, (510, 310))

            text = self.FONT.render('SUBMIT SCORE', False, submit_color)
            self.disp.blit(text, (500, 350))

            text = self.FONT.render('QUIT', False, quit_color)
            self.disp.blit(text, (550, 400))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    break

            keys_pressed = pg.key.get_pressed()
            if keys_pressed[pg.K_ESCAPE]:
                quit()

            # Changes the text to blue when selected
            elif keys_pressed[pg.K_UP]:
                if current == 0:
                    play_again_color = WHITE
                    quit_color = BLUE
                    current = 2

                elif current == 1:
                    submit_color = WHITE
                    play_again_color = BLUE
                    current = 0

                elif current == 2:
                    quit_color = WHITE
                    submit_color = BLUE
                    current = 1

            elif keys_pressed[pg.K_DOWN]:
                if current == 0:
                    play_again_color = WHITE
                    submit_color = BLUE
                    current = 1

                elif current == 1:
                    submit_color = WHITE
                    quit_color = BLUE
                    current = 2

                elif current == 2:
                    quit_color = WHITE
                    play_again_color = BLUE
                    current = 0

            # Processes selection
            elif keys_pressed[pg.K_RETURN]:
                # Play again
                if current == 0:
                    break

                # Submit score
                elif current == 1:
                    self.submit_score()

                # Quit
                elif current == 2:
                    quit()

            self.clock.tick(10)
            pg.display.update()

        g.run_level()
        return 0

    # Loads the lives on screen
    def load_lives(self):
        x = 950
        y = 0

        text = self.FONT.render('LIVES', False, WHITE)
        self.disp.blit(text, (850, 5))

        semi_colon = self.FONT.render(':', False, WHITE)
        self.disp.blit(semi_colon, (930, 7))

        for i in range(self.pacman.num_lives):
            temp = pg.transform.scale(self.heart_sprite, (30, 30))
            self.disp.blit(temp, (x, y))
            x += 30

    # Loads the total score number visually
    def load_score(self):
        coins = self.pacman.get_num_coins()

        text = self.FONT.render('SCORE', False, WHITE)
        self.disp.blit(text, (500, 5))

        text2 = ':'
        text_semi = self.FONT.render(text2, False, WHITE)
        self.disp.blit(text_semi, (580, 7))

        text3 = str(coins)
        text_score = self.FONT.render(text3, False, WHITE)
        self.disp.blit(text_score, (600, 5))

    # Loads the level number visually
    def load_level_text(self):
        # Updates game with current level rendered
        text = self.FONT.render('LEVEL', False, WHITE)
        self.disp.blit(text, (350, 5))

        semi_colon = self.FONT.render(':', False, WHITE)
        self.disp.blit(semi_colon, (430, 7))

        text2 = self.FONT.render(str(self.current_level_int), False, WHITE)
        self.disp.blit(text2, (450, 5))

    # Loads the settings page
    def load_settings(self):
        current = 0
        # Load previous setting
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

            # Highlights current selection in blue
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

            # Change pacman sprites, ghost sprites and points sprites
            elif keys_pressed[pg.K_RETURN]:
                if current == 0:
                    self.icon = "pacman"
                    print("pacman selected")
                    break

                elif current == 1:
                    self.icon = "biden"
                    self.point_sprite = "biden"
                    print("biden selected")
                    self.red_ghost.load_trump_ghosts("red")
                    self.blue_ghost.load_trump_ghosts("blue")
                    self.orange_ghost.load_trump_ghosts("orange")
                    self.pink_ghost.load_trump_ghosts("pink")
                    break

                elif current == 2:
                    self.icon = "trump"
                    self.point_sprite = "trump"
                    print("trump selected")
                    self.red_ghost.load_biden_ghosts("red")
                    self.blue_ghost.load_biden_ghosts("blue")
                    self.orange_ghost.load_biden_ghosts("orange")
                    self.pink_ghost.load_biden_ghosts("pink")
                    break

                elif current == 3:
                    break

            self.clock.tick(10)
            pg.display.update()

    # Loads the leaderboard visually
    def load_leader_board(self):
        if self.has_loaded_leader_board == False:
            self.leaderboard.update_top_scores()
            self.has_loaded_leader_board = True
        flag = True
        while flag:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    break

            self.disp.blit(self.background, (0, 0))
            text = self.FONT.render("Name  Score", False, YELLOW)
            self.disp.blit(text, (540, 5))

            text = self.FONT.render('GO BACK (Backspace)', False, BLUE)
            self.disp.blit(text, (570, 570))

            x = 500
            y = 50
            name = ""
            score = ""
            index = 1
            for i in self.leaderboard.top_scores:
                k = 0
                for j in i:
                    if k == 0:
                        name = j
                    else:
                        score = j
                    k += 1
                text = self.FONT.render(str(index) + ". ", False, YELLOW)
                if index >= 10:
                    self.disp.blit(text, (x - 20, y))
                else:
                    self.disp.blit(text, (x, y))
                text = self.FONT.render(name, False, YELLOW)
                self.disp.blit(text, (550, y))

                text = self.FONT.render(str(score), False, YELLOW)
                self.disp.blit(text, (650, y))

                y += 25
                index += 1

            keys_pressed = pg.key.get_pressed()
            if keys_pressed[pg.K_ESCAPE]:
                quit()

            elif keys_pressed[pg.K_BACKSPACE]:
                flag = False

            self.clock.tick(10)
            pg.display.update()

        g.load_menu()

    # Loads the main menu
    def load_menu(self):
        # Set current selection
        current = 0
        play_color = BLUE
        player_level_color = WHITE
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

            text = self.FONT.render('PLAY YOUR OWN LEVEL', False, player_level_color)
            self.disp.blit(text, (475, 300))

            text = self.FONT.render('LEADERBOARD', False, leaderboard_color)
            self.disp.blit(text, (540, 350))

            text = self.FONT.render('SETTINGS', False, settings_color)
            self.disp.blit(text, (560, 400))

            text = self.FONT.render('QUIT', False, quit_color)
            self.disp.blit(text, (590, 450))

            keys_pressed = pg.key.get_pressed()
            if keys_pressed[pg.K_ESCAPE]:
                quit()

            elif keys_pressed[pg.K_UP]:
                if current == 0:
                    play_color = WHITE
                    quit_color = BLUE
                    current = 4

                elif current == 1:
                    player_level_color = WHITE
                    play_color = BLUE
                    current = 0

                elif current == 2:
                    leaderboard_color = WHITE
                    player_level_color = BLUE
                    current = 1

                elif current == 3:
                    settings_color = WHITE
                    leaderboard_color = BLUE
                    current = 2

                elif current == 4:
                    quit_color = WHITE
                    settings_color = BLUE
                    current = 3

            elif keys_pressed[pg.K_DOWN]:
                if current == 0:
                    play_color = WHITE
                    player_level_color = BLUE
                    current = 1

                elif current == 1:
                    player_level_color = WHITE
                    leaderboard_color = BLUE
                    current = 2

                elif current == 2:
                    leaderboard_color = WHITE
                    settings_color = BLUE
                    current = 3

                elif current == 3:
                    settings_color = WHITE
                    quit_color = BLUE
                    current = 4

                elif current == 4:
                    quit_color = WHITE
                    play_color = BLUE
                    current = 0

            elif keys_pressed[pg.K_RETURN]:
                if current == 0:
                    break
                elif current == 1:
                    break
                elif current == 2:
                    self.load_leader_board()
                elif current == 3:
                    self.load_settings()
                elif current == 4:
                    quit()

            self.clock.tick(10)
            pg.display.update()

        if current == 0:
            g.run_level()

        elif current == 1:
            g.load_player_level()


if __name__ == '__main__':
    g = Game()
    g.load_menu()