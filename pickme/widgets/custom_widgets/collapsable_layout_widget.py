"""
    :package:   PickMe
    :file:      collapsable_layout_widget.py
    :brief:     Collapsable layout widget.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
from PySide2 import QtWidgets, QtGui, QtCore

class CollapsableLayoutWidget(QtWidgets.QWidget):
    def __init__(self, title, items=[]):
        super(CollapsableLayoutWidget, self).__init__(parent=None)

        self._title = title
        self._open_status = True
        self._items = items

        self.setupUi()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        pen = QtGui.QPen()
        pen.setWidth(1)
        pen.setColor("#555555")
        painter.setPen(pen)

        rect = QtCore.QRect(0, 0, painter.device().width()-1, painter.device().height()-1)
        painter.drawRoundedRect(rect, 5, 5)

    def setupUi(self):
        """Function to setup the widget's elements.
        """
        widget_layout = QtWidgets.QVBoxLayout()
        # widget_layout.setMargin(2)

        # Header
        header_layout = QtWidgets.QHBoxLayout()
        widget_layout.addLayout(header_layout)

        open_button = OpenButton(func=self.update_display)
        header_layout.addWidget(open_button)

        title_widget = QtWidgets.QLabel(f"<h3>{self._title}</h3>")
        header_layout.addWidget(title_widget)

        # Elements
        self.elements_widget = QtWidgets.QWidget()
        elements_layout = QtWidgets.QVBoxLayout()
        self.elements_widget.setLayout(elements_layout)

        for item in self._items:
            elements_layout.addWidget(item)
        
        self.elements_widget.setVisible(self._open_status)
        widget_layout.addWidget(self.elements_widget)

        self.setLayout(widget_layout)
    
    def update_display(self):
        """Update the display of the widget.
        """
        self._open_status = not self._open_status
        self.elements_widget.setVisible(self._open_status)

        self.update()

class OpenButton(QtWidgets.QWidget):
    """Custom open button.
    Source: https://www.pythonguis.com/tutorials/creating-your-own-custom-widgets/
    """
    def __init__(self, func=None):
        super(OpenButton, self).__init__(parent=None)

        self._func = func
        self._status = True

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed
        )

    def mousePressEvent(self, event):
        """Implement Mouse Clicks.

        Args:
            event (QEvent): Event.
        """
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                self._func()
                self._status = not self._status
                self.update()
            else:
                super(OpenButton, self).mousePressEvent(event)

    def sizeHint(self):
        return QtCore.QSize(12,12)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        
        pen = QtGui.QPen()
        pen.setWidth(2)
        pen.setColor("#555555")
        painter.setPen(pen)

        if(self._status):
            painter.drawLine(0, 0, painter.device().width()/2, painter.device().height()-1)
            painter.drawLine(painter.device().width()/2, painter.device().height()-1, painter.device().width(), 0)
        else:
            painter.drawLine(0, 0, painter.device().width(), (painter.device().height()-1)/2)
            painter.drawLine(painter.device().width(), (painter.device().height()-1)/2, 0, painter.device().height())
