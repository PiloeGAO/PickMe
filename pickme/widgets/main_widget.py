"""
    :package:   PickMe
    :file:      main_widget.py
    :brief:     Maion widget for PickMe.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import os

from PySide2 import QtWidgets, QtGui

from pickme.core.manager import Manager
from pickme.core.rig import Rig
from pickme.core.path import ROOT_DIR, ICONS_DIR

from pickme.widgets.auto_generated.main_widget import Ui_MainWidget
from pickme.widgets.custom_widgets.rig_button import RigButton

class MainWidget(QtWidgets.QWidget, Ui_MainWidget):
    def __init__(self, integration="standalone", parent=None):
        super(MainWidget, self).__init__()

        self._manager = Manager(self, integration=integration)

        with open(os.path.join(ROOT_DIR, "ui", "pickme_theme.qss"),"r") as qss:
            self.setStyleSheet(qss.read())

        self.setupUi(self)

        self.pickerWidget.manager = self._manager

        self.setup_interactions()
    
    def setup_interactions(self):
        """Setup all interactions for the main widget.
        """
        self.mainLayout.setMargin(0)

        # Setup a menubar for the mainwidget
        self.menubar = QtWidgets.QMenuBar(self)
        edit_menu = self.menubar.addMenu('Edit')

        create_rig_button = QtWidgets.QAction(QtGui.QIcon(os.path.join(ICONS_DIR, "plus.png")), "Create Rig", self)
        create_rig_button.triggered.connect(self.menu_create_rig)
        edit_menu.addAction(create_rig_button)

        create_picker_button = QtWidgets.QAction("Create Picker Layer", self)
        create_picker_button.triggered.connect(self.menu_create_picker_layer)
        edit_menu.addAction(create_picker_button)

        self.mainLayout.insertWidget(0, self.menubar)

        # Set header functions.
        reload_icon = os.path.join(ICONS_DIR, "return.png")
        
        self.headerWidget.set_action_button(
            display_name=False,
            icon=reload_icon,
            clicked_func=self.reload_configurations
        )

        self.load_rigs()
    
    # Menu Bar Functions
    def menu_create_rig(self):
        new_rig_name = self._manager.integration.get_rig_selected()

        if(new_rig_name == ""):
            error_dialog = QtWidgets.QMessageBox.critical(
                self, "Rig creation failed",
                "No valid rig selected", QtWidgets.QMessageBox.Ok
            )
            return
        
        new_rig = Rig.create(self._manager, new_rig_name)
        if(new_rig == None):
            error_dialog = QtWidgets.QMessageBox.critical(
                self, "Rig creation failed",
                "Something wrong happened. \nDid te same rig already created?", QtWidgets.QMessageBox.Ok
            )
            return

        self._manager.add_rig(new_rig)
        self.reload_configurations()
    
    def menu_create_picker_layer(self):
        if(self._manager.current_rig == None):
            print("Please load a rig.")
            return
        
        name, ok = QtWidgets.QInputDialog().getText(self, "Picer Layer Name",
            "Name:", QtWidgets.QLineEdit.Normal,
            "Picker Layer"
        )

        if(not ok and name == ""):
            return
        
        print(name)

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
            self.headerWidget.add_item_to_bar(
                RigButton(rig)
            )
        
        if(len(self._manager.rigs) > 0):
            self.pickerWidget.stackedWidget.setCurrentIndex(1)
            self.move_to_rig(0)

            [rig_button for rig_button in self.headerWidget.widgets if rig_button.rig.id == 0][0].set_active()

    def refresh_rig_buttons(self, active_button):
        """Refresh the header widgets and set buttons inactive except for the clicked one.

        Args:
            active_button (class: RigButton): Active button
        """
        for button in self.headerWidget.widgets:
            if(button == active_button):
                continue

            button.set_inactive()
    
    def create_attributes(self):
        self.pickerWidget.create_attributes()

    def refresh_attributes(self):
        self.pickerWidget.refresh_attributes()

    def move_to_rig(self, id):
        """Update the current rig in the Manager.

        Args:
            id (int): Index of the new selected rig
        """
        self._manager.current_rig = id
        self.pickerWidget.setup_interactions()