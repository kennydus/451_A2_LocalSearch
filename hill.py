import time
import board


# Prints out the completed board
def output_board(in_board):
    for i in range(in_board.n_queen):
        for j in range(in_board.n_queen):
            if in_board.map[i][j] == 1:
                print(1, end=' ')
            else:
                print('- ', end='')
        print()


def hill_climb(in_board):
    start_time = time.time_ns()
    # Initializing variables
    best_fitness = in_board.get_fitness()

    n_queen = in_board.n_queen

    while best_fitness != 0:
        for row in range(n_queen):
            # Represents index of queen in the row that results in the least number of attacking pairs.
            # Set it to the row's initial queen's index.
            best_index = in_board.map[row].index(1)
            best_fitness = in_board.get_fitness()

            in_board.flip(row, in_board.map[row].index(1))  # Flip the current row's queen to 0
            for spot in range(n_queen):
                # Set current spot to be a queen
                in_board.flip(row, spot)
                fitness = in_board.get_fitness()
                if fitness < best_fitness:
                    best_fitness = fitness
                    best_index = spot
                # Remove queen from current spot
                in_board.flip(row, spot)
            # Set the queen at the best_index
            in_board.flip(row, best_index)

        # Reset the board (random restart)
        if best_fitness != 0:
            in_board.__init__(n_queen)

    # Convert running time from ns to milliseconds.
    running_time = (time.time_ns() - start_time) / (10 ** 6)
    print(f'Running time: {round(running_time)} ms')

    # Printing out the completed board
    output_board(in_board)


if __name__ == '__main__':
    temp = board.Board(5)

    # print('=== Running Hill-Climb Algorithm ===')
    hill_climb(temp)
