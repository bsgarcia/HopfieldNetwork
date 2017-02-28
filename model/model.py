##################
# models\model.py #
##################
from PyQt5 import QtCore


class Model():

    #### properties for value of Qt model contents ####
    @property
    def comboBox_items(self):
        return self.comboBox_model.stringList()
    @comboBox_items.setter
    def comboBox_items(self, value):
        self.comboBox_model.setStringList(value)
    @property
    def comboBox_2_items(self):
        return self.comboBox_2_model.stringList()
    @comboBox_items.setter
    def comboBox_2_items(self, value):
        self.comboBox_2_model.setStringList(value)

    def __init__(self):
        super(Model, self).__init__()
        self._update_funcs = []
        self.config_section = 'settings'
        self.config_options = (
            ('pushButton', 'getboolean'),
            ('pushButton_2', 'getboolean'),
            ('pushButton_3', 'getboolean'),
            ('pushButton_4', 'getboolean'),
            ('checkBox', 'getboolean'),
            ('label', 'get'),
            ('label_2', 'get'),
            ('epochs', 'getint'),
            ('comboBox', 'getint'),
            ('comboBox_2', 'getint'),
            ('comboBox_3', 'getint'),
        )

        #### create Qt models for compatible widget types ####
        self.comboBox_model = QtCore.QStringListModel()
        self.comboBox_2_model = QtCore.QStringListModel()
        self.comboBox_3_model = QtCore.QStringListModel()

        #### model variables ####
        self.pushButton = None
        self.pushButton_2 = None
        self.pushButton_3 = None
        self.pushButton_4 = None
        self.checkBox = False
        self.label = None
        self.label_2 = None
        self.epochs = 1 
        self.comboBox = None
        self.comboBox_2 = 0 
        self.comboBox_3 = None
        self.gridLayout = None
        self.gridLayoutWidget = None
        self.gridLayout_2 = None
        self.gridLayoutWidget_2 = None

    def subscribe_update_func(self, func):
        if func not in self._update_funcs:
            self._update_funcs.append(func)

    def unsubscribe_update_func(self, func):
        if func in self._update_funcs:
            self._update_funcs.remove(func)

    def announce_update(self):
        for func in self._update_funcs:
            func()

