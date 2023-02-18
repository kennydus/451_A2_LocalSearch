import math
import random
import time
import board


# Remake the boards so that there are only 1 queen per column.
def remake_board(in_board):
    in_board.map = [[0 for _ in range(in_board.n_queen)] for _ in range(in_board.n_queen)]
    for column in range(in_board.n_queen):
        row = random.randint(0, in_board.n_queen - 1)
        in_board.map[row][column] = 1
    return in_board


# Returns number of attacking pairs.
# Starting from leftmost column, checks for queens in the
# diagonal and horizontal planes towards the right side.
def get_genetic_fitness(in_board):
    fit = 0
    for i in range(in_board.n_queen):
        for j in range(in_board.n_queen):
            if in_board.map[j][i] == 1:
                for k in range(1, in_board.n_queen - i):
                    if in_board.map[j][i + k] == 1:  # checking horizontal (right side)
                        fit += 1
                    if j - k >= 0 and in_board.map[j - k][i + k] == 1:  # checking diagonal (up + right)
                        fit += 1
                    if j + k < in_board.n_queen and in_board.map[j + k][i + k] == 1:  # checking diagonal (down + right)
                        fit += 1
    return fit


# Prints out the completed board
def output_board(in_board):
    for i in range(in_board.n_queen):
        for j in range(in_board.n_queen):
            if in_board.map[i][j] == 1:
                print(1, end=' ')
            else:
                print('- ', end='')
        print()


def generate_q_string(in_board):
    q_string = ''
    for column in range(in_board.n_queen):
        for row in range(in_board.n_queen):
            if in_board.map[row][column] == 1:
                q_string += str(row + 1)
                break
    return q_string


def genetic(boards):
    start_time = time.time_ns()
    n_queen = boards[0].n_queen
    iteration = 0
    # FOR EACH ARRAY, VALUES BELONG TO EACH BOARD IN ORDER
    # EX. initial_population[0] contains the string of queen positions for board #1.

    # Remake the boards so that there are only 1 queen per column.
    for i in range(len(boards)):
        boards[i] = remake_board(boards[i])

    # Maximum amount of non-attacking pairs
    total_pairs = math.comb(n_queen, 2)

    while True:
        # Array of strings (digits) that indicate the position of the queen in each column, per board.
        initial_population = []
        # Number of non-attacking pairs per board
        non_attacking_pairs = []

        for b in boards:
            # q_string represents the position of the queens in each column, starting from the leftmost column.
            # Top-most row is '1', and bottom-most row is 'n_queen'.
            q_string = generate_q_string(b)
            initial_population.append(q_string)

            non_attacking_pairs.append(total_pairs - get_genetic_fitness(b))

        # Probability of each board being chosen for reproducing.
        choose_prob = []
        for num_pairs in non_attacking_pairs:
            choose_prob.append(num_pairs / sum(non_attacking_pairs))

        # Parents contains the strings chosen for reproduction.
        parents = []
        for i in range(len(boards)):
            r = random.random()
            if r <= choose_prob[0]:
                parents.append(initial_population[0])
            elif r <= sum(choose_prob[:2]):
                parents.append(initial_population[1])
            elif r <= sum(choose_prob[:3]):
                parents.append(initial_population[2])
            elif r <= sum(choose_prob[:4]):
                parents.append(initial_population[3])
            elif r <= sum(choose_prob[:5]):
                parents.append(initial_population[4])
            elif r <= sum(choose_prob[:6]):
                parents.append(initial_population[5])
            elif r <= sum(choose_prob[:7]):
                parents.append(initial_population[6])
            else:
                parents.append(initial_population[7])

        # Children contains the strings after crossover stage.
        children = []
        for i in range(0, len(boards), 2):
            # Crossover point should include at least 1 digit from each parent.
            cross_point = random.randint(1, n_queen - 2)
            children.append(parents[i][:cross_point] + parents[i + 1][cross_point:])
            children.append(parents[i + 1][:cross_point] + parents[i][cross_point:])

        mutated_children = []
        for index in range(len(children)):
            # Mutation: We will set chance of mutation to be 10%
            if random.random() < .1:
                # Getting index of queen to be mutated
                mut_index = random.randint(0, n_queen - 1)
                mut_position = random.randint(1, n_queen)

                # print(f'q_string mutated: {children[index]} at index {mut_index}')
                mutated_children.append(
                    children[index][:mut_index] + str(mut_position) + children[index][mut_index + 1:])
            else:
                mutated_children.append(children[index])

        # Reset boards to zero, and create ones that match the strings from mutation list.
        for b in boards:
            b.map = [[0 for _ in range(n_queen)] for _ in range(n_queen)]
        for i in range(len(boards)):
            current_column = 0
            for q_pos in mutated_children[i]:
                boards[i].flip(int(q_pos) - 1, current_column)
                current_column += 1

        iteration += 1

        # Test fitness of each board
        for i in range(len(boards)):
            if get_genetic_fitness(boards[i]) == 0:
                running_time = (time.time_ns() - start_time) / 10 ** 6
                # print('Generations:', iteration)
                print(f'Running time: {round(running_time)}ms')
                output_board(boards[i])
                return boards[i]


if __name__ == '__main__':
    board_array = []
    for i in range(8):
        temp = board.Board(5)
        board_array.append(temp)

    # print('=== Running Genetic ===')
    genetic(board_array)
