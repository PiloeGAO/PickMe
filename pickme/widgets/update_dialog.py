"""
    :package:   PickMe
    :file:      update_dialog.py
    :brief:     Update dialog.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import os
import webbrowser

from PySide2 import QtWidgets, QtGui

from pickme.core.path import ICONS_DIR, LOCAL_CONFIG_DIR

from pickme.widgets.auto_generated.update_dialog import Ui_UpdateDialog

class UpdateDialog(QtWidgets.QDialog, Ui_UpdateDialog):
    def __init__(self, new_version, parent=None):
        super(UpdateDialog, self).__init__(parent)

        self._version = new_version

        self.setupUi(self)

        self.setup_interactions()
    
    def setup_interactions(self):
        """Setup all interactions for the main widget.
        """
        # Display update informations in the UI.
        self.update_icon.setText("")
        self.update_icon.setIcon(
            QtGui.QIcon(
                os.path.join(ICONS_DIR, "download.png")
            )
        )

        self.title_label.setText(f"<h1>Version \"{self._version.name}\" is out !</h1>")

        self.description_widget.setText(
            self._version.description
        )

        # Link buttons.
        self.download_button.clicked.connect(self.open_download_page)
    
    def open_download_page(self):
        """Open the download page.
        """
        webbrowser.open_new_tab(self._version.url)
        self.close()