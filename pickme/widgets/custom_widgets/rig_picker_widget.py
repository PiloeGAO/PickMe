"""
    :package:   PickMe
    :file:      rig_picker_widget.py
    :brief:     Main picker widget.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import os
import json
from functools import partial

from PySide2 import QtWidgets, QtGui, QtCore

from pickme.core.path import ROOT_DIR

class RigPickerWidget(QtWidgets.QGraphicsScene):
    def __init__(self, x, y, w, h, parent=None):
        super(RigPickerWidget, self).__init__(x, y, w, h, parent)
        self._manager = None
        self._rig = None
        self._current_picker_group = None

        self._current_clicked_pos = QtCore.QPointF(0, 0)

        self._menu = QtWidgets.QMenu("Options")
        self._edit_menu = QtWidgets.QMenu("Edit")
        self._menu.addMenu(self._edit_menu)
        self._groups_menu = QtWidgets.QMenu("Groups")
        self._menu.addMenu(self._groups_menu)
        self._menu.addSeparator()
        self._menu.addAction("Add Button", self.create_button)

    @property
    def manager(self):
        return self._manager

    @manager.setter
    def manager(self, manager):
        self._manager = manager
        self._rig = manager.rig
    
    def mousePressEvent(self, event):
        """Implement Middle Click and Right Click.

        Args:
            event (QEvent): Event.
        """
        if event.type() == QtCore.QEvent.GraphicsSceneMousePress:
            self._current_clicked_pos = event.scenePos()
            
            selected_element = self.items(event.scenePos())[0]

            if event.button() == QtCore.Qt.RightButton:
                if(self._rig != None):
                    # Edit current picker element.
                    self._edit_menu.clear()
                    self._edit_menu.addAction(
                        "Rename",
                        partial(
                            self.rename_picker_button,
                            selected_element
                        )
                    )

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
                            partial(
                                self.change_picker_button_color,
                                selected_element,
                                color_data["color"])
                        )

                    self._edit_menu.addMenu(color_menu)

                    self._edit_menu.addSeparator()

                    self._edit_menu.addAction(
                        "Delete",
                        partial(
                            self.delete_picker_button,
                            selected_element
                        )
                    )
                    
                    # Picker Group Selector
                    self._groups_menu.clear()
                    for picker_groups in self._rig.picker_groups:
                        self._groups_menu.addAction(
                            picker_groups.name.replace("_", " "),
                            partial(
                                self._rig.set_current_picker_group,
                                picker_groups
                            )
                        )
                
                self._menu.exec_(QtGui.QCursor.pos())
        
        super(RigPickerWidget, self).mousePressEvent(event)

    def load_layer(self):
        """Load the current group in the view.
        """
        self._rig = self._manager.rig

        self.clear()
        if(self._rig == None):
            return
        
        # Setup view.
        self._current_picker_group = self._rig.current_picker_group
        width = self._rig.current_picker_group.width
        height = self._rig.current_picker_group.height
        self.setSceneRect(0, 0, width, height)

        for elem in self._rig.current_picker_group.interactive_elements:
            self.addItem(
                RigPickerButton(
                    picker_element=elem
                )
            )
    
    # Create Picker Button.
    def create_button(self):
        """Add a button from viewport selection.
        """
        selection = self._manager.integration.get_selection()

        if(len(selection) == 0):
            print("Please select an object.")
            return
        elif(len(selection) > 1):
            print("Only the first selected object will have a button.")
        
        selected_object_name = selection[0]

        nice_name, status = QtWidgets.QInputDialog().getText(self._manager.ui,
                                    "Set name",
                                    "Name:", QtWidgets.QLineEdit.Normal,
                                    selected_object_name)

        if(not nice_name or not status):
            print("No name entered.")
            return

        button_size = [16, 16]

        points = [
            [self._current_clicked_pos.x() - button_size[0], self._current_clicked_pos.y() - button_size[1]],
            [self._current_clicked_pos.x() - button_size[0], self._current_clicked_pos.y() + button_size[1]],
            [self._current_clicked_pos.x() + button_size[0], self._current_clicked_pos.y() + button_size[1]],
            [self._current_clicked_pos.x() + button_size[0], self._current_clicked_pos.y() - button_size[1]]
        ]

        self._rig.current_picker_group.add_interactive_element(
            name=selected_object_name,
            nice_name=nice_name,
            color="#636e72",
            points=points
        )

        self.load_layer()

    # Edit Picker Button.
    def rename_picker_button(self, element):
        """Rename the selected element.

        Args:
            element (class: RigPickerButton): Selected element
        """
        nice_name, status = QtWidgets.QInputDialog().getText(self._manager.ui,
                                    "Set name",
                                    "New name:", QtWidgets.QLineEdit.Normal,
                                    element.picker_element.nice_name)

        if(not nice_name or not status):
            print("No name entered.")
            return
        
        element.picker_element.nice_name = str(nice_name)
        element.update()

        self._current_picker_group.save()
    
    def change_picker_button_color(self, element, new_color):
        """Update the color of the button.

        Args:
            new_color (str): Hex Color.
        """
        element.picker_element.color = new_color
        element.update()

        self._current_picker_group.save()
    
    def delete_picker_button(self, element):
        """Remove the selected element.

        Args:
            element (class: RigPickerButton): Selected element
        """
        self._current_picker_group.remove_interactive_element(element.picker_element)

        self.removeItem(element)
        self.update()

class RigPickerButton(QtWidgets.QGraphicsItem):
    Type = QtWidgets.QGraphicsItem.UserType + 1
    
    def __init__(self, picker_element=None, *args, **kwargs):
        super(RigPickerButton, self).__init__(*args, **kwargs)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, False)

        self._picker_element = picker_element

        points = []
        for point in self._picker_element.points:
            points.append(
                QtCore.QPointF(
                    float(point.x),
                    float(point.y)
                )
            )
        
        self.polygon = QtGui.QPolygonF(
            points
        )
    
    @property
    def picker_element(self):
        return self._picker_element
    
    def type(self):
       """ Enable the use of qgraphicsitem_cast with this item.
       """
       return self.Type

    def paint(self, painter, option, widget=None):
        painter.setPen(
            QtGui.QPen(
                self._picker_element.color
            )
        )
        painter.setBrush(
            QtGui.QBrush(
                self._picker_element.color,
                QtCore.Qt.SolidPattern
            )
        )

        painter.drawPolygon(self.polygon)

        painter.setPen(
            QtGui.QPen(
                QtCore.Qt.white
            )
        )

        painter.drawText(
            self.polygon.boundingRect().center(),
            self._picker_element.nice_name
        )
    
    def shape(self):
        """Define the shape of the Item, usefull for defining custom bounding boxes.

        Returns:
            class: QtGui.QPainterPath: Path of the shape
        """
        path = QtGui.QPainterPath()
        path.addPolygon(self.polygon)
        return path
    
    def boundingRect(self):
        return self.polygon.boundingRect()

    def mousePressEvent(self, event):
        self._picker_element.on_click()

        super(RigPickerButton, self).mousePressEvent(event)