# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'picker_widget.ui'
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


class Ui_PickerWidget(object):
    def setupUi(self, PickerWidget):
        if not PickerWidget.objectName():
            PickerWidget.setObjectName(u"PickerWidget")
        PickerWidget.resize(636, 594)
        self.verticalLayout = QVBoxLayout(PickerWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.rigDisplay = RigDisplayWidget(PickerWidget)
        self.rigDisplay.setObjectName(u"rigDisplay")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rigDisplay.sizePolicy().hasHeightForWidth())
        self.rigDisplay.setSizePolicy(sizePolicy)
        self.rigDisplay.setMinimumSize(QSize(64, 64))

        self.verticalLayout.addWidget(self.rigDisplay)

        self.selectionGroup = HorizontalButtonBarWidget(PickerWidget)
        self.selectionGroup.setObjectName(u"selectionGroup")
        sizePolicy.setHeightForWidth(self.selectionGroup.sizePolicy().hasHeightForWidth())
        self.selectionGroup.setSizePolicy(sizePolicy)
        self.selectionGroup.setMinimumSize(QSize(32, 32))

        self.verticalLayout.addWidget(self.selectionGroup)


        self.retranslateUi(PickerWidget)

        QMetaObject.connectSlotsByName(PickerWidget)
    # setupUi

    def retranslateUi(self, PickerWidget):
        PickerWidget.setWindowTitle(QCoreApplication.translate("PickerWidget", u"Form", None))
    # retranslateUi

