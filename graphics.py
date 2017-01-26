import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QWidget, QApplication, QTableWidget,
                                QTableWidgetItem, QGridLayout)
import PyQt5.Qt
import numpy as np

class Window(QWidget):
    def __init__(self, rows, columns, datas):
        super(Window, self).__init__()
        
        self.table = []
        self.item_list = []
        self.datas = datas
        self.table_size = 9
        self.colors = {"blue" : QtGui.QColor(0, 51, 51),
                      "white" : QtGui.QColor(255, 255, 255)
                      }
        
        layout = QGridLayout(self)

        for i in range(len(self.datas)):
            self.table.append(QTableWidget(rows, columns, self))
            self.table[i].verticalHeader().setVisible(False)
            self.table[i].horizontalHeader().setVisible(False)
            
            for y in range(rows):
                self.table[i].setRowHeight(y, self.table_size)
            for x in range(columns):
                self.table[i].setColumnWidth(x, self.table_size)
            
            for row in range(rows):
                for column in range(columns):
                    item = QTableWidgetItem()
                    self.table[i].setItem(row, column, item)
        
            self.color_items(i, rows, columns)
            
            layout.addWidget(self.table[i])
            
        self.show()


    def color_items(self, i, rows, columns):
        
        matrix = np.reshape(self.datas[i], (rows, columns))
        
        white = np.where(matrix == -1)  
        blue = np.where(matrix == 1)
        
        for j in range(len(white[0])):
            coordinates = (white[0][j], white[1][j])
            self.table[i].item(coordinates[0], coordinates[1]).setBackground(self.colors["white"]) 
            
        for j in range(len(blue[0])):
            coordinates = (blue[0][j], blue[1][j])
            self.table[i].item(coordinates[0], coordinates[1]).setBackground(self.colors["blue"]) 



def run(datas):
   
    app = QApplication(sys.argv)
    window = Window(6, 6, datas)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



