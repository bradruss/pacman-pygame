class Point:
    def __init__(self, positionx, positiony):
        self.positionx = positionx
        self.positiony = positiony
        self.touched = False
        self.is_power_up = False


    def get_touched(self):
        return self.touched

    def get_x(self):
        return self.positionx

    def get_y(self):
        return self.positiony

    def touched(self):
        self.touched = True
