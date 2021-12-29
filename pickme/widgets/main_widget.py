"""
    :package:   PickMe
    :file:      main_widget.py
    :brief:     Maion widget for PickMe.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import os
from functools import partial

from PySide2 import QtWidgets

from pickme.core.manager import Manager
from pickme.core.path import ICONS_DIR

from pickme.widgets.auto_generated.main_widget import Ui_MainWidget

class MainWidget(QtWidgets.QWidget, Ui_MainWidget):
    def __init__(self, integration="standalone", parent=None):
        super(MainWidget, self).__init__()

        self._manager = Manager(self, integration=integration)

        self.setupUi(self)

        self.pickerWidget.manager = self._manager

        self.setup_interactions()
    
    def setup_interactions(self):
        """Setup all interactions for the main widget.
        """
        # Set header functions.
        reload_icon = os.path.join(ICONS_DIR, "return.png")
        
        self.headerWidget.set_action_button(
            display_name=False,
            icon=reload_icon,
            clicked_func=self.reload_configurations
        )

        self.load_rigs()
    
    def reload_configurations(self, *args, **kwargs):
        """Reload rigs from disk.
        """
        print("Reload rigs.")
        self.pickerWidget.stackedWidget.setCurrentIndex(0)
        self.headerWidget.clear_bar()

        self._manager.reload_configurations()
        self.load_rigs()
    
    def load_rigs(self):
        """Load rigs from the Manager and add them to the UI.
        """
        for rig in self._manager.rigs:
            icon_path = rig.icon
            rig_icon = None

            if(icon_path != None):
                if(os.path.isfile(icon_path)):
                    rig_icon = icon_path

            self.headerWidget.add_button(
                name=rig.name,
                icon=rig_icon,
                clicked_func=partial(self.move_to_rig, rig.id)
            )
        
        if(len(self._manager.rigs) > 0):
            self.pickerWidget.stackedWidget.setCurrentIndex(1)
            self.move_to_rig(0)

    def move_to_rig(self, id):
        """Update the current rig in the Manager.

        Args:
            id (int): Index of the new selected rig
        """
        self._manager.current_rig = id
        self.pickerWidget.setup_interactions()