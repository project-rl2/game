class Stats:
    def __init__(self):
        self.reset_stats()
        self.run_game = True
        self.cur_lever = 1
        self.DefeatedEnemies = 0
        with open('my_game/record.txt', 'r') as file:
            self.maxDefeatedEnemies = int(file.readline())

    def reset_stats(self):
        self.cur_lever = 1
        self.DefeatedEnemies = 0
