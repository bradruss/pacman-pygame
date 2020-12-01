import pygame
import point

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

        # points array
        self.points = []

    def update_points(self):
        # find longest side
        leftside = abs(self.y_startl - self.y_endl)
        rightside = abs(self.y_startr - self.y_endr)

        if leftside > rightside:
            longestside = leftside
            shortestside = rightside
            ypos = self.y_startl
            yposend = self.y_endl
        else:
            longestside = rightside
            shortestside = leftside
            ypos = self.y_startr
            yposend = self.y_endr
        numpoints = longestside // 50

        denom = numpoints - 3
        if denom <=0:
            denom = 3

        scalingfactor = (shortestside) / denom

        # populate points array
        xpos = self.x_start + 25
        ypos += 25
        self.points.append(point.Point(int(xpos), int(ypos)))
        for i in range(1, numpoints - 1):
            self.points.append(point.Point(int(xpos), int(ypos)))
            ypos += scalingfactor

        self.points.append(point.Point(int(xpos), yposend - 25))

    def draw(self, window):
        # Draw Left Line
        pygame.draw.line(window, WHITE, (self.x_start, self.y_startl), (self.x_start, self.y_endl))
        # Draw Right Line
        pygame.draw.line(window, WHITE, (self.x_end, self.y_startr), (self.x_end, self.y_endr))

        # for p in self.points:
        #     pygame.draw.circle(window, WHITE, (p.get_x(), p.get_y()), 3)

    def check_in_corridor(self, x, y):
        if (x >= self.x_start and x <= self.x_end and y >= self.y_startl and y <= self.y_endl):
            return True
        else:
            return False

    def print(self):
        print_str = "Vertical, y_startl = " + str(self.y_startl) + ", y_startr = " + str(self.y_startr) + ", y_endl = " + str(self.y_endl) + ", y_endr = " + str(self.y_endr)
        print(print_str)