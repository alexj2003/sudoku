# algorithm to generate a complete sudoku grid
def check_grid(grid):  # check if grid is full (i.e. not got any zeros in it)
    for row in range(0, 9):
        for column in range(0, 9):
            if grid[row][column] == 0:  # if a zero is present
                return False
    # if no zeros are present in the grid - grid is full
    return True


def fill_grid(grid):  # generate a complete grid
    from random import shuffle
    possible_solutions = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # returns True when grid is complete
    for i in range(0, 81):  # lopp through all 81 boxes in the grid
        # find the row and column of that box:
        row = i//9
        column = i % 9

        if grid[row][column] == 0:  # if value hasnt been filled yet
            shuffle(possible_solutions)
            for number in possible_solutions:
                if not(number in grid[row]):  # if value not in row
                    # if value not in column
                    if not number in (grid[0][column], grid[1][column], grid[2][column], grid[3][column], grid[4][column], grid[5][column], grid[6][column], grid[7][column], grid[8][column]):
                        # find square that the box is in
                        square = []
                        if row <= 2:  # if in rows 0,1,2
                            if column <= 2:  # if in columns 0,1,2
                                for j in range(0, 3):
                                    square.append(grid[j][0:3])
                            elif column <= 5:  # if in columns 3,4,5
                                for j in range(0, 3):
                                    square.append(grid[j][3:6])
                            else:  # if in columns 6,7,8
                                for j in range(0, 3):
                                    square.append(grid[j][6:9])
                        elif row <= 5:  # if in rows 3,4,5
                            if column <= 2:  # if in columns 0,1,2
                                for j in range(3, 6):
                                    square.append(grid[j][0:3])
                            elif column <= 5:  # if in columns 3,4,5
                                for j in range(3, 6):
                                    square.append(grid[j][3:6])
                            else:  # if in columns 6,7,8
                                for j in range(3, 6):
                                    square.append(grid[j][6:9])
                        else:  # if in rows 6,7,8
                            if column <= 2:  # if in columns 0,1,2
                                for j in range(6, 9):
                                    square.append(grid[j][0:3])
                            elif column <= 5:  # if in columns 3,4,5
                                for j in range(6, 9):
                                    square.append(grid[j][3:6])
                            else:  # if in columns 6,7,8
                                for j in range(6, 9):
                                    square.append(grid[j][6:9])

                        # if value isn't in the square
                        if not(any(number in sublist for sublist in square)):
                            grid[row][column] = number  # add value to that box
                            if check_grid(grid) == True:  # if grid is complete
                                return True  # return True
                            elif fill_grid(grid) == True:
                                # call another instance of the function and iterate through all boxes again
                                return True  # return true if grid is compelted
            break
    grid[row][column] = 0


def generate_grid():
    grid = []  # create 9x9 array
    for i in range(9):
        grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

    done = fill_grid(grid)
    return grid
