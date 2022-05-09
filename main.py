from sudoku_generator import Sudoku, PreparedSudoku, SudokuTry
from interface_sdk import SudokUI
from time import time
import sys
from PyQt5.QtWidgets import QApplication
import numpy as np

MAX_TRIES: int = 1000

def get_sudoku():

    generation_start_time = time()
    
    app = QApplication(sys.argv)

    sudoku = Sudoku(generation_start_time, max_tries=10000)
    tries = sudoku.tries
    ui = SudokUI(sudoku)
    ui.show()
    

    prepared_sudoku = PreparedSudoku(sudoku, 1)
    ui = SudokUI(prepared_sudoku)
    ui.show()

    print('======================================================')
    print(f'Sudoku generation time: {time()-generation_start_time}')
    print(f'Sudoku - {tries} attempts:\n{sudoku}')
    print(f'Prepared sudoku:\n{prepared_sudoku}\n')

    ui.show()
    app.exec()

    return prepared_sudoku

def solve_sudoku(sudoku: Sudoku):

    solving_start_time = time()

    solved_sudoku = Sudoku(solving_start_time, to_solve_sudoku=sudoku, max_tries=100000)
    solve_tries = solved_sudoku.tries

    print('-----------------------------------------------------')
    print(f'Solving time: {time()-solving_start_time}s')
    print(f'Solved sudoku - {solve_tries} attempts:\n{solved_sudoku}\n')

    app = QApplication(sys.argv)
    interface = SudokUI(solved_sudoku)
    interface.show()
    app.exec()

    return solved_sudoku

def solve_extern_sudoku():

    extern_sudoku = np.array([
                   [5,3,0,0,7,0,0,0,0],
                   [6,0,0,1,9,5,0,0,0],
                   [0,9,8,0,0,0,0,6,0],
                   [8,0,0,0,6,0,0,0,3],
                   [4,0,0,8,0,3,0,0,1],
                   [7,0,0,0,2,0,0,0,6],
                   [0,6,0,0,0,0,2,8,0],
                   [0,0,0,4,1,9,0,0,5],
                   [0,0,0,0,8,0,0,7,9] 
    ])

    extern_sudoku_2 = np.array([
                   [0,0,0,0,6,0,0,9,3],
                   [0,8,0,0,0,7,4,0,0],
                   [0,0,3,0,0,0,0,6,8],
                   [0,0,0,0,2,3,0,0,0],
                   [1,9,0,4,0,5,0,3,7],
                   [0,0,0,1,7,0,0,0,0],
                   [8,7,0,0,0,0,6,0,0],
                   [0,0,1,8,0,0,0,7,0],
                   [4,6,0,0,9,0,0,0,0] 
    ])
    
    solving_start_time = time()

    solved_extern_sudoku = Sudoku(solving_start_time, to_solve_sudoku=extern_sudoku_2, max_tries=1000000)
    solve_tries = solved_extern_sudoku.tries

    print('-----------------------------------------------------')
    print(f'Solving time: {time()-solving_start_time}')
    print(f'Solved sudoku - {solve_tries} attempts:\n{solved_extern_sudoku}')

    app = QApplication(sys.argv)
    interface = SudokUI(solved_extern_sudoku)
    interface.show()
    app.exec()


def main():

    sudoku = get_sudoku()

    for i in range(1): solve_sudoku(sudoku)

    # solve_extern_sudoku()

    return 0


class MainError(Exception):

    def __init__(self):

        super().__init__('Failed execution')


if __name__=='__main__':

    if main(): raise MainError()
        
    print("Executed succesfully")
