import math
import random
import time


# Prints out the completed board
def output_board(board):
    for i in range(board.n_queen):
        for j in range(board.n_queen):
            if board.map[i][j] == 1:
                print(1, end=' ')
            else:
                print('- ', end='')
        print('\n')


def generate_q_string(board):
    q_string = ''
    for column in range(board.n_queen):
        for row in range(board.n_queen):
            if board.map[row][column] == 1:
                q_string += str(row + 1)
                break
    return q_string


def genetic(boards):
    start_time = time.time_ns()
    iteration = 0
    # FOR EACH ARRAY, VALUES BELONG TO EACH BOARD IN ORDER
    # EX. initial_population[0] contains the string of queen positions for board #1.

    total_pairs = math.comb(boards[0].n_queen, 2)

    while True:
        # Array of strings (digits) that indicate the position of the queen in each column, per board.
        initial_population = []
        # Number of non-attacking pairs per board
        non_attacking_pairs = []

        for board in boards:
            # q_string represents the position of the queens in each column, starting from the leftmost column.
            # Top-most row is '1', and bottom-most row is '5'.
            q_string = generate_q_string(board)
            initial_population.append(q_string)

            non_attacking_pairs.append(total_pairs - board.get_genetic_fitness())

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
            cross_point = random.randint(1, 3)
            children.append(parents[i][:cross_point] + parents[i + 1][cross_point:])
            children.append(parents[i + 1][:cross_point] + parents[i][cross_point:])

        mutated_children = []
        for index in range(len(children)):
            # Mutation: We will set chance of mutation to be 10%
            if random.random() < .1:
                # Getting index of queen to be mutated
                mut_index = random.randint(0, 4)
                mut_position = random.randint(1, 5)

                # print(f'q_string mutated: {children[index]} at index {mut_index}')
                mutated_children.append(
                    children[index][:mut_index] + str(mut_position) + children[index][mut_index + 1:])
            else:
                mutated_children.append(children[index])

        # Reset boards to zero, and create ones that match the strings from mutation list.
        for board in boards:
            board.map = [[0 for _ in range(5)] for _ in range(5)]
        for i in range(len(boards)):
            current_column = 0
            for q_pos in mutated_children[i]:
                boards[i].flip(int(q_pos) - 1, current_column)
                current_column += 1

        iteration += 1


        print('initial_population:\t', initial_population)
        print('choose_prob:\t\t', end=' ')
        rounded_probs = []
        for prob in choose_prob:
            rounded_probs.append('{:.3f}'.format(round(prob, 5)))
        print(rounded_probs)

        print(f'non-attack pairs:\t {non_attacking_pairs}')
        print('parents:\t\t\t', parents)
        print('children:\t\t\t', children)
        print(f'mutated_children:\t {mutated_children}\n')

        # Test fitness of each board
        for i in range(len(boards)):
            if boards[i].get_genetic_fitness() == 0:
                running_time = (time.time_ns() - start_time) / 10 ** 6
                print('Generations:', iteration)
                print(f'Running time: {round(running_time)}ms')
                output_board(boards[i])
                return boards[i]
