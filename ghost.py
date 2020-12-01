import pygame
import random
import level
import copy
import time


class Ghost():
    # Regular Pac-Man ghost sprites
    weak_ghost = pygame.image.load("weakGhost.png")
    images = [pygame.image.load("redGhost.png"), pygame.image.load("blueGhost.png"),
              pygame.image.load("orangeGhost.png"), pygame.image.load("pinkGhost.png")]

    # Trump Sprites
    trump = [pygame.image.load("TrumpGhosts/TrumpGhost.png"), pygame.image.load("TrumpGhosts/GuilianiGhost.png"),
              pygame.image.load("TrumpGhosts/PenceGhost.png"), pygame.image.load("TrumpGhosts/SessionsGhost.png")]
    weak_trump = [pygame.image.load("TrumpGhosts/TrumpGhostWeak.png"), pygame.image.load("TrumpGhosts/GuilianiGhostWeak.png"),
                 pygame.image.load("TrumpGhosts/PenceGhostWeak.png"), pygame.image.load("TrumpGhosts/SessionsGhostWeak.png")]

    # Biden sprites
    biden = [pygame.image.load("BidenGhosts/BidenGhost.png"), pygame.image.load("BidenGhosts/HarrisGhost.png"),
             pygame.image.load("BidenGhosts/ObamaGhost.png"), pygame.image.load("BidenGhosts/SandersGhost.png")]
    weak_biden = [pygame.image.load("BidenGhosts/BidenGhostWeak.png"),
                 pygame.image.load("BidenGhosts/HarrisGhostWeak.png"),
                 pygame.image.load("BidenGhosts/ObamaGhostWeak.png"),
                 pygame.image.load("BidenGhosts/SandersGhostWeak.png")]

    def __init__(self, color, level_num):
        # Color string
        self.color = color

        # Used initially for pac-man ghost creation then altered later if
        # biden or trump is selected
        self.sprite = self.load_ghost(color)
        self.weak = False
        self.x_pos = 0
        self.y_pos = 0
        self.current_level = level.Level(level_num)
        self.current_level_int = 1

        # Point/coins locations
        self.point_map = copy.deepcopy(self.current_level.p_map)

        # Where the ghost is heading
        self.current_direction = None

        # How much time is spent moving a certain way
        self.chase_iterations = 0
        self.random_iterations = -1
        self.death_iterations = 0
        self.dead = False
        # Used for sprite setting -> pacman, biden, or trump
        self.type = "pacman"
        r = random.randint(1, 4)
        if r == 1:
            self.current_direction = "up"
        elif r == 2:
            self.current_direction = "down"
        elif r == 3:
            self.current_direction = "right"
        else:
            self.current_direction = "left"
        loop = 0

    # Resets direction
    def reset_ghost(self):
        self.current_direction = None
        self.chase_iterations = 0
        self.random_iterations = -1
        r = random.randint(1, 4)
        if r == 1:
            self.current_direction = "up"
        elif r == 2:
            self.current_direction = "down"
        elif r == 3:
            self.current_direction = "right"
        else:
            self.current_direction = "left"

    # Loads regular Pacman ghost sprites
    def load_ghost(self, color):
        temp = None
        if color == "red":
            temp = self.images[0]
        elif color == "blue":
            temp = self.images[1]
        elif color == "orange":
            temp = self.images[2]
        elif color == "pink":
            temp = self.images[3]
        else:
            temp = self.images[3]
        return temp

    # Loads Trump ghost sprites
    def load_trump_ghosts(self, color):
        self.type = "trump"
        if color == "red":
            self.sprite = self.trump[0]
        elif color == "blue":
            self.sprite = self.trump[1]
        elif color == "orange":
            self.sprite = self.trump[2]
        elif color == "pink":
            self.sprite = self.trump[3]
        else:
            self.sprite = self.trump[3]

    # Loads weak Trump ghost sprites
    def load_trump_weak_ghosts(self, color):
        if color == "red":
            self.sprite = self.weak_trump[0]
        elif color == "blue":
            self.sprite = self.weak_trump[1]
        elif color == "orange":
            self.sprite = self.weak_trump[2]
        elif color == "pink":
            self.sprite = self.weak_trump[3]
        else:
            self.sprite = self.weak_trump[3]

    # Loads Biden ghost sprites
    def load_biden_ghosts(self, color):
        self.type = "biden"
        if color == "red":
            self.sprite = self.biden[0]
        elif color == "blue":
            self.sprite = self.biden[1]
        elif color == "orange":
            self.sprite = self.biden[2]
        elif color == "pink":
            self.sprite = self.biden[3]
        else:
            self.sprite = self.biden[3]

    # Loads weak Biden ghost sprites
    def load_biden_weak_ghosts(self, color):
        if color == "red":
            self.sprite = self.weak_biden[0]
        elif color == "blue":
            self.sprite = self.weak_biden[1]
        elif color == "orange":
            self.sprite = self.weak_biden[2]
        elif color == "pink":
            self.sprite = self.weak_biden[3]
        else:
            self.sprite = self.weak_biden[3]

    # Resets the ghost back to its invulnerable state
    def not_vulnerable(self):
        if self.type == "biden":
            self.load_biden_ghosts(self.color)
        elif self.type == "trump":
            self.load_trump_ghosts(self.color)
        else:
            self.sprite = self.load_ghost(self.color)
        self.weak = False

        # Resets ghosts from 3 pixel interval (vulnerable) to 5 pixel
        # while checking bounds
        if self.x_pos % 5 != 0:

            possible_right = self.x_pos + (5 - (self.x_pos % 5))
            possible_left = self.x_pos - (self.x_pos % 5)

            if possible_right > 1150 or possible_right < 0:
                self.x_pos = possible_left
            else:
                self.x_pos = possible_right

        if self.y_pos % 5 != 0:
            possible_down = self.y_pos + (5 - (self.y_pos % 5))
            possible_up = self.y_pos - (self.y_pos % 5)

            if possible_down > 550 or possible_down < 0:
                self.y_pos = possible_up
            else:
                self.y_pos = possible_down

    # Sets ghosts to vulnerable state
    def vulnerable(self):
        if self.type == "biden":
            self.load_biden_weak_ghosts(self.color)
        elif self.type == "trump":
            self.load_trump_weak_ghosts(self.color)
        else:
            self.sprite = self.weak_ghost
        self.weak = True

    # Spawns ghost right outside of the box
    def spawn_outside(self):
        # Red ghost uses this when a new level is loaded
        self.x_pos = 600
        self.y_pos = 300

    # Spawns ghost in the left "slot" of the ghost box
    def spawn_left(self):
        self.x_pos = 550
        self.y_pos = 400

    # Spawns ghost in the middle "slot" of the ghost box
    def spawn_middle(self):
        self.x_pos = 600
        self.y_pos = 400

    # Spawns ghost in the right "slot" of the ghost box
    def spawn_right(self):
        self.x_pos = 650
        self.y_pos = 400

    # Spawns ghost in the furthest back "slot"
    def spawn_middle_back(self):
        self.x_pos = 600
        self.y_pos = 450

    # Function to chase pac-man
    def move_chase(self, x, y):
        ver = x - self.x_pos
        hor = y - self.y_pos
        if hor > 0 and self.current_level.check_valid(self.x_pos, self.y_pos + 5):
            self.y_pos += 5
        elif hor < 0 and self.current_level.check_valid(self.x_pos, self.y_pos - 5):
            self.y_pos -= 5
        elif ver > 0 and self.current_level.check_valid(self.x_pos + 5, self.y_pos):
            self.x_pos += 5
        elif ver < 0 and self.current_level.check_valid(self.x_pos - 5, self.y_pos):
            self.x_pos -= 5

    # Ghost randomly moves around the level
    def move_random(self):
        # print(self.current_direction)
        if self.current_direction == "up" and self.current_level.check_valid(self.x_pos, self.y_pos - 5):
            self.y_pos -= 5
        elif self.current_direction == "down" and self.current_level.check_valid(self.x_pos, self.y_pos + 5):
            self.y_pos += 5
        elif self.current_direction == "right" and self.current_level.check_valid(self.x_pos + 5, self.y_pos):
            self.x_pos += 5
        elif self.current_direction == "left" and self.current_level.check_valid(self.x_pos - 5, self.y_pos):
            self.x_pos -= 5

        else:
            r = random.randint(1, 4)
            # test if up is good
            if r == 1 and self.current_level.check_valid(self.x_pos, self.y_pos - 5):
                self.current_direction = "up"
                self.y_pos -= 5
            elif r == 2 and self.current_level.check_valid(self.x_pos, self.y_pos + 5):
                self.current_direction = "down"
                self.y_pos += 5
            elif r == 3 and self.current_level.check_valid(self.x_pos + 5, self.y_pos):
                self.current_direction = "right"
                self.x_pos += 5
            elif r == 4 and self.current_level.check_valid(self.x_pos - 5, self.y_pos):
                self.current_direction = "left"
                self.x_pos -= 5

    # Used for when the ghost is in its vulnerable state -> random movement
    def move_random_slow(self):
        # Check to see if it is currently moving
        if self.current_direction == "up" and self.current_level.check_valid(self.x_pos, self.y_pos - 3):
            self.y_pos -= 3
        elif self.current_direction == "down" and self.current_level.check_valid(self.x_pos, self.y_pos + 3):
            self.y_pos += 3
        elif self.current_direction == "right" and self.current_level.check_valid(self.x_pos + 3, self.y_pos):
            self.x_pos += 3
        elif self.current_direction == "left" and self.current_level.check_valid(self.x_pos - 3, self.y_pos):
            self.x_pos -= 3

        else:
            r = random.randint(1, 4)
            # test if up is good
            if r == 1 and self.current_level.check_valid(self.x_pos, self.y_pos - 3):
                self.current_direction = "up"
                self.y_pos -= 3
            elif r == 2 and self.current_level.check_valid(self.x_pos, self.y_pos + 3):
                self.current_direction = "down"
                self.y_pos += 3
            elif r == 3 and self.current_level.check_valid(self.x_pos + 3, self.y_pos):
                self.current_direction = "right"
                self.x_pos += 3
            elif r == 4 and self.current_level.check_valid(self.x_pos - 3, self.y_pos):
                self.current_direction = "left"
                self.x_pos -= 3

    # Checks collision for death
    def check_death(self, x, y):
        if (self.x_pos <= (x + 25) <= self.x_pos + 50) and (self.y_pos <= (y + 25) <= self.y_pos + 50):
            return True

        else:
            return False
