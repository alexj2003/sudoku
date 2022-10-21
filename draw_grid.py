from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont
from PyQt5.QtCore import Qt
import sys
from time import time
from datetime import timedelta

# draw a grid for the sudoku program


class sudokuGrid(QWidget):
    def __init__(self):  # initialise window
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 900, 550)
        self.setWindowTitle("Sudoku")
        # setMouseTracking will be used later to find the mouse coordinates
        self.setMouseTracking(True)

        # add buttons to the window
        easy_btn = QPushButton("Generate easy puzzle", self)
        easy_btn.setGeometry(550, 100, 150, 40)
        easy_btn.clicked.connect(self.gen_easy)

        hard_btn = QPushButton("Generate hard puzzle", self)
        hard_btn.setGeometry(550, 150, 150, 40)
        hard_btn.clicked.connect(self.gen_hard)

        self.hint_btn = QPushButton(self)
        self.hint_btn.setGeometry(550, 250, 150, 40)
        self.hint_btn.clicked.connect(self.give_hint)

        solve_btn = QPushButton("Give Up", self)
        solve_btn.setGeometry(550, 300, 150, 40)
        solve_btn.clicked.connect(self.solve_puzzle)

        # automatically generate an easy puzzle when the program is started
        self.gen_easy()
        hint_text = "Hint (" + str(self.hints) + ")"
        self.hint_btn.setText(str(hint_text))
        self.show()

    def timer_start(self):
        # start a timer to track the length of time it takes to solve the puzzle
        self.start = time()
        self.is_started = True  # keep track of whether timer has been started

    def timer_end(self):
        if self.is_started:
            # end the timer and output the length of time elapsed
            self.end = time()
            # find time elapsed in seconds
            self.time_elapsed = round(self.end - self.start)
            # convert time_elapsed into HH:MM:SS
            self.time_elapsed = str(timedelta(seconds=self.time_elapsed))
            self.total_hints -= self.hints
            self.is_started = False
            self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        # when the left mouse button is clicked, get the coordinates of the mouse
        from math import floor
        if QMouseEvent.button() == Qt.LeftButton:
            x_coord = int(floor(QMouseEvent.x()))
            y_coord = int(floor(QMouseEvent.y()))

            # using the coords, calculate what box the mouse is in
            if (x_coord >= 50) and (x_coord <= 500) and (y_coord >= 50) and (y_coord <= 500):
                self.update_row = (int(floor((x_coord*9) / 450)-1))
                self.update_column = (int(floor((y_coord*9) / 450)-1))

    def keyPressEvent(self, QKeyEvent):
        # when user presses a key
        # if its a number - make that number the current selection
        # update the selected box with that number
        if not self.is_solved:
            # if puzzle isn't solved, values can be changed
            # find if the user has pressed a number key:
            if QKeyEvent.key() == Qt.Key_1:
                self.selected_value = 1
            elif QKeyEvent.key() == Qt.Key_2:
                self.selected_value = 2
            elif QKeyEvent.key() == Qt.Key_3:
                self.selected_value = 3
            elif QKeyEvent.key() == Qt.Key_4:
                self.selected_value = 4
            elif QKeyEvent.key() == Qt.Key_5:
                self.selected_value = 5
            elif QKeyEvent.key() == Qt.Key_6:
                self.selected_value = 6
            elif QKeyEvent.key() == Qt.Key_7:
                self.selected_value = 7
            elif QKeyEvent.key() == Qt.Key_8:
                self.selected_value = 8
            elif QKeyEvent.key() == Qt.Key_9:
                self.selected_value = 9
            elif QKeyEvent.key() == Qt.Key_Backspace:
                self.selected_value = " "
            try:
                # try to enter the selected value into the selected box:
                self.user_grid[self.update_row][self.update_column] = self.selected_value
                self.update()
            except AttributeError:
                # user hasn't selected a box to enter a value into yet
                pass
            finally:
                # check if the puzzle is solved after the user enters a value
                self.check_puzzle()

    def paintEvent(self, e):
        # use QPainter to draw a grid
        qp = QPainter()
        qp.begin(self)

        # change font size
        font = QFont()
        font.setPointSize(20)
        qp.setFont(font)

        # call functions to draw different parts of the GUI:
        self.draw_square(qp)
        self.draw_lines(qp)
        self.draw_grid(qp, self.user_grid)
        self.draw_text(qp)
        qp.end()

    def draw_square(self, qp):
        # draw square to contain the grid
        brush = QBrush()
        qp.setBrush(brush)
        qp.drawRect(50, 50, 450, 450)

    def draw_lines(self, qp):
        # draw 8 horizontal and 8 vertical lines to make the grid
        for i in range(1, 9):
            if i % 3 == 0:
                pen = QPen(Qt.black, 5, Qt.SolidLine)
            else:
                pen = QPen(Qt.black, 2, Qt.SolidLine)

            qp.setPen(pen)
            x1 = int(50 + ((i/9)*450))
            y1 = 50
            x2 = x1
            y2 = 500

            qp.drawLine(x1, y1, x2, y2)  # draws line from (x1, y1) to (x2, y2)
            qp.drawLine(y1, x1, y2, x2)

    def draw_grid(self, qp, grid):
        # draw the sudoku grid values
        for row in range(0, 9):
            for column in range(0, 9):
                # find the x and y values to draw the values at:
                x = int(65 + 450*((row)/9))
                y = int(37 + 450*((column+1)/9))
                if grid[row][column] != 0:
                    text = str(grid[row][column])
                    qp.drawText(x, y, text)

    def draw_text(self, qp):
        if self.is_solved:
            if self.gave_up:
                text = "You gave up after " + str(self.time_elapsed) + "."
                self.gave_up = False
            else:
                text = "Puzzle solved in " + \
                    str(self.time_elapsed)+" using " + \
                    str(self.total_hints)+" hints."
            qp.drawText(50, 537, text)

    def gen_easy(self):
        # generate a new easy puzzle when button is pressed
        from remove_values import main
        self.user_grid, self.complete_grid = main("e")
        self.hints = 5  # allow 5 hints for easy mode
        self.total_hints = 5
        hint_text = "Hint (" + str(self.hints) + ")"
        self.hint_btn.setText(str(hint_text))
        self.is_solved = False  # puzzle isn't solved - user can change values in grid
        self.timer_start()
        self.update()

    def gen_hard(self):
        # generate a new hard puzzle when button is pressed
        from remove_values import main
        self.user_grid, self.complete_grid = main("h")
        self.hints = 3  # allow 3 hints for easy mode
        self.total_hints = 3
        hint_text = "Hint (" + str(self.hints) + ")"
        self.hint_btn.setText(str(hint_text))
        self.is_solved = False
        self.timer_start()
        self.update()

    def give_hint(self):
        if not self.is_solved:  # if puzzle isn't solved
            if self.hints > 0:  # if user has hints left
                from random import randint
                self.hints -= 1
                hint_text = "Hint (" + str(self.hints) + ")"
                self.hint_btn.setText(str(hint_text))
                # pick a random box that has no value entered and display the correct value for that box
                row = randint(0, 8)
                column = randint(0, 8)
                while self.user_grid[row][column] != 0:
                    row = randint(0, 8)
                    column = randint(0, 8)
                self.user_grid[row][column] = self.complete_grid[row][column]
                self.update()

    def check_puzzle(self):
        # check if the puzzle has been solved
        is_correct = True
        for row in range(0, 9):
            for column in range(0, 9):
                if self.user_grid[row][column] != self.complete_grid[row][column]:
                    # puzzle isn't solved
                    is_correct = False
        if is_correct:  # if puzzle is correct, end game
            self.is_solved = True
            self.gave_up = False
            self.timer_end()

    def solve_puzzle(self):
        # when user clicks the solve button, fill in the grid
        self.user_grid = self.complete_grid
        if not self.is_solved:  # if puzzle not already completed
            self.gave_up = True
        else:
            self.gave_up = False
        self.is_solved = True
        self.timer_end()
        self.update()


def main():
    # create PyQt5 application
    app = QApplication(sys.argv)
    ex = sudokuGrid()
    sys.exit(app.exec_())
