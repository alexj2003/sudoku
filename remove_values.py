# remove values from the sudoku grid so user can solve it
def attempt_solve(g):
    position = find_empty(g)
    if not position:  # if no empty boxes, exit function
        return True
    row, column = position

    for number in range(1, 10):
        if not(number in g[row]):
            if not number in (g[0][column], g[1][column], g[2][column], g[3][column], g[4][column], g[5][column], g[6][column], g[7][column], g[8][column]):
                square = []  # find the square the value is located in
                if row <= 2:
                    if column <= 2:
                        for j in range(0, 3):
                            square.append(g[j][0:3])
                    elif column <= 5:
                        for j in range(0, 3):
                            square.append(g[j][3:6])
                    else:
                        for j in range(0, 3):
                            square.append(g[j][6:9])
                elif row <= 5:
                    if column <= 2:
                        for j in range(3, 6):
                            square.append(g[j][0:3])
                    elif column <= 5:
                        for j in range(3, 6):
                            square.append(g[j][3:6])
                    else:
                        for j in range(3, 6):
                            square.append(g[j][6:9])
                else:
                    if column <= 2:
                        for j in range(6, 9):
                            square.append(g[j][0:3])
                    elif column <= 5:
                        for j in range(6, 9):
                            square.append(g[j][3:6])
                    else:
                        for j in range(6, 9):
                            square.append(g[j][6:9])
                if not(any(number in sublist for sublist in square)):
                    # if value not in the square, row or column - add it to that box
                    g[row][column] = number
                    if attempt_solve(g) == True:
                        # if puzzle can be solved with that value, keep it
                        return True
                    # if puzzle cant be solved with that value, replace it
                    g[row][column] = 0
    return False


def find_empty(grid):  # find next empty box, and return coordinates
    for x in range(0, 9):
        for y in range(0, 9):
            if grid[x][y] == 0:
                return (x, y)
    return None


def remove_numbers(grid, difficulty):
    from random import randint
    if difficulty == "e":
        to_remove = 50  # remove 50 numbers if easy difficulty
    elif difficulty == "h":
        to_remove = 75  # remove 75 numbers if hard difficulty
    indices = []
    while to_remove > 0:
        # while that many numbers haven't been removed, attempt to remove another value
        x = randint(0, 8)
        y = randint(0, 8)
        backup = grid[x][y]
        grid[x][y] = 0
        for i in range(0, len(indices)):
            row = indices[i][0]
            column = indices[i][1]
            grid[row][column] = 0
        copy_grid = grid.copy()
        # check if solution can still be found
        if attempt_solve(copy_grid) == True:
            to_remove -= 1
            indices.append([x, y])
        else:
            grid[x][y] = backup
    for i in range(0, len(indices)):
        row = indices[i][0]
        column = indices[i][1]
        grid[row][column] = 0
    return grid


def main(difficulty):
    from gen_complete_grid import generate_grid
    complete_grid = generate_grid()  # generate compelted grid

    temp = []
    for i in range(0, 9):
        temp.append(complete_grid[i].copy())

    # remove numbers from the grid
    user_grid = remove_numbers(complete_grid, difficulty)

    return user_grid, temp
