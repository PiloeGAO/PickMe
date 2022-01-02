"""
    :package:   PickMe
    :file:      horizontal_button_bar_widget.py
    :brief:     Horizontal customizable bar with buttons.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
from PySide2 import QtWidgets, QtGui, QtCore

from pickme.widgets.auto_generated.horizontal_button_bar_widget import Ui_HorizontalButtonBarWidget

class HorizontalButtonBarWidget(QtWidgets.QWidget, Ui_HorizontalButtonBarWidget):
    def __init__(self, parent=None):
        super(HorizontalButtonBarWidget, self).__init__()

        self.setupUi(self)

        self.buttonArrayWidgetContentsLayout.setSpacing(0)
        self.buttonArrayWidgetContentsLayout.setMargin(0)

        self.buttonArrayWidget.setFrameStyle(QtWidgets.QFrame.NoFrame)

        self.setStyleSheet(
        """
        QPushButton {
            border-radius: 3px;
            border-style: solid;
            border-width: 2px;
            border-color: grey;
        }
        QScrollArea {
            border-radius: 3px;
            border-style: solid;
            border-width: 2px;
            border-color: grey;
        }
        """
        )
    
    @property
    def widgets(self):
        """Return all widgets in the bar.

        Returns:
            list: List of widgets
        """
        widgets = []

        for i in reversed(range(self.buttonArrayWidgetContentsLayout.count()-1)): 
            widgets.append(self.buttonArrayWidgetContentsLayout.itemAt(i).widget())
        
        return widgets

    def set_action_button(self, name="Action", display_name=True, icon=None, icon_size=(64, 64), flat=False, clicked_func=None, pressed_func=None, released_func=None, menu=None):
        """Set the action button datas.

        Args:
            name (str, optional): Text displayed on the button. Defaults to "Action".
            icon (QIcon, optional): Icon to display instead of the text. Defaults to None.
            icon_size (tuple, optional): Icon Size in pixel. Defaults to (64, 64).
            flat (bool, optional): Set button to flat display. Defaults to False.
            clicked_func (function, optional): Function to execute on clicked. Defaults to None.
            pressed_func (function, optional): Function to execute on press. Defaults to None.
            released_func (function, optional): Function to execute on release. Defaults to None.
            menu (QMenu, optional): Set the menu of the button. Defaults to None.
        """
        self.actionButton.setText(name)

        if(icon != None):
            icon_size = QtCore.QSize(icon_size[0], icon_size[1])

            if(not display_name): self.actionButton.setText("")

            # Convert string to QIcon.
            if(type(icon) == str):
                icon_pixmap = QtGui.QPixmap(icon)
                tmp_icon = QtGui.QIcon(icon_pixmap)
                icon = tmp_icon
            
            # Reset the icon to correct scale.
            if(icon_pixmap.width() < icon_size.width() or icon_pixmap.height() < icon_size.height()):
                icon_size = icon_pixmap.size()

            self.actionButton.setIcon(icon)
            self.actionButton.setIconSize(icon_size)
        
        self.actionButton.setFlat(flat)

        if(clicked_func != None):
            self.actionButton.clicked.connect(clicked_func)
        if(pressed_func != None):
            self.actionButton.pressed.connect(pressed_func)
        if(released_func != None):
            self.actionButton.released.connect(released_func)
        
        if(menu != None):
            self.actionButton.setMenu(menu)
    
    def add_button(self, name="Button", display_name=True, icon=None, flat=False, clicked_func=None, pressed_func=None, released_func=None, menu=None):
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
            if(not display_name): button.setText("")
            # Convert string to QIcon.
            if(type(icon) == str):
                tmp_icon = QtGui.QIcon()
                tmp_icon.addFile(icon)
                icon = tmp_icon

            button.setIcon(icon)

        if(clicked_func != None):
            button.clicked.connect(clicked_func)
        if(pressed_func != None):
            button.pressed.connect(pressed_func)
        if(released_func != None):
            button.released.connect(released_func)
        
        if(menu != None):
            button.setMenu(menu)
        
        self.buttonArrayWidgetContentsLayout.insertWidget(self.buttonArrayWidgetContentsLayout.count()-1, button)

    def add_item_to_bar(self, item):
        """Add a widget to the bar.

        Args:
            item (QWidget): Widget to add
        """
        self.buttonArrayWidgetContentsLayout.insertWidget(self.buttonArrayWidgetContentsLayout.count()-1, item)
    
    def remove_item(self, i):
        """Remove a specific element from the bar.

        Args:
            i (int): Index of the element
        """
        if(i < self.buttonArrayWidgetContentsLayout.count()-1 and i >= 0):
            self.buttonArrayWidgetContentsLayout.itemAt(i).widget().setParent(None)

    def clear_bar(self):
        """Clear the bar.

        source: https://gist.github.com/JokerMartini/7fe4f204b6a7912be3ac
        """
        for i in reversed(range(self.buttonArrayWidgetContentsLayout.count()-1)): 
            self.buttonArrayWidgetContentsLayout.itemAt(i).widget().setParent(None)