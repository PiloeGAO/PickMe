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
from pickme.core.selection_set import SelectionSet

class SelectionSetButton(QtWidgets.QToolButton):
    def __init__(self, selection_set, parent_widget, parent=None) -> None:
        super(SelectionSetButton, self).__init__(parent=parent)
        self._set = selection_set
        self._parent = parent_widget

        # Set Button Display.
        self.setFixedSize(64, 64)
        self.setText(self._set.name)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        # Set Menu.
        self._menu = QtWidgets.QMenu()

        self._menu.addAction("Show/Hide Selection Set", self.show_hide_selection_set)
        self._menu.addSeparator()

        if(self._set.selection_set_manager.is_editable):
            self._menu.addAction("Rename", self.rename)
            self._menu.addAction("Change Icon", self.change_icon)
            self._menu.addSeparator()

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
            QToolButton {
                background-color: %s;
                color: #FFFFFF;
                margin: 2px;
                border-radius: 3px;
                border-style: %s;
                border-width: 2px;
                border-color: %s;
            }

            QToolButton:hover {
                border-color: grey;
            }

            QToolButton:pressed {
                border-color: white;
            }
            """ % (self._set.color, "solid" if self._set.selection_set_manager.is_editable else "dashed", self._set.color)
            )
        
        if(os.path.isfile(self._set.icon)):
            icon_size = self.size()

            icon_pixmap = QtGui.QPixmap(self._set.icon)
            icon = QtGui.QIcon(icon_pixmap)
            
            # Reset the icon to correct scale.
            if(icon_pixmap.width() < icon_size.width() or icon_pixmap.height() < icon_size.height()):
                icon_size = icon_pixmap.size()

            self.setIcon(icon)
            self.setIconSize(icon_size/2)
        
    def mousePressEvent(self, event):
        """Implement Middle Click and Right Click.

        Args:
            event (QEvent): Event.
        """
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.MiddleButton:
                self._set.reset_moves()
            elif event.button() == QtCore.Qt.RightButton:
                self._menu.exec_(QtGui.QCursor.pos())
            else:
                super(SelectionSetButton, self).mousePressEvent(event)

    def show_hide_selection_set(self):
        """Show/Hide selection set.
        """
        self._set.rig.show_hide_selection_set(self._set)

    def rename(self):
        """Rename the current button.
        """
        new_name, ok = QtWidgets.QInputDialog().getText(self, "Rename set",
                                     "Name:", QtWidgets.QLineEdit.Normal,
                                     self._set.name)
        if(not ok or new_name == ""):
            return

        self._set.name = new_name

        self._set.selection_set_manager.save_sets()

        self._parent.load_selection_sets()

    def change_icon(self):
        """Chaneg the icon of the current button.
        """
        rig_path = self._set.rig.path
        new_icon, ok = QtWidgets.QInputDialog().getText(self, "Update icon",
                                     "Icon name:", QtWidgets.QLineEdit.Normal,
                                     self._set.icon_name)

        if(not ok):
            return
        
        if(not os.path.isfile(os.path.join(rig_path, "icons", new_icon))):
            new_icon = ""

        self._set.icon = new_icon

        self._set.selection_set_manager.save_sets()

        self._parent.load_selection_sets()

    def change_color(self, new_color):
        """Update the color of the button.

        Args:
            new_color (str): Hex Color.
        """
        self._set.color = new_color
        self._set.selection_set_manager.save_sets()
        self.setupUI()
    
    def delete(self):
        """Delete the button and remove the selection set from the rig.
        """
        self._set.rig.delete_selection_set(self._set.selection_set_manager, self._set.id)
        self.deleteLater()