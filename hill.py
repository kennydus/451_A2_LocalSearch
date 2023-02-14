import time


def hill_climb(board):
    start_time = time.time_ns()
    # Initializing variables
    best_fitness = board.get_fitness()

    while best_fitness != 0:
        for row in range(board.n_queen):
            # Represents index of queen in the row that results in the least number of attacking pairs.
            # Set it to the row's initial queen's index.
            best_index = board.map[row].index(1)
            best_fitness = board.get_fitness()

            board.flip(row, board.map[row].index(1))  # Flip the current row's queen to 0
            for spot in range(board.n_queen):
                # Set current spot to be a queen
                board.flip(row, spot)
                fitness = board.get_fitness()
                if fitness < best_fitness:
                    best_fitness = fitness
                    best_index = spot
                # Remove queen from current spot
                board.flip(row, spot)
            # Set the queen at the best_index
            board.flip(row, best_index)

        # Reset the board (random restart)
        if best_fitness != 0:
            board.__init__(board.n_queen)

    # Convert running time from ns to milliseconds.
    running_time = (time.time_ns() - start_time) / (10**6)
    print(f'Running time: {round(running_time)} ms')

    # Printing out the completed board
    for i in range(board.n_queen):
        for j in range(board.n_queen):
            if board.map[i][j] == 1:
                print(1, end=' ')
            else:
                print('- ', end='')
        print('\n')
