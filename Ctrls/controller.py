###########################
# ctrls\controller.py #
###########################
import numpy as np
import PyQt5
from PyQt5 import QtGui, QtCore, QtWidgets
from hopfield import HopfieldNetwork
from Data.numbers_to_learn import numbers


class MainController(object):

    def __init__(self, model):
        self.model = model
    
    #### widget event functions ####
    def change_pushButton(self, checked):
        self.model.pushButton = checked
        print('DEBUG: change_pushButton called with arg value:', checked)
        
        if self.net:
            stable = self.net.asynchronous_presentation(self.model.epochs)
            self.update_items(self.net.x_y, self.net.x_y, self.net.outputs, stable)
            self.model.announce_update()

    def change_pushButton_2(self, checked):
        self.model.pushButton_2 = checked
        print('DEBUG: change_pushButton_2 called with arg value:', checked)
        
        if self.net:
            stable = self.net.synchronous_presentation(self.model.epochs)
            self.update_items(self.net.x_y, self.net.x_y, self.net.outputs, stable)
            self.model.announce_update()

    def change_pushButton_3(self, checked):
        self.model.pushButton_3 = checked
        print('DEBUG: change_pushButton_3 called with arg value:', checked)
        
        if self.model.gridLayoutWidget:
            self.net.dataset = [numbers[i] for i in np.sort(list(numbers.keys()))]
            stable = [None for i in range(len(self.net.dataset))]
            self.net.outputs = np.copy(self.net.dataset)
            self.update_items(self.net.x_y, self.net.x_y, self.net.dataset, stable) 
        else: 
            self.load_datas()
        
        self.model.announce_update()

    def change_checkBox(self, state):
        self.model.checkBox = state
        print('DEBUG: change_checkBox called with arg value:', state)


    def change_epochs(self, value):
        self.model.epochs = value
        print('DEBUG: change_epochs called with arg value:', value)
    
    def change_comboBox(self, index):
        self.model.comboBox = index
        print('DEBUG: change_comboBox called with arg value:', index)
    
    #################################################################################
    def load_datas(self):
        
        if self.model.comboBox == 1:
            datas = [numbers[i] for i in np.sort(list(numbers.keys()))]
            self.net = HopfieldNetwork(datas)
            self.net.init_weights_matrix()

            self.fill_layout(
                    self.net.x_y,
                    self.net.x_y,
                    datas, 
                    stability=[None for i in range(len(datas))])
        else:
            datas = []
            for root, dirs, files in walk("./inputs_img/"):
                for file in files: 
                    arr = Converter.img_to_array("./inputs_img/"+file)
                    array = np.concatenate(arr)
                    datas.append(array)
    
    #################################################################################
    def fill_layout(self, columns, rows, datas, stability):
        
        self.table = []
        self.item_list = []
        self.text = []
        self.datas = datas
        self.table_size = 9
        self.colors = {"blue": QtGui.QColor(0, 51, 51),
                       "white": QtGui.QColor(255, 255, 255)}

        self.model.gridLayoutWidget = QtWidgets.QWidget()
        self.model.gridLayout = QtWidgets.QGridLayout(self.model.gridLayoutWidget) 
        coordinates = [(i,j) for i in range(2) for j in range(5)]
    
        #fill layout with grids
        for i in range(len(self.datas)):    
            self.table.append(QtWidgets.QTableWidget(rows, columns, self.model.gridLayoutWidget))
            self.table[i].verticalHeader().setVisible(False)
            self.table[i].horizontalHeader().setVisible(False)
            
            for y in range(rows):
                self.table[i].setRowHeight(y, self.table_size)
            for x in range(columns):
                self.table[i].setColumnWidth(x, self.table_size)
            
            #assign items to each cell (required to colorize them)
            for row in range(rows):
                for column in range(columns):
                    item = QtWidgets.QTableWidgetItem()
                    self.table[i].setItem(row, column, item)
        
            self.text.append(QtWidgets.QLabel(self.model.gridLayoutWidget))
            self.text[i].setGeometry(QtCore.QRect(120,80,180,70))
            self.text[i].setText("Stability: {}".format(stability[i]))
        
            self.model.gridLayout.addWidget(self.table[i], coordinates[i][0],
                                                           coordinates[i][1])
            self.model.gridLayout.addWidget(self.text[i],  coordinates[i][0],
                                                           coordinates[i][1])
        self.update_items(rows, columns, datas, stability)
    
    
    #################################################################################
    def update_items(self, rows, columns, datas, stability):
        
        idx_gen = (i for i in range(len(datas)))
        
        for itm in self.model.gridLayoutWidget.children():
            if type(itm) == PyQt5.QtWidgets.QTableWidget:
                
                idx = next(idx_gen)
                #reshape vectors to make them fit to 
                #QTable widgets dimensions (which are organized as matrices).
                matrix = np.reshape(datas[idx], (rows, columns))
                
                #find coordinates
                white = np.where(matrix == -1)  
                blue = np.where(matrix == 1)
                
                for j in range(len(white[0])):
                    coordinates = (white[0][j], white[1][j])
                    itm.item(coordinates[0], coordinates[1]).setBackground(self.colors["white"]) 
                    
                for j in range(len(blue[0])):
                    coordinates = (blue[0][j], blue[1][j])
                    itm.item(coordinates[0], coordinates[1]).setBackground(self.colors["blue"]) 

            elif type(itm) == PyQt5.QtWidgets.QLabel:
                itm.setText("Stability: {}".format(stability[idx]))

