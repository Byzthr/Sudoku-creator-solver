from time import time
import numpy as np
from numpy.random import randint
from numpy import ndarray
MAX_TRIES: int = 1000



class SudokuTry(ndarray):
    
    ''' A 9x9 np.ndarray that tries to respect sudokus properties. '''

    max_it = 100

    def __new__(cls, to_solve_sudoku: ndarray = np.zeros((9,9), dtype = int)):

        obj = np.copy(to_solve_sudoku).view(cls)
        obj.valid = False
        antirepeat = obj.analyze_sudoku_V1()

        # SudokuTry.print_array(antirepeat)
        
        missed = obj.define_boxes_V1(antirepeat)
        # print(obj)
        if not missed: obj.valid = True

        return obj

    def __array_finalize__(self, obj):

        if obj is None: return

    def analyze_sudoku_V1(self):

        ''' Runs through the matrix finding filled boxes and deleting those from the antirepeat.
            Returns prepared antirepeat. '''

        antirepeat = SudokuTry.AntirepeaterList()

        for i in range(9):
            for j in range(9):
                k = SudokuTry.define_k(i,j)

                if (n := self[i,j]) != 0:
                    antirepeat[0][i].remove(n)
                    antirepeat[1][j].remove(n)
                    antirepeat[2][k].remove(n)

        return antirepeat

    def analyze_sudoku_V2(self):

        ''' Same function as V1. This time coordinates from the filled boxes
            are processed with NumPy only those are called.
            Very similar performance (maybe a bit worse). '''

        antirepeat = SudokuTry.AntirepeaterList()
        presudoku_coords = np.where(self!=0)

        for i,j in zip(presudoku_coords[0], presudoku_coords[1]):
            k = SudokuTry.define_k(i,j)
            n = self[i,j]
            antirepeat[0][i].remove(n)
            antirepeat[1][j].remove(n)
            antirepeat[2][k].remove(n)


    def define_boxes_V1(self, antirepeat):

        ''' Defines sudoku's boxes until getting it or failing in one of them. '''

        for j in range(9):
            for i in range(9):
                if self[j,i] != 0: continue
                k = SudokuTry.define_k(i,j)
                antirepeat, self[j,i], missed = SudokuTry.place_number_V1(i, j, k, antirepeat)
                if missed: return 1

        return 0

    @classmethod
    def place_number_V1(cls, i, j, k, antirepeat):

        ''' Finds an available number for a box (it's in its 3 corresponding antirepeater sublists).
            Then it deletes it from them. '''

        if len(antirepeat[0][i])==1: random_index = 0
        else: random_index = randint(len(antirepeat[0][i]))

        it = 0
        while ((n := antirepeat[0][i][random_index]) not in antirepeat[1][j] or n not in antirepeat[2][k]) and (it<SudokuTry.max_it):
            random_index = randint(len(antirepeat[0][i]))
            it+=1
        if it >= SudokuTry.max_it: 
            return antirepeat, 0, 1

        antirepeat[0][i].remove(n)
        antirepeat[1][j].remove(n)
        antirepeat[2][k].remove(n)

        return antirepeat, n, 0

# Para la version mejorada

    def define_boxes_V2(self, antirepeat, presudoku_coords):

        ''' Evolution of V1. This time numbers on the last square of each row are saved and put first in the next row. '''

        for j in range(9):
            for i in range(9):
                if self[j,i] != 0: continue
                k = SudokuTry.define_k(i,j)

                antirepeat, self[j,i], missed = SudokuTry.place_number_V2(i, j, k, antirepeat)
                if (i+1)%3!=0 and (k+1)%3==0:
                    antirepeat[0][i][antirepeat[0][i].index(self[j,i])]

                if missed: return 1

        return 0

    @classmethod
    def place_number_V2(cls, i, j, k, antirepeat):

        ''' Modded version for define_box_V2. '''

        if len(antirepeat[0][i])==1: random_index = 0
        else: random_index = randint(len(antirepeat[0][i]))

        it = 0
        while ((n := antirepeat[0][i][random_index]) not in antirepeat[1][j] or n not in antirepeat[2][k]) and (it<SudokuTry.max_it):
            random_index = randint(len(antirepeat[0][i]))
            it+=1
        if it >= SudokuTry.max_it: 
            return antirepeat, 0, 1

        antirepeat[0][i].remove(n)
        antirepeat[1][j].remove(n)
        antirepeat[2][k].remove(n)

        return antirepeat, n, 0

    @classmethod
    def print_array(cls, arr: ndarray):

        ''' Method intended uniquely to print an antirepeat array '''

        print('\nRow:')
        for ar in arr[0]:
            print(ar)

        print('\nColumn:')
        for ar in arr[1]:
            print(ar)

        print('\nSquare')
        for ar in arr[2]:
            print(ar)

    @classmethod
    def define_k(cls, i: int, j: int) -> int:

        ''' Returns the square in which a box is. '''

        if i<3:
            if j<3: return 0
            if j<6: return 1
            if j<9: return 2
        if i<6:
            if j<3: return 3
            if j<6: return 4
            if j<9: return 5
        if i<9:
            if j<3: return 6
            if j<6: return 7
            if j<9: return 8


    class AntirepeaterList(list):

        ''' 3 component list each of which contains 9 [1 to 9] lists.
            Each main component corresponds to rows, columns and squares numbers respectively.
            Numbers from the lists are used in a sudoku and then eliminated so it does not appear more than one time. '''

        def __init__(self):

            for i in range(3):
                self.append([])

                for j in range(9):
                    self[i].append([])

                    for n in range(1,10):
                        self[i][j].append(n)


class Sudoku(SudokuTry):

    ''' Valid Sudoku. Tries SudokuTry's until it gets a valid one.
        It returns the sudokus matrix and the tries taken. '''

    def __new__(cls, start_time: float, to_solve_sudoku: ndarray = np.zeros((9,9), dtype=int), max_tries: int = MAX_TRIES):

        obj = SudokuTry().view(cls)
        obj.start_time = start_time
        sudoku_info = obj.get_sudoku(to_solve_sudoku, max_tries)
        obj = sudoku_info[0].view(cls)
        obj.tries = sudoku_info[1]
        print(f'{obj.tries/(time()-start_time)} tries/s')
        return obj

    def get_sudoku(self, to_solve_sudoku: ndarray, max_tries: int):

        ''' Sudoku try loop. '''

        tries: int = 0
        while not (sudoku := SudokuTry(to_solve_sudoku)).valid:
            tries += 1
            print_progress_bar(tries, max_tries)
            # print(sudoku)
            if tries >= max_tries: raise TryLimitExceded(self.start_time, tries)
        print('\n')

        return sudoku, tries


class PreparedSudoku(ndarray):

    ''' Selects a 'difficulty' number of boxes from each row and
        creates a new array with those boxes' values and returns it. '''

    def __new__(cls, sudoku: Sudoku, difficulty: int):
        obj = np.zeros((9,9), dtype=int).view(cls)
        shown_coords = obj.get_coordinates(difficulty)
        obj = obj.array_init(sudoku, shown_coords)

        return obj

    def __array_finalize__(self, obj):
        if obj is None: return

    def get_coordinates(self, difficulty):

        ''' Random coordinates. '''

        shown_numbers_number = 9*difficulty
        numbers_per_row = difficulty
        shown_coords = [[],[]]
        antirepeat = [0,1,2,3,4,5,6,7,8]*difficulty

        for i in range(shown_numbers_number):
            shown_coords[0].append(int(i/numbers_per_row))
            if i!=shown_numbers_number-1: jcoord = antirepeat.pop(randint(shown_numbers_number-1-i))
            else: jcoord = antirepeat.pop(0)
            shown_coords[1].append(jcoord)

        return shown_coords

    def array_init(self, sudoku, shown_coords):

        ''' New array construction. '''

        prepared_sudoku = np.zeros((9,9), dtype=int)
        for i,j in zip(shown_coords[0], shown_coords[1]):
            prepared_sudoku[i][j] = sudoku[i][j]

        return prepared_sudoku


class TryLimitExceded(Exception):

    ''' Exception to raise when a sudoku object loops through too many sudoku tries. '''

    def __init__(self, start_time: float, tries: int):

        self.tries = tries
        execution_time = time() - start_time
        print('\n')
        print('Execution time: %.4f' % execution_time)
        print(f'{tries/execution_time} tries/s')
        super().__init__(f'| Overpassed try limit: {tries} tries | Execution time: {execution_time} s')


def print_progress_bar(iteration: int, total: int, length: int = 100):

    ''' Sudoku tries progress bar printing. '''

    # percent = ('{0:.1f}').format(100*(iteration/float(total)))
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\rTry progress: |{bar}| {iteration}/{total} tries', end = '\r')
