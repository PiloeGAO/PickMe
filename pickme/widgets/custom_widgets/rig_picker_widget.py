"""
    :package:   PickMe
    :file:      rig_picker_widget.py
    :brief:     Main picker widget.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
from functools import partial

from PySide2 import QtWidgets, QtGui, QtCore

class RigPickerWidget(QtWidgets.QGraphicsScene):
    def __init__(self, x, y, w, h, parent=None):
        super(RigPickerWidget, self).__init__(x, y, w, h, parent)
        self._manager = None
        self._rig = None

        self._menu = QtWidgets.QMenu("Options")
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
            if event.button() == QtCore.Qt.RightButton:
                if(self._rig != None):
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
        width = self._rig.current_picker_group.width
        height = self._rig.current_picker_group.height
        self.setSceneRect(0, 0, width, height)

        for elem in self._rig.current_picker_group.interactive_elements:
            self.addItem(
                RigPickerButton(
                    picker_element=elem
                )
            )
    
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

        print(QtGui.QCursor.pos(), selected_object_name)

class RigPickerButton(QtWidgets.QGraphicsItem):
    Type = QtWidgets.QGraphicsItem.UserType + 1
    
    def __init__(self, picker_element=None, *args, **kwargs):
        super(RigPickerButton, self).__init__(*args, **kwargs)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
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
    
    def type(self):
       # Enable the use of qgraphicsitem_cast with this item.
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
    
    def boundingRect(self):
        return self.polygon.boundingRect()

    def mousePressEvent(self, event):
        tmp_polygon = QtGui.QPolygonF(
            [
                QtCore.QPointF(event.pos()),
                QtCore.QPointF(
                    event.pos().x() - 1,
                    event.pos().y()
                ),
                QtCore.QPointF(
                    event.pos().x(),
                    event.pos().y() + 1
                ),
            ]
        )

        if(self.polygon.intersects(tmp_polygon)):
            self._picker_element.on_click()

        super(RigPickerButton, self).mousePressEvent(event)