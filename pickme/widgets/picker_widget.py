"""
    :package:   PickMe
    :file:      picker_widget.py
    :brief:     Main picker widget.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
from PySide2 import QtWidgets
from pickme.widgets.auto_generated.picker_widget import Ui_PickerWidget

class PickerWidget(QtWidgets.QWidget, Ui_PickerWidget):
    def __init__(self, parent=None):
        super(PickerWidget, self).__init__()

        self.setupUi(self)