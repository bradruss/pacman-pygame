"""
Note that this python file is only for developors to develop game levels
NOT for game play users
As of now, not very user-friendly to use
"""

import pygame as pg
import corridorH as ch
import corridorV as cv
import copy
import threading

# Set game size
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1200
WHITE = (255, 255, 255)
WIDTH = 50
iteration_log = []  # keeps track of all changes
curr_map = {}  # dictionary of current map of corridors
iteration_log.append(curr_map)
finished = False


#joins corridors together. Note joins only horizontal and vertical corridors
def join(cor_h,cor_v,join_type):
    copy_h = curr_map[cor_h]
    copy_v = curr_map[cor_v]
    print(curr_map)

    # join at the bottom left
    if (join_type == 'bl'):
        copy_v.y_endr = copy_v.y_endr - WIDTH
        copy_h.x_startt = copy_h.x_startt + WIDTH
    # join at the bottom top left
    elif (join_type == 'tl'):
        copy_v.y_startr = copy_v.y_startr + WIDTH
        copy_h.x_startb = copy_h.x_startb + WIDTH
    # join at the bottom bottom right
    elif (join_type == 'br'):
        copy_v.y_endl = copy_v.y_endl - WIDTH
        copy_h.x_endt = copy_h.x_endt - WIDTH
    # join at top right
    elif (join_type == 'tr'):
        copy_v.y_startl = copy_v.y_startl + WIDTH
        copy_h.x_endb = copy_h.x_endb - WIDTH
    else:
        print("wrong type of join")

    # notifies that join is done and stores the join inside the map
    print("Join done")
    curr_map[cor_h] = copy_h
    curr_map[cor_v] = copy_v
    print(curr_map)


# writes out the level coordinates to a file
def write_out(file_name):
    outF = open(file_name, "w")
    for key in curr_map:
        if type(curr_map[key]) is cv.CorridorV:
            string_out = 'V,' + key + ',' + str(curr_map[key].x_start) + ',' + str(curr_map[key].y_startl + 50) + ',' + str(curr_map[key].y_startr + 50) + ',' + str(curr_map[key].x_end) + ',' + str(curr_map[key].y_endl + 50) + ',' + str(curr_map[key].y_endr + 50) + '\n'
            outF.write(string_out)
        if type(curr_map[key]) is ch.CorridorH:
            string_out = 'H,' + key + ',' + str(curr_map[key].x_startt) + ',' + str(curr_map[key].x_startb) + ',' + str(curr_map[key].y_start + 50) + ',' + str(curr_map[key].x_endt) + ',' + str(curr_map[key].x_endb) + ',' + str(curr_map[key].y_end + 50) + '\n'
            outF.write(string_out)
    outF.close()
    print("DONE WRITING OUT")


def file_reader(filename):
    f = open(filename, "r")
    # loops through file to load in coordinates for either a horizontal or vertical corridor
    for x in f:
        curr_line = x.rstrip('\n')
        a = curr_line.split(',')
        print(a)
        try:
            # Makes a horizontal Hallway and stores it in the map
            if a[1] == 'H':
                curr_map[a[0]] = ch.CorridorH(int(a[2]), int(a[3]), int(a[4]))
                copy_map = copy.deepcopy(curr_map)
                iteration_log.append(copy_map)
            # Makes a vertical hallway and stores it in the map
            elif a[1] == 'V':
                curr_map[a[0]] = cv.CorridorV(int(a[2]), int(a[4]), int(a[5]))
                copy_map = copy.deepcopy(curr_map)
                iteration_log.append(copy_map)
            # Joins two speicfied hallways in the specified way
            elif a[0] == 'join':
                join(a[1], a[2], a[3])
                copy_map = copy.deepcopy(curr_map)
                iteration_log.append(copy_map)
            # Deletes a specified hallway
            elif a[0] == 'delete':
                del curr_map[a[1]]
                copy_map = copy.deepcopy(curr_map)
                iteration_log.append(copy_map)
            # Ends the creation process and stores the level map in a specified file
            elif a[0] == 'done':
                write_out(a[1])
                finished = True
            # Reverts level map back one iteration
            elif a[0] == 'revert':
                print("Im about to revert")
                curr_map.clear()
                temp = copy.deepcopy(iteration_log[len(iteration_log) - 2])
                curr_map.update(temp)
                iteration_log.remove(iteration_log[len(iteration_log) - 1])
            else:
                print("incorrect input")
        except:
            print("exception error incorrect input")


def display_map():
    # Initialize window
    global finished
    pg.init()
    disp = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Set window title
    pg.display.set_caption("Pac-man")

    # Load background
    background = pg.image.load('background.jpg')

    # Display the background image
    disp.blit(background, (0, 0))

    # Manage how fast the screen updates
    clock = pg.time.Clock()

    while not finished:
        # makes it so user can exit out of window and end session
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
        # creates a black background
        disp.fill((0, 0, 0))
        # draws all currently created corridors
        for key in curr_map:
            curr_map[key].draw(disp)
        pg.display.flip()
        # 20 frames per second
        clock.tick(20)
        prompt_user_input()


def prompt_user_input():
    global finished
    while not finished:
        #prompts user for input
        print("Input (name,H or V,start x,end x,start y,end y), or (join,horizontal corridor,vertical corridor,type), (del,corridor), (done,file_name), (revert, now), or (read_file, filename)")
        val = input(": ")
        val = val.replace('(', '')
        val = val.replace(')', '')
        val = val.replace(' ', '')
        a = val.split(',')
        print(a)
        try:
            # Makes a horizontal Hallway and stores it in the map
            if a[1] == 'H':
                curr_map[a[0]] = ch.CorridorH(int(a[2]), int(a[3]), int(a[4]))
                copy_map = copy.deepcopy(curr_map)
                iteration_log.append(copy_map)
            # Makes a vertical hallway and stores it in the map
            elif a[1] == 'V':
                curr_map[a[0]] = cv.CorridorV(int(a[2]), int(a[4]), int(a[5]))
                copy_map = copy.deepcopy(curr_map)
                iteration_log.append(copy_map)
            # Joins two speicfied hallways in the specified way
            elif a[0] == 'join':
                join(a[1], a[2], a[3])
                copy_map = copy.deepcopy(curr_map)
                iteration_log.append(copy_map)
            # Deletes a specified hallway
            elif a[0] == 'delete':
                del curr_map[a[1]]
                copy_map = copy.deepcopy(curr_map)
                iteration_log.append(copy_map)
            # Ends the creation process and stores the level map in a specified file
            elif a[0] == 'done':
                write_out(a[1])
                finished = True
            # Reverts level map back one iteration
            elif a[0] == 'revert':
                print("I'm about to revert")
                curr_map.clear()
                temp = copy.deepcopy(iteration_log[len(iteration_log) - 2])
                curr_map.update(temp)
                iteration_log.remove(iteration_log[len(iteration_log) - 1])
            elif a[0] == 'read_file':
                print("I'm about to read a file")
                file_reader(a[1])
                print("I'm done reading the file")
            else:
                print("incorrect input")
        except:
            print("exception error incorrect input")



def main():
    # # creating thread
    # t1 = threading.Thread(target=display_map, args=())
    # t2 = threading.Thread(target=prompt_user_input, args=())
    #
    # # starting thread 1
    # t1.start()
    # # starting thread 2
    # t2.start()
    #
    # # wait until thread 1 is completely executed
    # t1.join()
    # # wait until thread 2 is completely executed
    # t2.join()
    #
    # # both threads completely executed
    # print("Done!")

    display_map()


if __name__ == '__main__':
    main()
