import random
import numpy as np
from hill import *
from genetic import *
import time


class Board:
    def __init__(self, n):
        self.n_queen = n
        self.map = [[0 for j in range(n)] for i in range(n)]

        for i in range(self.n_queen):
            j = random.randint(0, self.n_queen - 1)
            self.map[i][j] = 1

    # Returns number of attacking pairs.
    def get_fitness(self):
        fit = 0
        for i in range(self.n_queen):  # i represents row index
            for j in range(self.n_queen):  # j represents column index
                if self.map[i][j] == 1:
                    for k in range(1, self.n_queen - i):
                        if self.map[i + k][j] == 1:  # checking vertical (straight down)
                            fit += 1
                        if j - k >= 0 and self.map[i + k][j - k] == 1:  # checking diagonal (down + left)
                            fit += 1
                        if j + k < self.n_queen and self.map[i + k][j + k] == 1:  # checking diagonal (down + right)
                            fit += 1
        return fit

    def show_map(self):
        print(np.matrix(self.map))

    def flip(self, i, j):
        if self.map[i][j] == 0:
            self.map[i][j] = 1
        else:
            self.map[i][j] = 0


if __name__ == '__main__':
    test = Board(8)
    print(test.get_fitness())
    test.show_map()
    hill_climb(test, True)

    boards = []
    for i in range(8):
        temp = Board(5)
        hill_climb(temp, False)
        boards.append(temp)

    genetic(boards)
