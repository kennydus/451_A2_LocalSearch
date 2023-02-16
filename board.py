import copy
import random
import numpy as np
from hill import *
from genetic import *
from genetic_recursive import *
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

    # Remake the boards so that there are only 1 queen per column. Used for genetic algorithm.
    def remake_genetic(self):
        self.map = [[0 for _ in range(5)] for _ in range(5)]
        for column in range(5):
            row = random.randint(0, 4)
            self.map[row][column] = 1

    # Returns number of attacking pairs.
    # Starting from leftmost column, checks for queens in
    # diagonal and horizontal plane towards the right side.
    def get_genetic_fitness(self):
        fit = 0
        for i in range(self.n_queen):  # i represents column index
            for j in range(self.n_queen):  # j represents row index  [row][column]
                if self.map[j][i] == 1:  # if we found the queen in the current column
                    for k in range(1, self.n_queen - i):
                        if self.map[j][i + k] == 1:  # checking horizontal (right side)
                            fit += 1
                        if j - k >= 0 and self.map[j - k][i + k] == 1:  # checking diagonal (up + right)
                            fit += 1
                        if j + k < self.n_queen and self.map[j + k][i + k] == 1:  # checking diagonal (down + right)
                            fit += 1
        return fit


if __name__ == '__main__':
    test = Board(5)
    print(test.get_fitness())
    test.show_map()
    print('\n=== Running Hill Climb ===\n')
    hill_climb(board=test)

    boards = []
    for i in range(8):
        temp = Board(5)
        temp.remake_genetic()
        boards.append(temp)
    print('\n=== Running Genetic ===\n')
    recursive_boards = copy.deepcopy(boards)
    genetic(boards)
    # genetic_recursive(recursive_boards, iteration=0, start_time=time.time_ns())

