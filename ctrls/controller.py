###########################
# ctrls\controller.py #
###########################
import PyQt5
from PyQt5 import QtGui, QtCore, QtWidgets
from network.c_hopfield import HopfieldNetwork
from data.numbers_to_learn import numbers
from module.convert import Converter
from os import walk, getcwd
import numpy as np


class MainController(object):
    def __init__(self, model):
        self.model = model

    #### widget event functions ####
    def change_pushButton(self, checked):
        self.model.pushButton = checked
        print('DEBUG: change_pushButton called with arg value:', checked)

        if self.net:
            stable = self.net.asynchronous_presentation(self.model.epochs,
                                                        self.model.comboBox_2)
            self.update(self.net.x_y, self.net.x_y, self.net.outputs, stable)
            self.model.announce_update()

    def change_pushButton_2(self, checked):
        self.model.pushButton_2 = checked
        print('DEBUG: change_pushButton_2 called with arg value:', checked)

        if self.net:
            stable = self.net.synchronous_presentation(self.model.epochs,
                                                       self.model.comboBox_2)
            self.update(self.net.x_y, self.net.x_y, self.net.outputs, stable)
            self.model.announce_update()

    def change_pushButton_3(self, checked):
        self.model.pushButton_3 = checked
        print('DEBUG: change_pushButton_3 called with arg value:', checked)

        if self.model.gridLayoutWidget:
            self.reset_datas()

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

    def change_comboBox_2(self, index):
        self.model.comboBox_2 = index
        print('DEBUG: change_comboBox_2 called with arg value:', index)

    #===============================================================================#
    def reset_datas(self):
        del self.model.gridLayout
        del self.model.gridLayoutWidget
        self.init_layout()

    #===============================================================================#
    def load_datas(self):
        self.init_layout()

        if self.model.comboBox == 1:
            self.mode = "numbers"
            self.load_numbers()
        else:
            self.mode = "img"
            self.load_images()

    #===============================================================================#
    def load_numbers(self):
        datas = [numbers[i].copy() for i in np.sort(list(numbers.keys()))]
        self.init_network(datas)

        self.fill_layout_with_numbers(
            self.net.x_y,
            self.net.x_y,
            datas,
            stability=[None for i in range(len(datas))])

    #===============================================================================#
    def load_images(self):
        datas_to_learn = []
        img_to_print = []

        for root, dirs, files in walk("data/inputs_img/"):
            for file in files:
                arr = Converter.img_to_array("data/inputs_img/" + file)
                array = np.concatenate(arr)
                img_path = Converter.array_to_img([array])
                datas_to_learn.append(array)
                img_to_print.append(img_path)
        # for root, dirs, files in walk("data/test_img/"):
            # for file in files:
                # arr = Converter.img_to_array("data/test_img/" + file)
                # array = np.concatenate(arr)
                # img = Converter.array_to_img([array])
                # img_to_print.append()
        
        self.init_network(datas_to_learn)

        self.fill_layout_with_images(
            self.net.x_y,
            self.net.x_y,
            img_to_print,
            stability=[None for i in range(len(img_to_print))])

    #===============================================================================#
    def init_network(self, datas):
        self.net = HopfieldNetwork(datas)
        self.net.init_weights_matrix()

    #===============================================================================#
    def init_layout(self):
        self.model.gridLayoutWidget = QtWidgets.QWidget()
        self.model.gridLayout = QtWidgets.QGridLayout(
            self.model.gridLayoutWidget)
        if not self.model.comboBox:
            self.model.gridLayoutWidget.setStyleSheet(
                "border: 1px solid #5D5D5C;"
                "background: white")

    #===============================================================================#
    def fill_layout_with_numbers(self, columns, rows, datas, stability):
        table = []
        text =  []
        table_size = 9
        colors = {
            "blue": QtGui.QColor(0, 51, 51),
            "white": QtGui.QColor(255, 255, 255)
        }

        coordinates = [(i, j) for i in range(2) for j in range(5)]

        #fill layout with grids
        for i in range(len(datas)):
            table.append(
                QtWidgets.QTableWidget(rows, columns,
                                       self.model.gridLayoutWidget))
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

            text.append(QtWidgets.QLabel(self.model.gridLayoutWidget))
            text[i].setText("Stability: {}".format(stability[i]))

            self.model.gridLayout.addWidget(table[i], coordinates[i][0],
                                            coordinates[i][1])
            self.model.gridLayout.addWidget(text[i], coordinates[i][0],
                                            coordinates[i][1])

        self.update_numbers(rows, columns, datas, stability)

    #===============================================================================#
    def fill_layout_with_images(self, columns, rows, datas, stability):
        img = []
        text = []
        coord_img = [(i, j) for i in range(0, 5, 2) for j in range(0, 8, 2)]
        coord_text = [(i, j) for i in range(1, 6, 2) for j in range(0, 8, 2)]

        for i in range(len(datas)):
            img.append(QtWidgets.QLabel())
            img[i].setPixmap(
                QtGui.QPixmap(getcwd() + "/" + datas[i]).scaled(100, 120))
            img[i].setGeometry(10, 10, 200, 240)

            text.append(QtWidgets.QLabel())
            text[i].setText("Stability: {}".format(stability[i]))

            self.model.gridLayout.addWidget(img[i], coord_img[i][0],
                                            coord_img[i][1])
            self.model.gridLayout.addWidget(text[i], coord_text[i][0],
                                            coord_text[i][1])

    #===============================================================================#
    def update(self, rows, columns, datas, stability):
        if self.mode == "numbers":
            self.update_numbers(rows, columns, datas, stability)
        else:
            self.update_images(rows, columns, datas, stability)

    #===============================================================================#
    def update_numbers(self, rows, columns, datas, stability):
        idx_gen = (i for i in range(len(datas)))
        colors = {
            "blue": QtGui.QColor(0, 51, 51),
            "white": QtGui.QColor(255, 255, 255)
        }

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
                    itm.item(coordinates[0],
                             coordinates[1]).setBackground(colors["white"])

                for j in range(len(blue[0])):
                    coordinates = (blue[0][j], blue[1][j])
                    itm.item(coordinates[0],
                             coordinates[1]).setBackground(colors["blue"])

            elif type(itm) == PyQt5.QtWidgets.QLabel:
                itm.setText("Stability: {}".format(stability[idx]))

    #===============================================================================#
    def update_images(self, rows, columns, datas, stability):
        path_list = []
        for i in range(len(datas)):
            path = Converter.array_to_img(datas[i])
            path_list.append(path)

        i = 0
        idx_gen = (i for i in range(len(datas)))

        for itm in self.model.gridLayoutWidget.children():

            i += 1

            if i % 2 == 0 and type(itm) == PyQt5.QtWidgets.QLabel:
                idx = next(idx_gen)
                itm.setPixmap(
                    QtGui.QPixmap(getcwd() + "/" + path_list[idx]).scaled(100,
                                                                          120))
                itm.setGeometry(10, 10, 200, 240)

            if i % 2 != 0 and type(itm) == PyQt5.QtWidgets.QLabel:
                itm.setText("Stability: {}".format(stability[idx]))
