"""
    :package:   PickMe
    :file:      rig_display_widget.py
    :brief:     Main picker widget.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import os
from functools import partial

from PySide2 import QtWidgets

from pickme.core.path import ICONS_DIR
from pickme.widgets.auto_generated.rig_display_widget import Ui_RigDisplayWidget
from pickme.widgets.selection_set_button import SelectionSetButton

class RigDisplayWidget(QtWidgets.QWidget, Ui_RigDisplayWidget):
    def __init__(self, parent=None):
        super(RigDisplayWidget, self).__init__()

        self._manager = None

        self.setupUi(self)
    
    @property
    def manager(self):
        return self._manager

    @manager.setter
    def manager(self, manager):
        self._manager = manager
        self.setup_interactions()

    def setup_interactions(self):
        """Setup all interactions for the main widget.
        """
        # Set header functions.
        plus_icon = os.path.join(ICONS_DIR, "plus.png")
        
        self.selectionGroup.set_action_button(
            display_name=False,
            icon=plus_icon,
            clicked_func=self.add_selection_set
        )

        if(self._manager.rig != None):
            self.load_selection_sets()
    
    def load_selection_sets(self):
        """Load selections sets for current rig.
        """
        self.selectionGroup.clear_bar()

        for set in self._manager.rig.selection_sets:
            selection_set_button = SelectionSetButton(set, self._manager.integration)
            self.selectionGroup.add_item_to_bar(selection_set_button)

    def add_selection_set(self):
        """Add a selection group to the UI.
        """
        name, status = QtWidgets.QInputDialog().getText(self,
                                    "QInputDialog().getText()",
                                    "Name:", QtWidgets.QLineEdit.Normal,
                                    "Selection")
        
        selection = self._manager.integration.get_selection()

        if((not name and not status) or selection == []):
            print("No name entered or nothing selected.")
            return
        
        self._manager.rig.create_selection_set(name=name, objects=selection)

        self.load_selection_sets()