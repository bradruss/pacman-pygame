class WallV:
    def __init__(self, x_fixed, y_start, y_end):
        self.x_fixed = x_fixed
        self.y_start = y_start
        self.y_end = y_end

    def get_x_fixed(self):
        return self.x_fixed

    def get_y_start(self):
        return self.y_start

    def get_y_end(self):
        return self.y_end