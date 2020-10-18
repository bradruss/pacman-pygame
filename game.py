import pacman
import ghost
import pygame as pg

# TODO: to load sprite animation, use a for loop to load frames (different images)
window_height = 600
window_width = 1200
def main():
    # Initialize window
    pg.init()
    disp = pg.display.set_mode((window_width,window_height))
    pg.display.set_caption("Pac-man")

    clock = pg.time.Clock()
    pacman_sprite = [pg.image.load('pacman/Pacman.png'), pg.image.load('pacman/Pacman2.png'), pg.image.load('pacman/Pacman3.png')]

    # Load background
    background = pg.image.load('background.jpg')

    # Load pacman
    #sprite_image_original = pg.image.load("pacman.png").convert_alpha()
    # Set rotation and zoom scale
    #sprite_image = pg.transform.rotozoom(sprite_image_original,0,.1)

    # Display background
    disp.blit(background, (0, 0))

    # Set initial Pacman point
    x = 100
    y = 100
    pacman_image = 0
    rotation = 0
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
            if y >= 5:
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

            if y <= 460:
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
            if x >= 5:
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
            if x <= 1075:
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

        # 30 fps
        clock.tick(30)
        pg.display.update()



if __name__ == '__main__':
    main()