class WallV:
    def __init__(self, y_fixed, x_start, x_end):
        self.y_fixed = y_fixed
        self.x_start = x_start
        self.x_end = x_end

    def get_y_fixed(self):
        return self.y_fixed

    def get_x_start(self):
        return self.x_start

    def get_x_end(self):
        return self.x_end