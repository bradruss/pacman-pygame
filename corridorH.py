import pygame

WIDTH = 50
WHITE = (255, 255, 255)


class CorridorH:
    def __init__(self, x_start, x_end, y_start):
        self.x_startt = x_start
        self.x_startb = x_start
        self.y_start = y_start
        self.x_endt = x_end
        self.x_endb = x_end
        self.y_end = self.y_start + WIDTH

    def draw(self, window):
        # Draw Top Line
        pygame.draw.line(window, WHITE, (self.x_startt, self.y_start), (self.x_endt, self.y_start))
        # Draw Bottom Line
        pygame.draw.line(window, WHITE, (self.x_startb, self.y_end), (self.x_endb, self.y_end))

    def check_in_corridor(self, x, y):
        if (x >= self.x_start and x <= self.x_end and y >= self.y_start and y <= self.y_end):
            return True
        else:
            return False

    def print(self):
        print_str = "Horizontal, x_startt = " + str(self.x_startt) + ", x_startb = " + str(self.x_startb) + ", x_endt = " + str(self.x_endt) + ", x_endb = " + str(self.y_endb)
        print(print_str)