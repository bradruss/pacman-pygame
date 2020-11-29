from operator import itemgetter
class Leaderboard:
    def __init__(self):
        self.file = None
        self.top_scores = []
        self.leaderboard = []
        self.leaderboard_sorted = []
        try:
            self.file = open("leaderboard.csv")
            self.load_leaderboard()
        except IOError:
            self.file = None
            print("Leaderboard file could not be opened")

    def load_leaderboard(self):
        print("load leaderboard called")
        for line in self.file:
            line = line.rstrip('\n')
            first = line.split(',')[0]
            second = line.split(',')[1]
            second = int(second)
            temp = []
            temp.append(first)
            temp.append(second)
            self.leaderboard.append(temp)

    def update_top_scores(self):
        self.leaderboard_sorted = self.leaderboard
        self.leaderboard_sorted = sorted(self.leaderboard_sorted, key=itemgetter(1), reverse=False)

        # Populate top scores
        upper_bound = len(self.leaderboard_sorted) - 1
        for a in range(20):
            if len(self.leaderboard_sorted) > 0:
                self.top_scores.append(self.leaderboard_sorted[upper_bound])
                upper_bound -= 1

    def update_leaderboard(self, element):
        self.leaderboard.append(element)
        self.update_top_scores()

        # Write out to CSV
        if self.file is not None:
            self.file.close()
            self.file = open('leaderboard.csv', 'a')
            self.file.write('\n' + element[0] + ',' + str(element[1]))
            self.file.close()
        else:
            print("Failed to update local leaderboard csv")
