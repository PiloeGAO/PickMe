"""
    :package:   PickMe
    :file:      selection_set_button.py
    :brief:     Custom button with all actions related to selection sets.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import os
import json
from functools import partial

from PySide2 import QtWidgets, QtGui, QtCore

from pickme.core.path import ROOT_DIR, ICONS_DIR

class SelectionSetButton(QtWidgets.QPushButton):
    def __init__(self, selection_set, parent=None) -> None:
        super(SelectionSetButton, self).__init__(selection_set.name, parent=parent)
        self._set = selection_set

        # Set Button Display.
        self.setFixedSize(64, 64)

        # Set Menu.
        self._menu = QtWidgets.QMenu()

        color_menu_icon = QtGui.QIcon(os.path.join(ICONS_DIR, "toolFill.png"))
        color_menu = QtWidgets.QMenu("Colors")

        color_config_file = open(os.path.join(ROOT_DIR, "ui", "selection_sets_colors.json"), "r")
        colors_data = json.load(color_config_file)
        color_config_file.close()

        for color_data in colors_data:
            pixmap = QtGui.QPixmap(16, 16)
            pixmap.fill(QtGui.QColor(color_data["color"]))
            icon = QtGui.QIcon(pixmap)

            color_menu.addAction(
                icon,
                color_data["name"],
                partial(self.change_color, color_data["color"])
            )

        self._menu.addMenu(color_menu)
        self._menu.addSeparator()

        delete_icon = QtGui.QIcon(os.path.join(ICONS_DIR, "trashcanOpen.png"))
        self._menu.addAction(delete_icon, "Delete", self.delete)

        # Set Connections
        self.clicked.connect(self._set.select_objects)

        # Initialize Display
        self.setupUI()
    
    def setupUI(self):
        """ Setup the displqy of the button (visual only).
        """
        if(self._set.color != ""):
            self.setStyleSheet("""
                background-color: {color};
                color: #FFFFFF;
                border:  none;
            """.format(
                color = self._set.color
            ))
        
    def mousePressEvent(self, event):
        """Implement Middle Click and Right Click.

        Args:
            event (QEvent): Event.
        """
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.MiddleButton:
                print("Toto")
            elif event.button() == QtCore.Qt.RightButton:
                self._menu.exec_(QtGui.QCursor.pos())
            else:
                super(SelectionSetButton, self).mousePressEvent(event)

    def change_color(self, new_color):
        """Update the color of the button.

        Args:
            new_color (str): Hex Color.
        """
        self._set.color = new_color
        self._set.rig.save_selection_sets()
        self.setupUI()
    
    def delete(self):
        """Delete the button and remove the selection set from the rig.
        """
        self._set.rig.delete_selection_set(self._set.id)
        self.deleteLater()