import os


class Cell:
    def __init__(self):
        self.value = 0
        self.solved = False
        self.empty = True
        self.impossibleValues = set()
    # fills the cell with a temporary/test value
    def Fill(self, val):
        self.value = val
        self.empty = False
        self.impossibleValues.add(val)
        ## uncomment line below to watch the algorithm solve
        #self.PrintSudoku(0);
    # fills cell with value but leaves 'empty' var as false
    def FillEmpty(self, val):
        self.value = val
        self.empty = True
    # fills cell with a permemnant value - for use when filling given values from puzzle
    def FillPerm(self, val):
        self.value = val
        self.solved = True
        self.empty = False
    # Empties cell and impossible values set, also sets value to 0
    def Empty(self):
        self.value = 0
        self.empty = True
        self.impossibleValues.clear()


class Puzzle:

    def __init__(self):
        self.solved = False
        self.sudoku = [[Cell() for x in range(9)] for x in range(9)]

    def FillSudoku(self, sudokuArrIn):
        for x in range(9):
            for y in range(9):
                if sudokuArrIn[x][y] == 0:
                    self.sudoku[x][y].FillEmpty(sudokuArrIn[x][y])
                else:
                    self.sudoku[x][y].FillPerm(sudokuArrIn[x][y])
    #checks all cells are full
    def CheckSudokuComplete(self):
        if self.solved == False:
            # PrintSudoku();
            for x in range(9):
                if self.solved == True:
                    break;
                for y in range(9):
                    if self.solved == True:
                        break;
                    if (self.sudoku[x][y].value == 0):
                        return False;
        self.PrintSudoku(1);
        self.solved = True;
        return True;
    # prints all values to console
    def PrintSudoku(self, mode):
        if self.solved == False:
            if mode == 0:
                os.system("cls")
            for i in range(9):

                print("\n");
                for x in range(9):
                    print(self.sudoku[i][x].value, "   ", end="")
                    x += 1;
                i += 1;
            print("\n")

    # calls SolveSudoku() funct until sudoku is solved
    def SolveSudokuInit(self):
        while self.CheckSudokuComplete() == False:
            self.SolveSudoku();
    # checks sudoku from [0][0] and when finding an empty value calls CheckCell() on that value
    def SolveSudoku(self):
        for x in range(9):
            if (self.solved == True):
                break
            for y in range(9):
                if self.solved == True:
                    break
                if (self.sudoku[x][y].empty == True):
                    if self.CheckCell(x, y) == 1:
                        if self.BackTrack(x, y) == 1:
                            return 1;

    # check if 3x3 grid contains 'value' arg
    # returns False if value argument exists in col
    # returns True if not
    def Check3x3(self, row, column, value):
        rowStart = row - (row % 3);
        colStart = column - (column % 3);
        rowCurr = rowStart;
        collCurr = colStart;
        for x in range(3):
            collCurr = colStart;
            for y in range(3):
                if self.sudoku[row][column] == value or self.sudoku[rowCurr][collCurr].empty == False:
                    continue;
                    if self.sudoku[rowCurr][colCurr].value == value and self.sudoku[rowCurr][colCurr].empty == True:
                        return False;
                colCurr += 1;
            rowCurr += 2;
        return True
    def Fill(self, row, col, val):
        #call fill on the current cell
        self.sudoku[row][col].Fill(val)
        ##uncomment below line to watch program solve puzzle
        #self.PrintSudoku(0)

    # check if row contains 'value' arg
    # returns False if value argument exists in Row
    # returns True if not
    def CheckRow(self, row, column, value):
        for x in range(9):
            if (x == column) or (self.sudoku[row][x].empty == True):
                continue;
            if self.sudoku[row][x].value == value:
                return False;
        return True;

    # checks column of puzzle for 'value' arg
    # returns False if value argument exists in Col
    # returns True if not
    def CheckCol(self, row, column, value):
        for x in range(9):
            if (x == row) or (self.sudoku[x][column].empty == True):
                continue;
            if self.sudoku[row][x].value == value:
                return False;

    # fills the cell at [row, column]'s impossibleValues set with all values currently in the same row, column or 3x3 grid
    def FillExistingVals(self, row, column):
        for x in range(9):
            if (x == column) or (self.sudoku[row][x].empty == True):
                continue;
            else:

                self.sudoku[row][column].impossibleValues.add(self.sudoku[row][x].value);
        # all values in column
        for x in range(9):
            if (x == row) or (self.sudoku[x][column].empty == True):
                continue;
            else:

                self.sudoku[row][column].impossibleValues.add(self.sudoku[x][column].value);
        # check3x3
        rowStart = row - (row % 3);
        colStart = column - (column % 3);
        rowCurr = rowStart;
        colCurr = colStart;
        for x in range(3):
            colCurr = colStart;
            for y in range(3):
                if self.sudoku[rowCurr][colCurr].empty == False:
                    self.sudoku[row][column].impossibleValues.add(self.sudoku[rowCurr][colCurr].value);
                colCurr += 1;
            rowCurr += 1;

    # returns True if 'x' is already in possible values
    def CheckPossVals(self, row, column, x):
        setSample = set();
        setSample.add(x);
        if len(setSample.intersection(self.sudoku[row][column].impossibleValues)) > 0:
            return True;
        else:
            return False;

    # enters values in the cell if they do not break constraints
    # returns 1 if cannot enter another number and Backtrack() is called from SolveSudoku()
    def CheckCell(self, row, column):
        numberEntered = False;
        seq = [1, 2, 3, 4, 5, 6, 7, 8, 9];
        self.FillExistingVals(row, column);

        for x in range(9):
            if self.CheckPossVals(row, column, seq[x]) == False:
                
                numberEntered = True;
                self.Fill(row, column, seq[x]);
                break;
        if (numberEntered == False):
            if self.solved == False:
                return 1;
        else:
            if row == 8 & column == 8:
                return 0;

    # if (output is SolveSudoku) return 1;
    def BackTrack(self, row, column):
        # if the current cell is a permFilled
        # step back and recur on BackTrack()
        if self.sudoku[row][column].solved == True:
            if (column - 1 >= 0):
                column -= 1;
            else:
                if row - 1 >= 0:
                    row -= 1;
                    column = 8;
            if self.BackTrack(row, column) == 1:
                return 1;
        # checks if all values have been tried for that cell
        if len(self.sudoku[row][column].impossibleValues) == 9:
            self.sudoku[row][column].Empty();
            if (column - 1 >= 0):
                column -= 1;
            else:
                if row - 1 >= 0:
                    row -= 1;
                    column = 8;
            if self.BackTrack(row, column) == 1:
                return 1;
        # if all constraint appr values have not been tried:
        #   clears cell to try another value
        #   returns 1
        else:
            self.sudoku[row][column].value = 0;
            self.sudoku[row][column].empty = True;
            return 1;


p = Puzzle();
# sudoku 1
p.sudoku[0][1].FillPerm(8);
p.sudoku[0][5].FillPerm(2);
p.sudoku[0][8].FillPerm(5);
p.sudoku[1][0].FillPerm(9);
p.sudoku[1][3].FillPerm(7);
p.sudoku[1][6].FillPerm(1);
p.sudoku[1][7].FillPerm(4);
p.sudoku[2][1].FillPerm(1);
p.sudoku[2][2].FillPerm(3);
p.sudoku[2][3].FillPerm(8);
p.sudoku[2][6].FillPerm(9);
p.sudoku[3][2].FillPerm(9);
p.sudoku[3][3].FillPerm(5);
p.sudoku[3][6].FillPerm(8);
p.sudoku[3][7].FillPerm(6);
p.sudoku[3][8].FillPerm(1);
p.sudoku[4][0].FillPerm(2);
p.sudoku[4][5].FillPerm(4);
p.sudoku[5][2].FillPerm(1);
p.sudoku[5][5].FillPerm(7);
p.sudoku[6][5].FillPerm(9);
p.sudoku[6][6].FillPerm(3);
p.sudoku[6][7].FillPerm(8);
p.sudoku[7][1].FillPerm(3);
p.sudoku[7][8].FillPerm(9);
p.sudoku[8][0].FillPerm(8);
p.sudoku[8][7].FillPerm(7);

# #'hard' puzzle
hard = Puzzle();
hard.sudoku[0][3].FillPerm(6);
hard.sudoku[0][7].FillPerm(1);
hard.sudoku[1][1].FillPerm(1);
hard.sudoku[1][4].FillPerm(5);
hard.sudoku[2][0].FillPerm(9);
hard.sudoku[2][2].FillPerm(4);
hard.sudoku[2][3].FillPerm(2);
hard.sudoku[2][8].FillPerm(7);
hard.sudoku[3][1].FillPerm(3);
hard.sudoku[3][5].FillPerm(2);
hard.sudoku[4][0].FillPerm(2);
hard.sudoku[4][1].FillPerm(6);
hard.sudoku[4][3].FillPerm(1);
hard.sudoku[4][5].FillPerm(8);
hard.sudoku[4][7].FillPerm(7);
hard.sudoku[4][8].FillPerm(3);
hard.sudoku[5][3].FillPerm(7);
hard.sudoku[5][7].FillPerm(8);
hard.sudoku[6][0].FillPerm(4);
hard.sudoku[6][5].FillPerm(7);
hard.sudoku[6][6].FillPerm(3);
hard.sudoku[6][8].FillPerm(1);
hard.sudoku[7][4].FillPerm(9);
hard.sudoku[7][7].FillPerm(5);
hard.sudoku[8][1].FillPerm(8);
hard.sudoku[8][5].FillPerm(6);

evil = Puzzle();
# 'evil' puzzle
evilArr = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 2, 8, 3, 6, 0, 0],
           [0, 1, 0, 0, 0, 0, 8, 2, 0],
           [0, 0, 0, 9, 2, 5, 0, 7, 0],
           [0, 2, 0, 0, 0, 0, 0, 3, 0],
           [0, 8, 0, 4, 3, 7, 0, 0, 0],
           [0, 3, 9, 0, 0, 0, 0, 6, 0],
           [0, 0, 4, 8, 7, 1, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0]
           ]

evil.FillSudoku(evilArr)

p.PrintSudoku(1)
p.SolveSudokuInit()
p.PrintSudoku(0)
x = input()

hard.PrintSudoku(0)
hard.SolveSudokuInit();
hard.PrintSudoku(1);
x = input()

evil.PrintSudoku(0)
evil.SolveSudokuInit();
evil.PrintSudoku(1);
x = input()