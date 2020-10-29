import pygame as pg
import corridorH as ch
import corridorV as cv

# Set game size
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1200
WHITE = (255, 255, 255)
WIDTH = 50
c_map = {}

def join(cor_h,cor_v,join_type):
    copy_h = c_map[cor_h]
    copy_v = c_map[cor_v]
    print(c_map)

    if (join_type == 'bl'):
        copy_v.y_endr = copy_v.y_endr - WIDTH
        copy_h.x_startt = copy_h.x_startt + WIDTH
    elif (join_type == 'tl'):
        copy_v.y_startr = copy_v.y_startr + WIDTH
        copy_h.x_startb = copy_h.x_startb + WIDTH
    elif (join_type == 'br'):
        copy_v.y_endl = copy_v.y_endl - WIDTH
        copy_h.x_endt = copy_h.x_endt - WIDTH
    elif (join_type == 'tr'):
        copy_v.y_startl = copy_v.y_startl + WIDTH
        copy_h.x_endb = copy_h.x_endb - WIDTH
    else:
        print("wrong type of join")

    print("Join done")
    c_map[cor_h] = copy_h
    c_map[cor_v] = copy_v
    print(c_map)


def write_out(file_name):
    outF = open(file_name, "w")
    for key in c_map:
        if type(c_map[key]) is cv.CorridorV:
            string_out = 'V,' + key + ',' + str(c_map[key].x_start) + ',' + str(c_map[key].y_startl) + ',' + str(c_map[key].y_startr) + ',' + str(c_map[key].x_end) + ',' + str(c_map[key].y_endl) + ',' + str(c_map[key].y_endr) + '\n'
            outF.write(string_out)
        if type(c_map[key]) is ch.CorridorH:
            string_out = 'H,' + key + ',' + str(c_map[key].x_startt) + ',' + str(c_map[key].x_startb) + ',' + str(c_map[key].y_start) + ',' + str(c_map[key].x_endt) + ',' + str(c_map[key].x_endb) + ',' + str(c_map[key].y_end) + '\n'
            outF.write(string_out)
    outF.close()
    print("DONE WRITING OUT")




def main():
    # Initialize window
    pg.init()
    disp = pg.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    # Set window title
    pg.display.set_caption("Pac-man")

    # Load background
    background = pg.image.load('background.jpg')

    # Display the background image
    disp.blit(background, (0, 0))

    # Manage how fast the screen updates
    clock = pg.time.Clock()

    finished = False

    while not finished:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
        disp.fill((0, 0, 0))
        for key in c_map:
            c_map[key].draw(disp)
        pg.display.flip()
        clock.tick(20)

        print("Input (name,H or V,start x,end x,start y,end y), or (join,horizontal corridor,vertical corridor,type), (del,corridor), or (done,file_name)")
        val = input(": ")
        val = val.replace('(', '')
        val = val.replace(')', '')
        val = val.replace(' ', '')
        a = val.split(',')
        print(a)
        try:
            if a[1] == 'H':
                c_map[a[0]] = ch.CorridorH(int(a[2]), int(a[3]), int(a[4]))
            elif a[1] == 'V':
                c_map[a[0]] = cv.CorridorV(int(a[2]), int(a[4]), int(a[5]))
            elif a[0] == 'join':
                join(a[1], a[2], a[3])
            elif a[0] == 'delete':
                del c_map[a[1]]
            elif a[0] == 'done':
                write_out(a[1])
                finished = True
            else:
                print("incorrect input")
        except:
            print("incorrect input")

        # Display pacman and background



if __name__ == '__main__':
    main()
