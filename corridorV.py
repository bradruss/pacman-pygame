import pygame

WIDTH = 50
WHITE = (255, 255, 255)


class CorridorV:
    def __init__(self, x_start, y_start, y_end):
        self.x_start = x_start
        self.y_startl = y_start
        self.y_startr = y_start
        self.x_end = self.x_start + WIDTH
        self.y_endl = y_end
        self.y_endr = y_end


    def draw(self, window):
        # Draw Left Line
        pygame.draw.line(window, WHITE, (self.x_start, self.y_startl), (self.x_start, self.y_endl))
        # Draw Right Line
        pygame.draw.line(window, WHITE, (self.x_end, self.y_startr), (self.x_end, self.y_endr))

    def check_in_corridor(self, x, y):
        if (x >= self.x_start and x <= self.x_end and y >= self.y_start and y <= self.y_end):
            return True
        else:
            return False

    def print(self):
        print_str = "Vertical, y_startl = " + str(self.y_startl) + ", y_startr = " + str(self.y_startr) + ", y_endl = " + str(self.y_endl) + ", y_endr = " + str(self.y_endr)
        print(print_str)