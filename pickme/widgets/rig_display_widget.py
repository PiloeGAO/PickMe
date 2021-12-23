"""
    :package:   PickMe
    :file:      rig_display_widget.py
    :brief:     Main picker widget.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import os

from PySide2 import QtWidgets, QtGui

from pickme.widgets.auto_generated.rig_display_widget import Ui_RigDisplayWidget

from pickme.core.path import ICONS_DIR

class RigDisplayWidget(QtWidgets.QWidget, Ui_RigDisplayWidget):
    def __init__(self, parent=None):
        super(RigDisplayWidget, self).__init__()

        self.setupUi(self)
        self.setup_interactions()
    
    def setup_interactions(self):
        """Setup all interactions for the main widget.
        """
        # Set header functions.
        plus_icon = QtGui.QIcon()
        plus_icon.addFile(os.path.join(ICONS_DIR, "plus.png"))
        
        self.selectionGroup.set_action_button(
            icon=plus_icon,
            clicked_func=self.add_selection_group
        )
    
    def add_selection_group(self):
        """Add a selection group to the UI.
        """
        self.selectionGroup.add_button("Toto")