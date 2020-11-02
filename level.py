import pacman
# import ghost
import pygame as pg
import corridorH as ch
import corridorV as cv


#width of the corridors
WIDTH = 50

class Level:
    def __init__(self, filename):
        self.filename = filename
        self.points = 0
        self.win = False
        self.c_map = {}
        # loads in file to dictionary c_map
        self.file_reader()

    def file_reader(self):
        f = open(self.filename, "r")
        # loops through file to load in coordinates for either a horizontal or vertical corridor
        for x in f:
            curr_line = x
            array = curr_line.split(',')
            if array[0] == 'H':
                cor = ch.CorridorH(0,0,0)
                cor.x_startt = int(array[2])
                cor.x_startb = int(array[3])
                cor.y_start = int(array[4])
                cor.x_endt = int(array[5])
                cor.x_endb = int(array[6])
                cor.y_end = int(array[7])
                self.c_map[array[1]] = cor

            if array[0] == 'V':
                cor = cv.CorridorV(0, 0, 0)
                cor.x_start = int(array[2])
                cor.y_startl = int(array[3])
                cor.y_startr = int(array[4])
                cor.x_end = int(array[5])
                cor.y_endl = int(array[6])
                cor.y_endr = int(array[7])
                self.c_map[array[1]] = cor

        print("Level File Loaded In")
        f.close()


    # draws the level to display
    def draw_level(self, disp):
        for key in self.c_map:
            self.c_map[key].draw(disp)
        pg.display.flip()

    # checks to see if the inputted x and y coordinates of pacman are a "valid" move so that pacman
    # doesn't go through the walls of the map. Checks this by seeing if pacman will run into any of the
    # lines drawn to the display. Loops through every corridor and checks if pacman will run into the lines
    # of that particular corridor

    def check_valid(self, x, y):
        midx = x + WIDTH/2
        midy = y + WIDTH/2
        left_edge = x # This is the left edge of pacman
        right_edge = x + WIDTH # This is the right edge of pacman
        top_edge = y # This is the top edge of pacman
        bottom_edge = y + WIDTH  # This is the bottom edge of pacman
        valid = True # Flag that checks if pacman is in a valid position
        test_num = 0
        # This will check if the x and y coordinates inputted puts pacman in a valid position
        for key in self.c_map:
            cor = self.c_map[key]
            # The approach to checking is to see if Pacman will pass through any of the lines drawn on screen
            if type(cor) is cv.CorridorV:

                # make sure pacman's edges aren't passing through any of the lines
                # check the left line of the vertical corridor
                print("check left of " + key)
                if left_edge < cor.x_start < right_edge and ((cor.y_startl < top_edge or cor.y_startl < bottom_edge) and (cor.y_endl > bottom_edge or cor.y_endl > top_edge)):
                    valid = False
                    print("rule 1")

                # check the right line of the vertical corridor
                print("check right of " + key)
                if left_edge < cor.x_end < right_edge and ((cor.y_startr < top_edge or cor.y_startr < bottom_edge) and (cor.y_endr > bottom_edge or cor.y_endr > top_edge)):
                    valid = False
                    print("rule 2")

            if type(cor) is ch.CorridorH:
                # check the top line of the horizontal corridor
                print("check top of " + key)
                if top_edge < cor.y_start < bottom_edge and ((cor.x_startt < left_edge or cor.x_startt < right_edge) and (cor.x_endt > right_edge or cor.x_endt > left_edge)):
                    valid = False
                    print("rule 3")
                # check the bottom line of the horizontal corridor
                print("check bottom of " + key)
                if top_edge < cor.y_end < bottom_edge and ((cor.x_startb < left_edge or cor.x_startb < right_edge) and (cor.x_endb > right_edge or cor.x_endb > left_edge)):
                    valid = False
                    print("rule 4")

        return valid



