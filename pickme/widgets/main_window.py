"""
    :package:   PickMe
    :file:      main_window.py
    :brief:     Main window.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
from PySide2  import QtWidgets

class MainWindow(QtWidgets.QWidget):
    """Main Window class.

    Args:
        parent (class: "QtWidgets", optional): PyQt parent. Defaults to None.
    """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)

        # Initialize UI.
        self.initUI()
    
    def initUI(self):
        """Generate the window.
        """
        # Set the window title.
        self.setWindowTitle("PickMe")
        
        # Set the window size.
        self.setGeometry(0, 0, 640, 480)

        # Set the window style.
        self.setStyle(QtWidgets.QStyleFactory.create("Fusion"))