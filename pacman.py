import pygame as pg

class Pacman:
    def __init__(self, icon):
        self.num_lives = 5
        # Total score
        self.num_coins = 0
        self.is_dangerous = False

        # Set pacman sprite to pacman by default
        self.sprite = [pg.image.load('pacman/Pacman.png'), pg.image.load('pacman/Pacman2.png'), pg.image.load('pacman/Pacman3.png')]

        # Takes parameter when creating ghost and sets it to whatever is selected by the user
        if icon == 'biden':
            self.sprite = [pg.image.load('biden/close.png'), pg.image.load('biden/close2.png'), pg.image.load('biden/open.png')]
            self.death = [pg.image.load('pacman/pacman-death-1.png'), pg.image.load('pacman/pacman-death-2.png'), pg.image.load('pacman/pacman-death-3.png'), pg.image.load('pacman/pacman-death-4.png'),
                          pg.image.load('pacman/pacman-death-5.png'), pg.image.load('pacman/pacman-death-6.png'), pg.image.load('pacman/pacman-death-7.png'), pg.image.load('pacman/pacman-death-8.png')]
        elif icon == 'trump':
            self.sprite = [pg.image.load('trump/trump-closed.png'), pg.image.load('trump/trump-open.png'),pg.image.load('trump/trump-closed.png')]
            self.death = [pg.image.load('trump/trump-death-1.png'), pg.image.load('trump/trump-death-2.png'), pg.image.load('trump/trump-death-3.png'), pg.image.load('trump/trump-death-4.png'),
                          pg.image.load('trump/trump-death-5.png'), pg.image.load('trump/trump-death-6.png'), pg.image.load('trump/trump-death-7.png'), pg.image.load('trump/trump-death-8.png')]
        elif icon == 'pacman':
            self.sprite = [pg.image.load('pacman/Pacman.png'), pg.image.load('pacman/Pacman2.png'), pg.image.load('pacman/Pacman3.png')]
            self.death = [pg.image.load('pacman/pacman-death-1.png'), pg.image.load('pacman/pacman-death-2.png'), pg.image.load('pacman/pacman-death-3.png'), pg.image.load('pacman/pacman-death-4.png'),
                          pg.image.load('pacman/pacman-death-5.png'), pg.image.load('pacman/pacman-death-6.png'), pg.image.load('pacman/pacman-death-7.png'), pg.image.load('pacman/pacman-death-8.png')]
        else:
            self.sprite = [pg.image.load('pacman/Pacman.png'), pg.image.load('pacman/Pacman2.png'), pg.image.load('pacman/Pacman3.png')]
            self.death = [pg.image.load('pacman/pacman-death-1.png'), pg.image.load('pacman/pacman-death-2.png'), pg.image.load('pacman/pacman-death-3.png'), pg.image.load('pacman/pacman-death-4.png'),
                          pg.image.load('pacman/pacman-death-5.png'), pg.image.load('pacman/pacman-death-6.png'), pg.image.load('pacman/pacman-death-7.png'), pg.image.load('pacman/pacman-death-8.png')]


        self.waka = pg.mixer.Sound('Sound/waka.wav')
        self.waka.set_volume(0.5)

    def get_num_coins(self):
        return self.num_coins

    def get_is_dangerous(self):
        return self.is_dangerous

    def set_num_coins(self, num_coins):
        self.num_coins = num_coins

    def collect_coin(self):
        self.num_coins += 10

    def get_num_lives(self):
        return self.num_lives

    def set_num_lives(self, num_lives):
        self.num_lives = num_lives

    # Load pacman death animation
    def show_death(self, disp, rotation, x, y):
        clock = pg.time.Clock()
        for i in range(0, 8):
            disp.blit(pg.transform.rotate(self.death[i], rotation), (x, y))
            clock.tick(100000)
            pg.display.update()