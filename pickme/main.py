"""
    :package:   PickMe
    :file:      __init__.py
    :brief:     File that open the UI in standalone mode.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""

from os import sys, path

from PySide2 import QtWidgets

if __name__ == "__main__":
    if __package__ is None:
        print("Not executed in package.")
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    from pickme.widgets.main_window import MainWindow

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_()) 