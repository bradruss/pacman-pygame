class Leaderboard:
    def __init__(self):
        self.file = None
        self.top_scores = []
        self.leaderboard = []
        try:
            self.file = open("leaderboard.csv")
            self.load_leaderboard()
        except IOError:
            self.file = None
            print("Leaderboard file could not be opened")


    def load_leaderboard(self):
        for line in self.file:
            line = line.rstrip('\n')
            line = line.split(',')
            self.top_scores.append(line)

    def update_top_scores(self):
        print()


    def update_leaderboard(self):
        print()