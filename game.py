import pygame as pg

# TODO: to load sprite animation, use a for loop to load frames (different images)

def main():
    window_height = 600
    window_width = 1200
    pg.init()
    disp = pg.display.set_mode((window_width,window_height))
    background = pg.image.load('background.jpg')
    sprite_image_original = pg.image.load("pacman.png").convert_alpha()
    sprite_image = pg.transform.rotozoom(sprite_image_original,0,.1)
    
    disp.blit(background, (0, 0))
    x = 100
    y = 100
    while True:
        disp.blit(background,(0,0))
        disp.blit(sprite_image, (x, y))
        for event in pg.event.get():
            if event.type == pg.K_ESCAPE:
                quit()

            # If key is pressed
            elif event.type == pg.KEYDOWN:
                if event.type == pg.K_UP:
                    print('up button pressed')
                    # make sprite rotate

                elif event.type == pg.K_DOWN:
                    print('down button pressed')
                    # make sprite rotate


                elif event.type == pg.K_LEFT:
                    print('left button pressed')
                    # make sprite rotate


        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_UP]:
            if y >= 5:
                y -= 5
        elif keys_pressed[pg.K_DOWN]:

            if y <= 460:
                y += 5

        elif keys_pressed[pg.K_LEFT]:
            if x >= 5:
                x -= 5
        elif keys_pressed[pg.K_RIGHT]:
            if x <= 1075:
                x += 5
        #print('X:',x)
        #print('Y',y)
        pg.display.update()



if __name__ == '__main__':
    main()