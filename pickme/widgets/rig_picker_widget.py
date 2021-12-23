"""
    :package:   PickMe
    :file:      rig_picker_widget.py
    :brief:     Main picker widget.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
from PySide2 import QtWidgets

class RigPickerWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(RigPickerWidget, self).__init__()