"""
    :package:   PickMe
    :file:      main_widget.py
    :brief:     Maion widget for PickMe.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
from PySide2 import QtWidgets
from pickme.widgets.auto_generated.main_widget import Ui_MainWidget
class MainWidget(QtWidgets.QWidget, Ui_MainWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__()

        self.setupUi(self)