"""
    :package:   PickMe
    :file:      error_dialog.py
    :brief:     Error dialog.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import os
import traceback
import webbrowser

from PySide2 import QtWidgets, QtGui

from pickme.core.path import ICONS_DIR, LOCAL_CONFIG_DIR

from pickme.widgets.auto_generated.error_dialog import Ui_ErrorDialog

from pickme.core.logger import get_logger
logger = get_logger(debug=os.environ.get("PICKME_DEBUG", False))

class ErrorDialog(QtWidgets.QDialog, Ui_ErrorDialog):
    def __init__(self, type, value, traceback, parent=None):
        super(ErrorDialog, self).__init__(parent)

        self._error_type = type
        self._error_value = value
        self._error_traceback = traceback

        self.setupUi(self)

        self.setup_interactions()
    
    def setup_interactions(self):
        """Setup all interactions for the main widget.
        """
        # Display error in the UI.
        self.error_icon.setText("")
        self.error_icon.setIcon(
            QtGui.QIcon(
                os.path.join(ICONS_DIR, "warning.png")
            )
        )
        self.error_info_label.setText(f"<h2>{self._error_type.__name__}: {self._error_value}</h2>")
        self.traceback_details.setText(
            "".join(
                traceback.extract_tb(
                self._error_traceback
                ).format()
            )
        )

        # Link buttons.
        self.open_log_button.clicked.connect(self.open_log_file)
        self.report_button.clicked.connect(self.open_report_page)
        self.close_button.clicked.connect(self.close_pickme)
    
    def open_log_file(self):
        """Open the log file.
        """
        log_file_path = os.path.join(LOCAL_CONFIG_DIR, "logs.log")
        if(not os.path.isfile(log_file_path)):
            logger.warning("Log file not found.")
            return
        
        os.startfile(log_file_path)

    def open_report_page(self):
        """Open the report page in user's webbrowser.
        """
        base_url = "https://github.com/PiloeGAO/PickMe/issues/new"

        query = {
            "labels" : "crash report",
            "title" : f"PickMe Crash [{self._error_type.__name__}: {self._error_value}]",
            "body" : "Please add the log here with steps that produce the crash"
        }

        formatted_query = ""
        for key, item in query.items():
            formatted_query += f"{key}={item.replace(' ', '+')}&"
        formatted_query = formatted_query[:-1]
        
        webbrowser.open_new_tab(f"{base_url}?{formatted_query}")

    def close_pickme(self):
        """Close the dialog, and close PickMe due to the error.
        """
        self.close()
