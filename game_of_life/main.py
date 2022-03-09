from PyQt5.QtWidgets import QMainWindow, QFrame, QGridLayout, QColumnView, QPushButton, QApplication
import sys
import numpy as np
    
    
class GameOfLifeUI(QMainWindow):
    def __init__(self, frame, number_of_lines, number_of_columns):
        super().__init__()
        
        # We get the parameters of the frame to do the modifications on the interface after
        self.frame = frame
        self.number_of_lines = number_of_lines
        self.number_of_columns = number_of_columns
        
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("Game of Life")
        
        # This line allows to create a layout
        self.setCentralWidget(QFrame())
        
        # We create a grid layout because it corresponds with the matrix named frame and we remove the spaces 
        # between the cells
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        
        for i in range(0, number_of_lines):
            for j in range(0, number_of_columns):
                
                # We add ColumnView widgets in the grid because it will look like cells
                cell = QColumnView()
                
                # If a cell is alive, we color it in black
                if frame[i][j] == 1:
                    cell.setStyleSheet("background-color: black")
                    
                self.grid.addWidget(cell, i, j)      
        
        # We create a button "Next frame" that actualises the frame when it's clicked         
        button = QPushButton(self)
        button.setText("Next frame")
        button.clicked.connect(lambda: self.set_frame(compute_next_frame(self.frame)))
                 
        self.centralWidget().setLayout(self.grid)    

    
    def set_frame(self, frame):
        # Actualise the frame of the object that is used
        self.frame = frame
        
        for i in range(0, self.number_of_lines):
            for j in range(0, self.number_of_columns):
                
                # Get the cell at position (i, j)
                cell = self.grid.itemAtPosition(i, j).widget()
                
                # Changes black cells that have to be white
                if frame[i][j] == 0 and "black" in cell.styleSheet():
                    new_cell = QColumnView()
                    self.grid.replaceWidget(cell, new_cell)
                  
                # Changes white cells that have to be black    
                elif frame[i][j] == 1 and "black" not in cell.styleSheet():
                    new_cell = QColumnView()
                    new_cell.setStyleSheet("background-color: black")
                    self.grid.replaceWidget(cell, new_cell)
                    
                    

frame = np.array([[0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,1,1,0,0,0],
                  [0,0,1,1,0,0,0],
                  [0,0,0,1,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0]])

number_of_lines = frame.shape[0]
number_of_columns = frame.shape[1]


def compute_number_neighbors(paded_frame, index_line, index_column):
    number_neighbors = 0
    
    # We do this because we use the paded frame in this method
    index_line += 1
    index_column += 1
    
    for idx_line in range((index_line - 1), (index_line + 2)):
        for idx_col in range((index_column - 1), (index_column + 2)): 
            if idx_line != index_line or idx_col != index_column:
                number_neighbors += paded_frame[idx_line][idx_col]       
                
    return number_neighbors
        

def compute_next_frame(frame):
    # paded_frame allows to avoid errors from the size of the matrix and keep the original frame to count the number
    # of neighbors
    paded_frame = np.pad(frame, 1, mode="constant")
    
    global number_of_lines 
    global number_of_columns
    
    for idx_line in range(0, number_of_lines):
        for idx_col in range(0, number_of_columns):
            
            number_neighbors = compute_number_neighbors(paded_frame, idx_line, idx_col)
            
            # We apply the rules of the game of life
            if frame[idx_line][idx_col] == 0 and number_neighbors == 3:
                frame[idx_line][idx_col] = 1
            elif frame[idx_line][idx_col] == 1 and (number_neighbors < 2 or number_neighbors > 3):
                frame[idx_line][idx_col] = 0  
    
    return frame
        

# This bloc opens a window with a game of life        
app = QApplication(sys.argv)
window = GameOfLifeUI(frame, number_of_lines, number_of_columns)
window.show()
sys.exit(app.exec_())  