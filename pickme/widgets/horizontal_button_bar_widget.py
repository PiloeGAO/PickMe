# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'horizontal_button_bar_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_HorizontalButtonBarWidget(object):
    def setupUi(self, HorizontalButtonBarWidget):
        if not HorizontalButtonBarWidget.objectName():
            HorizontalButtonBarWidget.setObjectName(u"HorizontalButtonBarWidget")
        HorizontalButtonBarWidget.resize(599, 116)
        self.horizontalLayout = QHBoxLayout(HorizontalButtonBarWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttonArrayWidget = QScrollArea(HorizontalButtonBarWidget)
        self.buttonArrayWidget.setObjectName(u"buttonArrayWidget")
        self.buttonArrayWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.buttonArrayWidget.setWidgetResizable(True)
        self.buttonArrayWidgetContents = QWidget()
        self.buttonArrayWidgetContents.setObjectName(u"buttonArrayWidgetContents")
        self.buttonArrayWidgetContents.setGeometry(QRect(0, 0, 490, 90))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonArrayWidgetContents.sizePolicy().hasHeightForWidth())
        self.buttonArrayWidgetContents.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.buttonArrayWidgetContents)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.buttonArrayWidget.setWidget(self.buttonArrayWidgetContents)

        self.horizontalLayout.addWidget(self.buttonArrayWidget)

        self.actionButton = QPushButton(HorizontalButtonBarWidget)
        self.actionButton.setObjectName(u"actionButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.actionButton.sizePolicy().hasHeightForWidth())
        self.actionButton.setSizePolicy(sizePolicy1)
        self.actionButton.setMinimumSize(QSize(16, 16))

        self.horizontalLayout.addWidget(self.actionButton)


        self.retranslateUi(HorizontalButtonBarWidget)

        QMetaObject.connectSlotsByName(HorizontalButtonBarWidget)
    # setupUi

    def retranslateUi(self, HorizontalButtonBarWidget):
        HorizontalButtonBarWidget.setWindowTitle(QCoreApplication.translate("HorizontalButtonBarWidget", u"Form", None))
        self.actionButton.setText(QCoreApplication.translate("HorizontalButtonBarWidget", u"Action", None))
    # retranslateUi

