"""
    :package:   PickMe
    :file:      selection_set_button.py
    :brief:     Custom button with all actions related to selection sets.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
# TODO: Move selection sets to a class instead of a dict.
from functools import partial

from PySide2 import QtWidgets

class SelectionSetButton(QtWidgets.QPushButton):
    def __init__(self, selection_set, parent=None) -> None:
        super(SelectionSetButton, self).__init__(selection_set.name, parent=parent)

        self.setFixedSize(64, 64)

        self._set = selection_set
        self.clicked.connect(self._set.select_objects)