"""
    :package:   PickMe
    :file:      float_slider_widget.py
    :brief:     Float slider widget.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
from PySide2 import QtWidgets, QtCore

class FloatSliderWidget(QtWidgets.QWidget):
    def __init__(self, default_value, min_value=0, max_value=1, func=None):
        super(FloatSliderWidget, self).__init__(parent=None)

        self._factor = 100

        self._value = default_value * self._factor
        self._min = min_value * self._factor
        self._max = max_value * self._factor

        self._update_function = func

        self.setupUi()
    
    @property
    def value(self):
        return self._value / self._factor
    
    @value.setter
    def value(self, value):
        self._value = value * self._factor
        self.slider.setValue(self._value)

        if(self.value < self.min):
            self.min = self.value
        
        if(self.value > self.max):
            self.max = self.value

    @property
    def min(self):
        return self._min / self._factor
    
    @min.setter
    def min(self, min):
        self._min = min * self._factor

    @property
    def max(self):
        return self._max / self._factor

    @max.setter
    def max(self, max):
        self._max = max * self._factor

    def setupUi(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setMargin(0)

        self.min_value_widget = QtWidgets.QLabel(str(self.min))
        layout.addWidget(self.min_value_widget)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.setToolTip(str(self.value))

        self.slider.setMinimum(self._min)
        self.slider.setMaximum(self._max)
        self.slider.setValue(self._value)

        self.slider.sliderReleased.connect(
            self.update_value
        )

        layout.addWidget(self.slider)
        
        self.max_value_widget = QtWidgets.QLabel(str(self.max))
        layout.addWidget(self.max_value_widget)

        self.setLayout(layout)
    
    def update_value(self):
        self._value = self.slider.value()
        self.slider.setToolTip(str(self.value))
        
        self._update_function(self.value) 
