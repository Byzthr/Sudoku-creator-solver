import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QFrame, QVBoxLayout, QGridLayout, QShortcut, QApplication
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QThread, QTimer, Qt
from numpy import ndarray


class SudokUI(QWidget):

    def __init__(self, sudoku: ndarray):

        super().__init__()

        self.initUI()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(125, 0, 125, 0)

        self.sudoku_grid = SudokuGrid(self, sudoku)

        head_text_label = QLabel('SUDOKU', self)
        head_text_label.setAlignment(Qt.AlignCenter)
        head_text_label.setStyleSheet('''
            font-size: 25px;
            border-style: solid;
            border-color: black;
            border-width: 1px;
            ''')

        # close_button = qt.QPushButton('Close', self)
        # close_button.clicked.connect(self.close)

        layout.addWidget(head_text_label, 30)
        layout.addWidget(self.sudoku_grid, 350)
        # layout.addWidget(close_button, 200)
        
    def initUI(self):

        self.setWindowTitle('Sudoku')
        self.setGeometry(200, 200, 600, 400)
        self.show()

    def update_matrix(self, sudoku):

        self.sudoku_grid.update_grid(sudoku)
        # QApplication.processEvents()
        # QThread.msleep(1)



class SudokuGrid(QFrame):

    def __init__(self, parent, sudoku):

        super().__init__(parent)

        self.sudoku = sudoku

        self.setGeometry(150, 30, 350, 350)
        self.setFixedSize(350, 350)
        self.setStyleSheet('background: white')

        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)

        self.create_grid(self.sudoku)
    
    def create_grid(self, sudoku):

        for i in range(3):
            for j in range(3):

                square = QFrame()
                square.layout = QGridLayout(square)
                square.layout.setSpacing(0)
                square.layout.setContentsMargins(0, 0, 0, 0)
                square.setStyleSheet('border-style: solid; border-color: black; border-width: 2px')
                self.paint_square(sudoku, square, i, j)
                self.layout.addWidget(square, i, j)

    def paint_square(self, sudoku, square, si, sj):

        for i in range(3):
            for j in range(3):
                if sudoku[3*si+i,3*sj+j] !=0: box = self.Box(self, str(sudoku[3*si+i,3*sj+j]))
                else: box = self.Box(self, ' ')
                square.layout.addWidget(box, i, j)

    def update_grid(self, sudoku: ndarray):

        self.sudoku = sudoku

        self.update()

    class Box(QLabel):

        def __init__(self, parent, text):

            super().__init__(text, parent)

            self.setAlignment(Qt.AlignCenter)
            self.setStyleSheet('''
                font-size: 25px;
                border-style: solid;
                border-color: black;
                border-width: 1px;
                background-color: white;
                ''')

        def mousePressEvent(self, ev):
            
            shortcuts = []
            self.setStyleSheet('''
                background-color: lightgrey;
                font-size: 25px;
                ''')
            for i in range(9):
                shortcuts.append(QShortcut(QKeySequence(str(i+1)), self, lambda n=1+1: self.set_number(n)))
            print('focus set')


        def set_number(self, n):

            self.setStyleSheet('''
                font-size: 25px;
                border-style: solid;
                border-color: black;
                border-width: 1px;
                ''')
            self.setText(str(n))
            print('number set')