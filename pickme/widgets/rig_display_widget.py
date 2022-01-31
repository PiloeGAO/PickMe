"""
    :package:   PickMe
    :file:      rig_display_widget.py
    :brief:     Main picker widget.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import os

from PySide2 import QtWidgets, QtCore
from pickme.core.attribute import AttributeTypes

from pickme.core.path import ICONS_DIR

from pickme.widgets.auto_generated.rig_display_widget import Ui_RigDisplayWidget
from pickme.widgets.custom_widgets.attribute_widget import AttributeWidget
from pickme.widgets.custom_widgets.collapsable_layout_widget import CollapsableLayoutWidget
from pickme.widgets.custom_widgets.rig_picker_widget import RigPickerWidget
from pickme.widgets.custom_widgets.selection_set_button import SelectionSetButton

from pickme.core.logger import get_logger
logger = get_logger()

class RigDisplayWidget(QtWidgets.QWidget, Ui_RigDisplayWidget):
    def __init__(self, parent=None):
        super(RigDisplayWidget, self).__init__()

        self._manager = None
        self._rig = None

        self.attributes_widgets = []

        self.setupUi(self)

        self._rig_picker_scene = RigPickerWidget(0, 0, 0, 0)
        self.picker_graphics_view.setScene(self._rig_picker_scene)

    @property
    def manager(self):
        return self._manager

    @manager.setter
    def manager(self, manager):
        self._manager = manager

        self._rig_picker_scene.manager = manager

        self.setup_interactions()

    def resizeEvent(self, event):
        """Resize the sub-widgets.

        Args:
            event (:obj:`PySide2.QtGui.QResizeEvent`): Event
        """
        super(RigDisplayWidget, self).resizeEvent(event)

        self.update_picker_graphics_view_size()

    def setup_interactions(self):
        """Setup all interactions for the main widget.
        """
        # Set Attributes functions.
        self.create_attributes()

        # Set selection sets functions.
        plus_icon = os.path.join(ICONS_DIR, "plus.png")
        
        self.selectionGroup.set_action_button(
            name="Selection Sets",
            display_name=False,
            icon=plus_icon,
            clicked_func=self.add_selection_set
        )

        self.refresh_widget_content()
    
    def refresh_widget_content(self):
        """Refresh the content of the widget.
        """
        if(self._manager.rig == None):
            return

        if(self._rig == None and self._manager.rig != None):
            self._rig = self._manager.rig
        
        # Reset the splitter
        if(len(self._rig._picker_groups) > 0):
            widget_size = (self.size().width(), self.size().height())
            self.horizontalSplitter.setSizes([widget_size[0]/2, widget_size[1]])

            self.load_picker()
        else:
            self.horizontalSplitter.setSizes([0, self.size().width()])
        
        logger.info(f"Loading \"{self._rig.name}\"")
        self.load_selection_sets()

    # Picker Area
    def load_picker(self):
        """Load a new picker in the picker area.
        """
        self._rig_picker_scene.load_group()

        self.update_picker_graphics_view_size()

    def update_picker_graphics_view_size(self, size=()):
        """Update the size of the element inside of the QGraphicsView.
        """
        if(size == ()):
            width = self.picker_graphics_view.width()
            height = self.picker_graphics_view.height()
        else:
            width = size[0]
            height = size[1]
        
        self.picker_graphics_view.fitInView(0, 0, width, height,aspectRatioMode=QtCore.Qt.KeepAspectRatio)

    # Attributes Editor    
    def create_attributes(self):
        """Create attributes.
        """
        if(self._rig == None):
            return
        
        self.clear_attributes_editor()
        self.attributes_widgets = []

        # Set Attributes functions.
        for attr in self._rig.attributes:
            if(attr.attribute_type == AttributeTypes.group):
                if(len(attr.childs) == 0): continue

                childs_attributes_widgets = [AttributeWidget(attribute=child_attr) for child_attr in attr.childs]
                self.attributes_widgets.extend(childs_attributes_widgets)
                collapsable_layout_widget = CollapsableLayoutWidget(
                    attr.nice_name,
                    items = childs_attributes_widgets
                )

                self.add_item_to_attributes_editor(collapsable_layout_widget)

            else:
                attribute_widget = AttributeWidget(attribute=attr)
                self.attributes_widgets.append(attribute_widget)
                self.add_item_to_attributes_editor(attribute_widget)

    def refresh_attributes(self):
        """Update attributes values.
        """
        for attr_widget in self.attributes_widgets:
            attr_widget.refresh_widget()

    def add_item_to_attributes_editor(self, item):
        """Add a widget to the bar.

        Args:
            item (:obj:`PySide2.QtWidgets.QWidget`): Widget to add
        """
        self.attributesEditorLayout.insertWidget(self.attributesEditorLayout.count()-1, item)
    
    def remove_item_from_attributes_editor(self, i):
        """Remove a specific element from the bar.

        Args:
            i (int): Index of the element
        """
        if(i < self.attributesEditorLayout.count()-1 and i >= 0):
            self.attributesEditorLayout.itemAt(i).widget().setParent(None)

    def clear_attributes_editor(self):
        """Clear the bar.

        source: https://gist.github.com/JokerMartini/7fe4f204b6a7912be3ac
        """
        for i in reversed(range(self.attributesEditorLayout.count()-1)): 
            self.attributesEditorLayout.itemAt(i).widget().setParent(None)

    # Selection Sets.
    def load_selection_sets(self):
        """Load selections sets for current rig.
        """
        self.selectionGroup.clear_bar()

        for set in self._rig.selection_sets:
            selection_set_button = SelectionSetButton(set, self)
            self.selectionGroup.add_item_to_bar(selection_set_button)

    def add_selection_set(self):
        """Add a selection group to the UI.
        """
        if(self._rig == None):
            return
        
        name, status = QtWidgets.QInputDialog().getText(self,
                                    "Set Name",
                                    "Name:", QtWidgets.QLineEdit.Normal,
                                    "Selection")

        if(not name or not status):
            logger.error("No name entered.")
            return
        
        selection = self._manager.integration.get_selection()
        if(len(selection) == 0):
            logger.error("Nothing selected ! ")
            return

        rig_path = self._rig.path
        icon_name = ""
        
        if(os.path.isfile(os.path.join(rig_path, "icons", name))):
            icon_name = name
            name = os.path.splitext(name)[:-1][0]

        self._rig.create_selection_set(name=name, objects=selection, icon=icon_name)

        self.load_selection_sets()