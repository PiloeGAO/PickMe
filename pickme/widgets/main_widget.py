"""
    :package:   PickMe
    :file:      main_widget.py
    :brief:     Maion widget for PickMe.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import os

from PySide2 import QtWidgets, QtGui

from pickme.widgets.auto_generated.main_widget import Ui_MainWidget

from pickme.core.path import ICONS_DIR

class MainWidget(QtWidgets.QWidget, Ui_MainWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__()

        self.setupUi(self)
        self.setup_interactions()
    
    def setup_interactions(self):
        """Setup all interactions for the main widget.
        """
        # Set header functions.
        reload_icon = QtGui.QIcon()
        reload_icon.addFile(os.path.join(ICONS_DIR, "return.png"))
        
        self.headerWidget.set_action_button(
            icon=reload_icon
        )

        for i in range(3):
            self.headerWidget.add_button(name=f"Rig {i}")