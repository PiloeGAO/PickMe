"""
    :package:   PickMe
    :file:      horizontal_button_bar_widget.py
    :brief:     Horizontal customizable bar with buttons.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
from PySide2 import QtWidgets
from pickme.widgets.auto_generated.horizontal_button_bar_widget import Ui_HorizontalButtonBarWidget
class HorizontalButtonBarWidget(QtWidgets.QWidget, Ui_HorizontalButtonBarWidget):
    def __init__(self, parent=None):
        super(HorizontalButtonBarWidget, self).__init__()

        self.setupUi(self)