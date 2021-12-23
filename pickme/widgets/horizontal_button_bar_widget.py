"""
    :package:   PickMe
    :file:      horizontal_button_bar_widget.py
    :brief:     Horizontal customizable bar with buttons.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
from PySide2 import QtWidgets
from pickme.widgets.auto_generated.horizontal_button_bar_widget import Ui_HorizontalButtonBarWidget
class HorizontalButtonBarWidget(QtWidgets.QWidget, Ui_HorizontalButtonBarWidget):
    def __init__(self, parent=None):
        super(HorizontalButtonBarWidget, self).__init__()

        self.setupUi(self)
    
    def set_action_button(self, name="Action", icon=None, flat=False, clicked_func=None, pressed_func=None, released_func=None, menu=None):
        """Set the action button datas.

        Args:
            name (str, optional): Text displayed on the button. Defaults to "Action".
            icon (QIcon, optional): Icon to display instead of the text. Defaults to None.
            flat (bool, optional): Set button to flat display. Defaults to False.
            clicked_func (function, optional): Function to execute on clicked. Defaults to None.
            pressed_func (function, optional): Function to execute on press. Defaults to None.
            released_func (function, optional): Function to execute on release. Defaults to None.
            menu (QMenu, optional): Set the menu of the button. Defaults to None.
        """
        if(icon != None):
            self.actionButton.setText("")
            self.actionButton.setIcon(icon)
        else:
            self.actionButton.setText(name)
        
        self.actionButton.setFlat(flat)
        self.actionButton.setFixedSize(64, 64)

        if(clicked_func != None):
            self.actionButton.clicked.connect(clicked_func)
        if(pressed_func != None):
            self.actionButton.pressed.connect(pressed_func)
        if(released_func != None):
            self.actionButton.released.connect(released_func)
        
        if(menu != None):
            self.actionButton.setMenu(menu)
    
    def add_button(self, name="Button", icon=None, flat=False, clicked_func=None, pressed_func=None, released_func=None, menu=None):
        """Add a button to bar.

        Args:
            name (str, optional): Text displayed on the button. Defaults to "Button".
            icon (QIcon, optional): Icon to display instead of the text. Defaults to None.
            flat (bool, optional): Set button to flat display. Defaults to False.
            clicked_func (function, optional): Function to execute on clicked. Defaults to None.
            pressed_func (function, optional): Function to execute on press. Defaults to None.
            released_func (function, optional): Function to execute on release. Defaults to None.
            menu (QMenu, optional): Set the menu of the button. Defaults to None.
        """
        button = QtWidgets.QPushButton(name)
        button.setFlat(flat)
        button.setFixedSize(64, 64)

        if(icon != None):
            button.setIcon(icon)

        if(clicked_func != None):
            button.clicked.connect(clicked_func)
        if(pressed_func != None):
            button.pressed.connect(pressed_func)
        if(released_func != None):
            button.released.connect(released_func)
        
        if(menu != None):
            button.setMenu(menu)
        
        self.buttonArrayWidgetContentsLayout.addWidget(button)

    def add_item_to_bar(self, item):
        """Add a widget to the bar.

        Args:
            item (QWidget): Widget to add
        """
        self.buttonArrayWidgetContentsLayout.addWidget(item)
    
    def remove_item(self, i):
        """Remove a specific element from the bar.

        Args:
            i (int): Index of the element
        """
        if(i < self.buttonArrayWidgetContentsLayout.count() and i >= 0):
            self.buttonArrayWidgetContentsLayout.itemAt(i).widget().setParent(None)

    def clear_bar(self):
        """Clear the bar.

        source: https://gist.github.com/JokerMartini/7fe4f204b6a7912be3ac
        """
        for i in reversed(range(self.buttonArrayWidgetContentsLayout.count())): 
            self.buttonArrayWidgetContentsLayout.itemAt(i).widget().setParent(None)