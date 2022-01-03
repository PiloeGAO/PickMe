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
        self.mainLayout = QHBoxLayout(HorizontalButtonBarWidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonArrayWidget = QScrollArea(HorizontalButtonBarWidget)
        self.buttonArrayWidget.setObjectName(u"buttonArrayWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonArrayWidget.sizePolicy().hasHeightForWidth())
        self.buttonArrayWidget.setSizePolicy(sizePolicy)
        self.buttonArrayWidget.setFrameShape(QFrame.NoFrame)
        self.buttonArrayWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.buttonArrayWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.buttonArrayWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.buttonArrayWidget.setWidgetResizable(True)
        self.buttonArrayWidgetContents = QWidget()
        self.buttonArrayWidgetContents.setObjectName(u"buttonArrayWidgetContents")
        self.buttonArrayWidgetContents.setGeometry(QRect(0, 0, 518, 116))
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.buttonArrayWidgetContents.sizePolicy().hasHeightForWidth())
        self.buttonArrayWidgetContents.setSizePolicy(sizePolicy1)
        self.buttonArrayWidgetContentsLayout = QHBoxLayout(self.buttonArrayWidgetContents)
        self.buttonArrayWidgetContentsLayout.setObjectName(u"buttonArrayWidgetContentsLayout")
        self.buttonArrayWidgetSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.buttonArrayWidgetContentsLayout.addItem(self.buttonArrayWidgetSpacer)

        self.buttonArrayWidget.setWidget(self.buttonArrayWidgetContents)

        self.mainLayout.addWidget(self.buttonArrayWidget)

        self.actionButton = QPushButton(HorizontalButtonBarWidget)
        self.actionButton.setObjectName(u"actionButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.actionButton.sizePolicy().hasHeightForWidth())
        self.actionButton.setSizePolicy(sizePolicy2)
        self.actionButton.setMinimumSize(QSize(16, 16))

        self.mainLayout.addWidget(self.actionButton)


        self.retranslateUi(HorizontalButtonBarWidget)

        QMetaObject.connectSlotsByName(HorizontalButtonBarWidget)
    # setupUi

    def retranslateUi(self, HorizontalButtonBarWidget):
        HorizontalButtonBarWidget.setWindowTitle(QCoreApplication.translate("HorizontalButtonBarWidget", u"Form", None))
        self.actionButton.setText(QCoreApplication.translate("HorizontalButtonBarWidget", u"Action", None))
    # retranslateUi

