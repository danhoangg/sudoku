import numpy as np
import math


def getQuadrantNo(i: int, j: int) -> list[int]:  # gets the quadrant number for a given row and column number
    return [i // 3, j // 3]


def getSquareNo(i: int, j: int) -> int:  # gets the number of the square from column and row, number from 0-80
    return 9 * i + j


def getRowNumbers(rowNo: int) -> list[int]:
    listnums = []
    for i in range(9):
        listnums.append(rowNo * 9 + i)
    return listnums


def getColNumbers(colNo: int) -> list[int]:
    listnums = []
    for i in range(9):
        listnums.append(i * 9 + colNo)
    return listnums


def getQuadrantNumbers(quadNo1: int, quadNo2: int) -> list[int]:
    listnums = []
    for i in range(3):
        for j in range(3):
            listnums.append((quadNo1 * 27) + (i * 9) + (quadNo2 * 3) + j)
    return listnums


def viewGrid(grid):
    print()
    for i in range(9):
        if i % 3 == 0:
            for j in range(55):
                print('-', end="")
            print()
            print('‖', end="")
        else:
            print('‖', end="")
        for j in range(9):
            if math.isnan(grid[i][j]):
                num = ' '
            else:
                num = math.floor(grid[i][j])
            if j % 3 == 2:
                print(' ', num, ' ‖', end="")
            else:
                print(' ', num, ' |', end="")
        print()
    for i in range(55):
        print('-', end="")
    print()


class sudoku:
    def __init__(self):
        self.playerGrid = None
        self.answerGrid = np.zeros([9, 9])
        self.__fillGrid()

    def __getRow(self, rowNo: int) -> list[int]:  # returns list of numbers in the row
        return self.answerGrid[rowNo]

    def __getColumn(self, colNo: int) -> list[int]:  # returns list of numbers in the column
        return self.answerGrid[:, colNo]

    def __getQuadrant(self, squareNo: list[int]) -> list[int]:  # returns the list of numbers in the quadrant specified
        numbers = []
        for i in range(3):
            for j in range(3):
                numbers.append(self.answerGrid[3 * squareNo[0] + i, 3 * squareNo[1] + j])
        return numbers

    def __fillGrid(self):
        global rand
        numdict = {}
        for i in range(81):
            numdict[i] = {}

        impossible = True
        while impossible:
            impossible = False
            for i in range(9):
                for j in range(9):
                    legal = False  # checks if the number can be placed there
                    quadno = getQuadrantNo(i, j)
                    rownums = getRowNumbers(i)
                    colnums = getColNumbers(j)
                    quadnums = getQuadrantNumbers(quadno[0], quadno[1])

                    squareno = getSquareNo(i, j)

                    counter = 0
                    while not legal:
                        rand = np.random.randint(9, size=1)[0] + 1
                        legal = True

                        # check if the number is allowed to be in the square
                        if rand in numdict[squareno]:
                            legal = False

                        counter += 1
                        if counter >= 100:
                            impossible = True
                            for k in range(81):
                                numdict[k] = {}
                            self.answerGrid = np.zeros([9, 9])
                            break

                    if impossible:
                        break

                    self.answerGrid[i][j] = rand
                    numdict[squareno][rand] = 1
                    for k in rownums:
                        numdict[k][rand] = 1
                    for k in colnums:
                        numdict[k][rand] = 1
                    for k in quadnums:
                        numdict[k][rand] = 1
                if impossible:
                    break

    def play(self, difficulty: str):
        self.playerGrid = self.answerGrid.copy()
        match difficulty:
            case "easy":
                empty = 43
            case "medium":
                empty = 51
            case "hard":
                empty = 53
            case "pro":
                empty = 58
            case "expert":
                empty = 60
            case _:
                print('No difficulty selected')
                return
        counter = 0
        while counter != empty:  # making random squares empty
            randsquare = np.random.randint(81, size=1)[0]
            i = randsquare // 9
            j = randsquare - 9 * i

            if self.playerGrid[i][j] != '':
                self.playerGrid[i][j] = None
                counter += 1

        win = False
        while not win:

            # creating the board the user will see
            viewGrid(self.playerGrid)

            # taking input for playing the game
            # input should be in the form i,j,num
            inp = input()
            splitinp = inp.split(',')
            x = int(splitinp[0]) - 1
            y = int(splitinp[1]) - 1
            num = int(splitinp[2])

            if not math.isnan(self.playerGrid[x][y]):
                print('invalid guess position')
            elif num != self.answerGrid[x][y]:
                print('incorrect')
            else:
                empty -= 1
                self.playerGrid[x][y] = self.answerGrid[x][y]

            if empty <= 0:
                win = True

        print('You Win')

    def generate(self):
        while True:
            print(self.answerGrid)
            self.__fillGrid()


game = sudoku()
game.play('hard')
