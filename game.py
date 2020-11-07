import pacman
from ghost import Ghost
import pygame as pg
import level

# Set game size
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1200


def main():
    # Initialize Level 1
    level_one = level.Level('level1')
    # Initialize window
    pg.init()
    disp = pg.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    # Set window title
    pg.display.set_caption("Pac-man")

    # Create timer for frames
    clock = pg.time.Clock()

    # Pacman sprite array
    pacman_sprite = [pg.image.load('pacman/Pacman.png'), pg.image.load('pacman/Pacman2.png'), pg.image.load('pacman/Pacman3.png')]

    # Load background
    background = pg.image.load('background.jpg')

    # Display the background image
    disp.blit(background, (0, 0))

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
        disp.blit(background,(0,0))

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
            if y >= 5 and level_one.check_valid(x,y-5):
                y -= 5
                if pacman_image < 2:
                    pacman_image += 1
                else:
                    pacman_image = 0

                # Rotate Pacman 90 degrees
                rotation = 90
                isLeft = False
                disp.blit(pg.transform.rotate(pacman_sprite[pacman_image],rotation),(x,y))

        elif keys_pressed[pg.K_DOWN]:

            if y <= 460 and level_one.check_valid(x,y+5):
                y += 5
                if pacman_image < 2:
                    pacman_image += 1
                else:
                    pacman_image = 0

                # Rotate Pacman -90 degrees
                rotation = -90
                isLeft = False
                disp.blit(pg.transform.rotate(pacman_sprite[pacman_image],rotation),(x,y))

        elif keys_pressed[pg.K_LEFT]:
            if x >= 5 and level_one.check_valid(x-5,y):
                x -= 5
                if pacman_image < 2:
                    pacman_image += 1
                else:
                    pacman_image = 0

                isLeft = True

                # Flip params = (image, X axis flip bool, Y axis flip bool)
                temp = pg.transform.flip(pg.transform.rotate(pacman_sprite[pacman_image],0),True,False)
                disp.blit(temp,(x,y))

        elif keys_pressed[pg.K_RIGHT]:
            if x <= 1075 and level_one.check_valid(x+5,y):
                x += 5
                if pacman_image < 2:
                    pacman_image += 1
                else:
                    pacman_image = 0
                rotation = 0
                isLeft = False
                disp.blit(pg.transform.rotate(pacman_sprite[pacman_image],rotation),(x,y))

        elif keys_pressed[pg.K_ESCAPE]:
            quit()

        else:
            # Dont set rotation - occurs when key left
            if isLeft:
                temp = pg.transform.flip(pg.transform.rotate(pacman_sprite[pacman_image], 0), True, False)
                disp.blit(temp, (x, y))

            # Set rotation - occurs when key up, down, and right
            else:
                disp.blit(pg.transform.rotate(pacman_sprite[pacman_image],rotation),(x,y))

        level_one.draw_level(disp)
        # 30 fps
        clock.tick(30)
        ghosts = [Ghost ()]
        for g in ghosts:
            disp.blit(g.surface, g.rect)
        pg.display.update()
        print("x is " + str(x) + "and y is " + str(y))


if __name__ == '__main__':
    main()
