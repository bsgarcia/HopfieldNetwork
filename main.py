##########
# main.py #
##########
import sys
from PyQt5 import QtGui, QtWidgets
from Model.model import Model
from Ctrls.controller import MainController
from View.UI import Ui_MainView
from View.view import MainView


class App(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = Model()
        self.main_ctrl = MainController(self.model)
        self.main_view = MainView(self.model, self.main_ctrl, Ui_MainView)
        self.main_view.show()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
