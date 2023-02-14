import math
import random


def genetic(boards):
    # FOR EACH ARRAY, VALUES BELONG TO EACH BOARD IN ORDER
    # EX. initial_populations[0] contains the string of queen positions for board #1.
    total_pairs = math.comb(5, 2)

    # Array of strings (digits) that indicate the position of the queen in each column, per board.
    initial_populations = []
    # Number of non-attacking pairs per board
    non_attacking_pairs = []

    for board in boards:
        # Remake the boards so that there are only 1 queen per column
        board.map = [[0 for _ in range(5)] for _ in range(5)]
        for column in range(5):
            row = random.randint(0, 4)
            board.map[row][column] = 1

        # q_string represents the position of the queens in each column, starting from the leftmost column.
        # Bottom most row is '1', and topmost row is '5'.
        q_string = ''
        for column in range(5):
            for row in range(board.n_queen - 1, -1, -1):
                if board.map[row][column] == 1:
                    q_string += str(board.n_queen - row)
                    break

        non_attacking_pairs.append(total_pairs - board.get_fitness())

        initial_populations.append(q_string)
        print(q_string)

    print(initial_populations)

    # Probability of each board being chosen for reproducing.
    choose_prob = []
    for num_pairs in non_attacking_pairs:
        choose_prob.append(num_pairs / sum(non_attacking_pairs))
    print(choose_prob)

    # Selections contains the strings chosen for reproduction.
    selections = []
    for i in range(8):
        r = random.random()
        if 0 <= r <= choose_prob[0]:
            selections.append(initial_populations[0])
        elif r <= sum(choose_prob[:2]):
            selections.append(initial_populations[1])
        elif r <= sum(choose_prob[:3]):
            selections.append(initial_populations[2])
        elif r <= sum(choose_prob[:4]):
            selections.append(initial_populations[3])
        elif r <= sum(choose_prob[:5]):
            selections.append(initial_populations[4])
        elif r <= sum(choose_prob[:6]):
            selections.append(initial_populations[5])
        elif r <= sum(choose_prob[:7]):
            selections.append(initial_populations[6])
        else:
            selections.append(initial_populations[7])
    print(selections)

    cross_over = []
    for i in range(0, 8, 2):
        # Crossover point should include at least 1 digit from each parent.
        cross_point = random.randint(1, 3)
        temp = selections[i][:cross_point]
        cross_over.append(selections[i][:cross_point] + selections[i+1][cross_point:])
        cross_over.append(selections[i+1][:cross_point] + selections[i][cross_point:])
    print(cross_over)
