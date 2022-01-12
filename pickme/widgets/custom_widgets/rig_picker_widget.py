"""
    :package:   PickMe
    :file:      rig_picker_widget.py
    :brief:     Main picker widget.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
from PySide2 import QtWidgets, QtGui, QtCore

class RigPickerWidget(QtWidgets.QGraphicsScene):
    def __init__(self, x, y, w, h, layer=None, parent=None):
        super(RigPickerWidget, self).__init__(x, y, w, h, parent)

    def load_layer(self, layer, width=100, height=100):
        self.setSceneRect(0, 0, width, height)
        self.clear()

        for elem in layer.interactive_elements:
            self.addItem(
                RigPickerButton(
                    picker_element=elem
                )
            )

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