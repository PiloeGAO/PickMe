# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from pickme.widgets.horizontal_button_bar_widget import Ui_HorizontalButtonBarWidget


class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        if not MainWidget.objectName():
            MainWidget.setObjectName(u"MainWidget")
        MainWidget.resize(720, 500)
        self.verticalLayout = QVBoxLayout(MainWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.headerWidget = Ui_HorizontalButtonBarWidget(MainWidget)
        self.headerWidget.setObjectName(u"headerWidget")

        self.verticalLayout.addWidget(self.headerWidget)

        self.rigsWidget = QTabWidget(MainWidget)
        self.rigsWidget.setObjectName(u"rigsWidget")
        self.rigTab = QWidget()
        self.rigTab.setObjectName(u"rigTab")
        self.rigsWidget.addTab(self.rigTab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.rigsWidget.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.rigsWidget)


        self.retranslateUi(MainWidget)

        QMetaObject.connectSlotsByName(MainWidget)
    # setupUi

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(QCoreApplication.translate("MainWidget", u"Form", None))
        self.rigsWidget.setTabText(self.rigsWidget.indexOf(self.rigTab), QCoreApplication.translate("MainWidget", u"Tab 1", None))
        self.rigsWidget.setTabText(self.rigsWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWidget", u"Tab 2", None))
    # retranslateUi

