import pygame
import point

WIDTH = 50
WHITE = (255, 255, 255)
RED = (255,0,0)


class CorridorH:
    def __init__(self, x_start, x_end, y_start):
        self.x_startt = x_start
        self.x_startb = x_start
        self.y_start = y_start
        self.x_endt = x_end
        self.x_endb = x_end
        self.y_end = self.y_start + WIDTH
        #points array
        self.points = []

    def update_points(self):
        #find longest side
        topside = abs(self.x_startt - self.x_endt)
        bottomside = abs(self.x_startb - self.x_endb)

        if topside > bottomside:
            longestside = topside
            shortestside = bottomside
            xpos = self.x_startt
            xposend = self.x_endt
        else:
            longestside = bottomside
            shortestside = topside
            xpos = self.x_startb
            xposend = self.x_endb
        numpoints = longestside // 50

        scalingfactor = (shortestside) / (numpoints - 3)

        #populate points array
        ypos = self.y_start + 25
        xpos += 25
        print(self.x_endt)
        self.points.append(point.Point(int(xpos), int(ypos)))
        for i in range(1, numpoints - 1):
            self.points.append(point.Point(int(xpos), int(ypos)))
            xpos += scalingfactor

        self.points.append(point.Point(xposend - 25, int(ypos)))


    def draw(self, window):
        # Draw Top Line
        pygame.draw.line(window, WHITE, (self.x_startt, self.y_start), (self.x_endt, self.y_start))
        # Draw Bottom Line
        pygame.draw.line(window, WHITE, (self.x_startb, self.y_end), (self.x_endb, self.y_end))

        # for p in self.points:
        #     pygame.draw.circle(window, WHITE, (p.get_x(), p.get_y()), 3)
        #     print(p.get_x())
        #     print(p.get_y())



    def check_in_corridor(self, x, y):
        if (x >= self.x_start and x <= self.x_end and y >= self.y_start and y <= self.y_end):
            return True
        else:
            return False

    def print(self):
        print_str = "Horizontal, x_startt = " + str(self.x_startt) + ", x_startb = " + str(self.x_startb) + ", x_endt = " + str(self.x_endt) + ", x_endb = " + str(self.y_endb)
        print(print_str)