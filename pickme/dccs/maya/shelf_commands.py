'''
    :package:   PickMe
    :file:      shelf_commands.py
    :author:    ldepoix
    :version:   0.0.2
    :brief:     Commands to execute from the shelf.
'''
import webbrowser

from pickme.widgets.main_widget import MainWidget
from pickme.dccs.maya.maya_widgets import DockableWidgetUIScript

def open_ui():
    """Open the interface of PickMe.
    """
    pickme_main_widget = MainWidget(integration="maya")
    DockableWidgetUIScript(window_name="PickMe", widget=pickme_main_widget, restore=False)

def open_doc():
    """Open the project documentation on the web browser.
    """
    webbrowser.open_new_tab("https://github.com/PiloeGAO/PickMe/")