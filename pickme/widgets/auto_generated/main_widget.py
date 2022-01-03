# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from pickme.widgets.horizontal_button_bar_widget import HorizontalButtonBarWidget
from pickme.widgets.rig_display_widget import RigDisplayWidget


class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        if not MainWidget.objectName():
            MainWidget.setObjectName(u"MainWidget")
        MainWidget.resize(720, 500)
        self.mainLayout = QVBoxLayout(MainWidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(3, 3, 3, 3)
        self.headerWidget = HorizontalButtonBarWidget(MainWidget)
        self.headerWidget.setObjectName(u"headerWidget")

        self.mainLayout.addWidget(self.headerWidget)

        self.pickerWidget = RigDisplayWidget(MainWidget)
        self.pickerWidget.setObjectName(u"pickerWidget")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pickerWidget.sizePolicy().hasHeightForWidth())
        self.pickerWidget.setSizePolicy(sizePolicy)

        self.mainLayout.addWidget(self.pickerWidget)


        self.retranslateUi(MainWidget)

        QMetaObject.connectSlotsByName(MainWidget)
    # setupUi

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(QCoreApplication.translate("MainWidget", u"Form", None))
    # retranslateUi

