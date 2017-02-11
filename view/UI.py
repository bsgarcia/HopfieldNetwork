# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainView(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(945, 690)
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(565, 30, 131, 20))
        self.checkBox.setObjectName("checkBox")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(800, 20, 101, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(690, 20, 101, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.epochs = QtWidgets.QSpinBox(Form)
        self.epochs.setGeometry(QtCore.QRect(490, 20, 61, 31))
        self.epochs.setObjectName("epochs")
        self.epochs.setMaximum(10000)
        self.epochs.setValue(1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(435, 30, 61, 20))
        self.label.setObjectName("label")
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(19, 79, 500, 300))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(90, 20, 90, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(Form)
        self.comboBox_2.setGeometry(QtCore.QRect(329, 20, 90, 31))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 30, 51, 16))
        self.label_2.setObjectName("label_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(200, 20, 91, 31))
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.checkBox.setText(_translate("Form", "Force stability"))
        self.pushButton.setText(_translate("Form", "Asynchronous"))
        self.pushButton_2.setText(_translate("Form", "Synchronous"))
        self.label.setText(_translate("Form", "epochs:"))
        self.comboBox.setItemText(0, _translate("Form", "Images"))
        self.comboBox.setItemText(1, _translate("Form", "Numbers"))
        self.comboBox_2.setItemText(0, _translate("Form", "f1"))
        self.comboBox_2.setItemText(1, _translate("Form", "f2"))
        self.comboBox_2.setItemText(2, _translate("Form", "f3"))
        self.label_2.setText(_translate("Form", "mode:"))
        self.pushButton_3.setText(_translate("Form", "Load "))

