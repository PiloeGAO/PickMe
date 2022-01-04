"""
    :package:   PickMe
    :file:      attribute_widget.py
    :brief:     Attribute widget.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
from PySide2 import QtWidgets, QtCore

from pickme.core.attribute import AttributeTypes

from pickme.widgets.custom_widgets.float_slider_widget import FloatSliderWidget

class AttributeWidget(QtWidgets.QWidget):
    def __init__(self, attribute=None, update_function=None):
        super(AttributeWidget, self).__init__(parent=None)

        self._attribute = attribute

        self.setupUi()
    
    def mousePressEvent(self, event):
        """Implement Middle Click and Right Click.

        Args:
            event (QEvent): Event.
        """
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.MiddleButton:
                # Reset the value to default.
                self.update_value(self._attribute.default_value)
                self._attribute.edit_attribute(self._attribute.default_value)
            else:
                super(AttributeWidget, self).mousePressEvent(event)
    
    def setupUi(self):
        """Build the user interface.
        """

        layout = QtWidgets.QGridLayout()
        layout.setMargin(0)
        self.setLayout(layout)

        if(self._attribute == None):
            self.title = QtWidgets.QLabel("No attribute linked")

        self.title = QtWidgets.QLabel(self._attribute.nice_name)
        layout.addWidget(self.title, 0, 0)

        if(self._attribute.attribute_type == AttributeTypes.number):
            self.value_widget = FloatSliderWidget(
                self._attribute.value,
                self._attribute.min_value,
                self._attribute.max_value,
                func=self._attribute.edit_attribute
            )

        elif(self._attribute.attribute_type == AttributeTypes.boolean):
            self.value_widget = QtWidgets.QCheckBox("")
            self.value_widget.setChecked(self._attribute.value)
            self.value_widget.toggled.connect(
                self._attribute.edit_attribute
            )

        elif(self._attribute.attribute_type == AttributeTypes.string):
            self.value_widget = QtWidgets.QLineEdit()
            self.value_widget.setText(self._attribute.value)
            self.value_widget.textChanged.connect(
                self._attribute.edit_attribute
            )

        else:
            self.value_widget = QtWidgets.QLabel("Incorrect value type.")

        layout.addWidget(self.value_widget, 0, 1)
    
    def refresh_widget(self):
        """Refresh the widget.
        """
        self.update_value(self._attribute.value)
    
    def update_value(self, new_value):
        """Update the value of the widget.

        Args:
            new_value (int, float, bool, str): New value
        """
        if(self._attribute.attribute_type == AttributeTypes.number):
            self.value_widget.value = new_value

        elif(self._attribute.attribute_type == AttributeTypes.boolean):
            self.value_widget.setChecked(new_value)

        elif(self._attribute.attribute_type == AttributeTypes.string):
            self.value_widget.setText(new_value)

        else:
            print("Nothing to update.")