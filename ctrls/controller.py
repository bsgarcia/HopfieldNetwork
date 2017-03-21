###########################
# ctrls\controller.py #
###########################
import PyQt5
from PyQt5 import QtGui, QtCore, QtWidgets
from network.c_hopfield import HopfieldNetwork
from data.numbers_to_learn import nb_to_learn
from data.numbers_to_present import nb_to_present
from module.convert import Converter
from os import walk, getcwd, path
import numpy as np
import re


class MainController(object):
    def __init__(self, model):
        self.model = model
        if not path.isdir(".dont_show"):
            self.info_msgbox()

    #==================== info start up===============================================
    def info_msgbox(self):
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("Info")
        msgbox.setText("The network is able to learn two types of data:\n\n"
                       "---------------------------------------------------"
                       "----------------------------------- \n"
                       "Pictures\n"
                       "---------------------------------------------------"
                       "----------------------------------- \n"
                       "Pictures to learn are located in data/learn_img/ \n"
                       "Pictures to present are located in data/test_img/ \n"
                       "---------------------------------------------------"
                       "----------------------------------- \n\n"
                       "---------------------------------------------------"
                       "----------------------------------- \n"
                       "Numbers\n"
                       "---------------------------------------------------"
                       "----------------------------------- \n"
                       "Numbers to learn are located in data/numbers_to_learn.py \n"
                       "Numbers to present are located in data/numbers_to_present.py\n"
                       "---------------------------------------------------"
                       "----------------------------------- \n")
        
        dont_show = msgbox.addButton("Don't show this\nmessage anymore", 
                                    QtWidgets.QMessageBox.ActionRole)
        ok = msgbox.addButton("Ok", QtWidgets.QMessageBox.ActionRole)

        msgbox.exec_()
        
        if msgbox.clickedButton() == dont_show:
            from os import mkdir
            mkdir(".dont_show")
        else:
            pass

    #==================== error msg===============================================
    def error_msgbox(self):
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("Error")
        msgbox.setText("No pattern in memory! \nSelect images or numbers before!")
        msgbox.exec_()

    ### Widgets events ####
    #==================== synchronous update event ===============================
    def change_pushButton(self, checked): 
        self.model.pushButton = checked
        print('DEBUG: change_pushButton called with arg value:', checked)
        
        try:
            print("TEST!!!!!!!!!!!!!!!")
            try:
                print(self.old_matrix == self.net.w_matrix)
                stable = self.net.asynchronous_presentation(self.model.epochs,
                                                        self.model.comboBox_2,
                                                        self.model.checkBox)
                self.update(self.net.x_y, self.net.x_y, self.net.outputs, stable)
                self.model.announce_update()
        
            except:
                stable = self.net.asynchronous_presentation(self.model.epochs,
                                                        self.model.comboBox_2,
                                                        self.model.checkBox)
                self.update(self.net.x_y, self.net.x_y, self.net.outputs, stable)
                self.model.announce_update()
        
        except AttributeError:
            self.error_msgbox()    

    #==================== asynchronous update event ===============================
    def change_pushButton_2(self, checked):
        self.model.pushButton_2 = checked
        print('DEBUG: change_pushButton_2 called with arg value:', checked)
            
        try:
            stable = self.net.synchronous_presentation(self.model.epochs,
                                                       self.model.comboBox_2,
                                                       self.model.checkBox)
            self.update(self.net.x_y, self.net.x_y, self.net.outputs, stable)
            self.model.announce_update()
        
        except AttributeError:
            self.error_msgbox()

    #==================== load or reload data =====================================
    def change_pushButton_3(self, checked):
        self.model.pushButton_3 = checked
        print('DEBUG: change_pushButton_3 called with arg value:', checked)

        self.reset_data()

        self.load_data()
        self.model.announce_update()
    
    #==================== show learned patterns =====================================
    def change_pushButton_4(self, checked):
        self.model.pushButton_4 = checked
        print('DEBUG: change_pushButton_4 called with arg value:', checked)
        
        self.model.gridLayoutWidget_2 = QtWidgets.QWidget()
        self.model.gridLayout_2 = QtWidgets.QGridLayout(self.model.gridLayoutWidget_2)
        
        try:
            self.show_learned_patterns()   
            self.model.announce_update()
            self.model.gridLayout_2 = None
            self.model.gridLayoutWidget_2 = None
        
        except AttributeError:
            self.error_msgbox()

    #==================== unlearn button  ==========================================
    def change_pushButton_5(self, checked):
        self.model.pushButton_5 = checked
        print('DEBUG: change_pushButton_5 called with arg value:', self.model.pushButton_5)
        
        try:
            self.net.unlearn_pattern(self.net.outputs[self.model.comboBox_3])
            self.old_matrix = self.net.w_matrix.copy() 
            self.reset_data()
            self.load_data()
            self.net.w_matrix = self.old_matrix.copy()
            
            self.model.announce_update()
        
        except AttributeError:
            self.error_msgbox()
            
    #==================== force stability ==========================================
    def change_checkBox(self, state):
        self.model.checkBox = not self.model.checkBox 
        print('DEBUG: change_checkBox called with arg value:', self.model.checkBox)

    #==================== number of epochs =========================================
    def change_epochs(self, value):
        self.model.epochs = value
        print('DEBUG: change_epochs called with arg value:', value)

    #==================== type of learned pattern: images/numbers ==================
    def change_comboBox(self, index):
        self.model.comboBox = index
        print('DEBUG: change_comboBox called with arg value:', index)

    #==================== activation function choice ===============================
    def change_comboBox_2(self, index):
        self.model.comboBox_2 = index
        print('DEBUG: change_comboBox_2 called with arg value:', index)
    
    #====================  unlearn choice ==========================================
    def change_comboBox_3(self, index):
        self.model.comboBox_3 = index
        print('DEBUG: change_comboBox_3 called with arg value:', index)

    #===============================================================================
    def reset_data(self):
        self.model.gridLayout = None
        self.model.gridLayoutWidget = None
        self.model.gridLayout_2 = None
        self.model.gridLayoutWidget_2 = None

        self.init_main_layout()

    #===============================================================================
    def load_data(self):
        self.init_main_layout()
        
        if self.model.comboBox:
            self.mode = "numbers"
            self.load_numbers()
        else:
            self.mode = "img"
            self.load_images()

    #===============================================================================
    def load_numbers(self):
        data_to_learn = \
                [nb_to_learn[i].copy() for i in np.sort(list(nb_to_learn.keys()))]
        data_to_present = \
                [nb_to_present[i].copy() for i in np.sort(list(nb_to_present.keys()))]

        self.init_network(data_to_learn, data_to_present)
        self.model.pattern_to_present = self.net.outputs
        
        self.fill_layout_with_numbers(
            self.net.x_y,
            self.net.x_y,
            self.net.outputs,
            stability=[None for i in range(len(self.net.outputs))],
            layout=self.model.gridLayout,
            widget=self.model.gridLayoutWidget)

    #===============================================================================
    def load_images(self):
        data = self.import_images()
        self.init_network(data[0], data[1])
        
        self.fill_layout_with_images(
            data[2],
            stability=[None for i in range(len(data[2]))],
            layout=self.model.gridLayout)
        
    #===============================================================================
    def import_images(self):
        #load img to learn and store path in order to show them if 
        #learned patterns event is called
        path_list = []
        img_to_learn = []
        for root, dirs, files in walk("data/learn_img/"):
            for file in sorted(files):
                arr = Converter.img_to_array("data/learn_img/" + file)
                array = np.concatenate(arr)
                img_to_learn.append(array)
                img_path = Converter.array_to_img(array) 
                path_list.append(img_path)
        
        self.learned_path = path_list.copy()
        
        #load img to test + img to print in main window
        path_list = []
        img_to_present = []
        for root, dirs, files in walk("data/test_img/"):
            for file in sorted(files):
                arr = Converter.img_to_array("data/test_img/" + file)
                array = np.concatenate(arr)
                img_to_present.append(array)
                img_path = Converter.array_to_img(array)
                path_list.append(img_path)
        
        self.model.pattern_to_present = img_to_present.copy()
        
        return (img_to_learn, img_to_present, path_list)

    #===============================================================================
    def init_network(self, data_to_learn, data_to_present):
        self.net = HopfieldNetwork(data_to_learn, data_to_present)

    #===============================================================================
    def init_main_layout(self):
        self.model.gridLayoutWidget = QtWidgets.QWidget()
        self.model.gridLayout = QtWidgets.QGridLayout(
            self.model.gridLayoutWidget)
        if not self.model.comboBox:
            self.model.gridLayoutWidget.setStyleSheet(
                "border: 1px solid #5D5D5C;"
                "background: white")
    
    #===============================================================================
    def fill_layout_with_numbers(self, columns, rows, data, stability, layout, widget):
        table = []
        text =  []
        table_size = 15
        colors = {
            "blue": QtGui.QColor(36, 110, 189),
            "white": QtGui.QColor(255, 255, 255)
        }

        coordinates = [(x, y) for x in range(2) for y in range(5)]

        #fill layout with grids
        for i in range(len(data)):
            table.append(QtWidgets.QTableWidget(rows, columns))
            table[i].verticalHeader().setVisible(False)
            table[i].horizontalHeader().setVisible(False)

            for y in range(rows):
                table[i].setRowHeight(y, table_size)
            for x in range(columns):
                table[i].setColumnWidth(x, table_size)

            #assign items to each cell (required to colorize them)
            for row in range(rows):
                for column in range(columns):
                    item = QtWidgets.QTableWidgetItem()
                    table[i].setItem(row, column, item)

            text.append(QtWidgets.QLabel())
            text[i].setText("Pattern {}\nStability: {}".format(i, stability[i]))

            layout.addWidget(table[i], coordinates[i][0],coordinates[i][1])
            layout.addWidget(text[i], coordinates[i][0], coordinates[i][1])

        self.update_numbers(rows, columns, data, stability, widget)

    #===============================================================================
    def fill_layout_with_images(self, data, stability, layout):
        img = []
        text = []
        coord_img = [(x, y) for x in range(0, 5, 2) for y in range(0, 8, 2)]
        coord_text = [(x, y) for x in range(1, 6, 2) for y in range(0, 8, 2)]

        for i in range(len(data)):
            img.append(QtWidgets.QLabel())
            img[i].setPixmap(
                    QtGui.QPixmap(getcwd() + "/" + data[i]).scaled(200, 250))
            
            text.append(QtWidgets.QLabel())
            text[i].setText("Pattern {}\nStability: {}".format(i, stability[i]))

            layout.addWidget(img[i], coord_img[i][0],coord_img[i][1])
            layout.addWidget(text[i], coord_text[i][0], coord_text[i][1])

    #===============================================================================
    def update(self, rows, columns, data, stability):
        if self.mode == "numbers":
            self.update_numbers(rows, columns, data, stability, 
                                self.model.gridLayoutWidget)
        else:
            path_list = self.get_new_images(data)
            self.update_images(path_list, stability)

    #===============================================================================
    def update_numbers(self, rows, columns, data, stability, widget):
        idx_gen = (i for i in range(len(data)))
        colors = {
            "blue": QtGui.QColor(36, 110, 189),
            "white": QtGui.QColor(255, 255, 255)
        }

        for itm in widget.children():
            if type(itm) == PyQt5.QtWidgets.QTableWidget:
                idx = next(idx_gen)

                #reshape vectors to make them fit to 
                #QTable widgets dimensions (which are organized as matrices).
                matrix = np.reshape(data[idx], (rows, columns))

                #find coordinates
                white = np.where(matrix == -1)
                blue = np.where(matrix == 1)
                
                #colorize
                for j in range(len(white[0])):
                    coordinates = (white[0][j], white[1][j])
                    itm.item(coordinates[0],
                             coordinates[1]).setBackground(colors["white"])

                for j in range(len(blue[0])):
                    coordinates = (blue[0][j], blue[1][j])
                    itm.item(coordinates[0],
                             coordinates[1]).setBackground(colors["blue"])

            elif type(itm) == PyQt5.QtWidgets.QLabel:
                itm.setText("Pattern {}\nStability: {}".format(idx, stability[idx]))

    #===============================================================================
    def get_new_images(self, data):
        return list(Converter.array_to_img(i) for i in data)

    #===============================================================================
    def update_images(self, path_list, stability):
        i = 0
        idx_gen = (i for i in range(len(path_list)))

        for itm in self.model.gridLayoutWidget.children():
            i += 1
            if i % 2 == 0 and type(itm) == PyQt5.QtWidgets.QLabel:
                idx = next(idx_gen)
                itm.setPixmap(
                    QtGui.QPixmap(getcwd() + "/" + path_list[idx]).scaled(200, 250))

            if i % 2 != 0 and type(itm) == PyQt5.QtWidgets.QLabel:
                itm.setText("Pattern {}\nStability: {}".format(idx, stability[idx]))
    
    #===============================================================================
    def show_learned_patterns(self):
        if self.mode == "img":
            self.fill_layout_with_images(
                self.learned_path,
                stability=[None for i in range(len(self.learned_path))],
                layout=self.model.gridLayout_2)
            
            self.model.gridLayoutWidget_2.setStyleSheet(
                    "border: 1px solid #5D5D5C;"
                    "background: white")
        else:
            self.fill_layout_with_numbers(
                self.net.x_y,
                self.net.x_y,
                self.net.dataset,
                stability=[None for i in range(len(self.net.dataset))],
                layout=self.model.gridLayout_2,
                widget=self.model.gridLayoutWidget_2)
        
 
