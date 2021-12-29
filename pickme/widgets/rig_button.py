"""
    :package:   PickMe
    :file:      rig_button.py
    :brief:     Custom button with all actions related to a rig.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import os

from PySide2 import QtWidgets, QtGui, QtCore

class RigButton(QtWidgets.QToolButton):
    def __init__(self, rig, parent=None) -> None:
        super(RigButton, self).__init__(parent=parent)
        self._rig = rig
        self._is_current = False
        
        # Set Button Display.
        self.setFixedSize(64, 64)
        self.setText(self._rig.name)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setAutoRaise(True)
        self.set_inactive()

        if(os.path.isfile(self._rig.icon)):
            icon_size = self.size()

            icon_pixmap = QtGui.QPixmap(self._rig.icon)
            icon = QtGui.QIcon(icon_pixmap)
            
            # Reset the icon to correct scale.
            if(icon_pixmap.width() < icon_size.width() or icon_pixmap.height() < icon_size.height()):
                icon_size = icon_pixmap.size()

            self.setIcon(icon)
            self.setIconSize(icon_size/2)
        
        # Set Connections
        self.clicked.connect(self.set_current_rig)
    
    @property
    def rig(self):
        return self._rig
    
    def set_active(self):
        """Set the button down.
        """
        self.setDown(True)

        self.setStyleSheet(
        """
        border-radius: 3px;
        border-style: solid;
        border-width: 2px;
        border-color: white;
        """
        )

        self._is_current = True
    
    def set_inactive(self):
        """Set the button up.
        """
        self.setDown(False)
        
        self.setStyleSheet(
        """
        border-radius: 0px;
        border-style: none;
        border-width: 0px;
        border-color: white;
        """
        )

        self._is_current = False

    def set_current_rig(self):
        """Set the current rig.
        """
        if(self._is_current): return

        self._rig.manager.ui.move_to_rig(self._rig.id)
        self._rig.manager.ui.refresh_rig_buttons(self)
        self.set_active()