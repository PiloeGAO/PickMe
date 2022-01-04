# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rig_display_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from pickme.widgets.custom_widgets.horizontal_button_bar_widget import HorizontalButtonBarWidget
from pickme.widgets.custom_widgets.rig_picker_widget import RigPickerWidget


class Ui_RigDisplayWidget(object):
    def setupUi(self, RigDisplayWidget):
        if not RigDisplayWidget.objectName():
            RigDisplayWidget.setObjectName(u"RigDisplayWidget")
        RigDisplayWidget.resize(306, 250)
        self.mainLayout = QVBoxLayout(RigDisplayWidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(RigDisplayWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.no_rig_page = QWidget()
        self.no_rig_page.setObjectName(u"no_rig_page")
        self.verticalLayout_2 = QVBoxLayout(self.no_rig_page)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.no_rig_label = QLabel(self.no_rig_page)
        self.no_rig_label.setObjectName(u"no_rig_label")
        font = QFont()
        font.setFamily(u"Calibri")
        font.setPointSize(20)
        self.no_rig_label.setFont(font)
        self.no_rig_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.no_rig_label)

        self.stackedWidget.addWidget(self.no_rig_page)
        self.rig_display_page = QWidget()
        self.rig_display_page.setObjectName(u"rig_display_page")
        self.verticalLayout = QVBoxLayout(self.rig_display_page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSplitter = QSplitter(self.rig_display_page)
        self.horizontalSplitter.setObjectName(u"horizontalSplitter")
        self.horizontalSplitter.setEnabled(True)
        self.horizontalSplitter.setOrientation(Qt.Horizontal)
        self.horizontalSplitter.setHandleWidth(5)
        self.rigDisplay = RigPickerWidget(self.horizontalSplitter)
        self.rigDisplay.setObjectName(u"rigDisplay")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rigDisplay.sizePolicy().hasHeightForWidth())
        self.rigDisplay.setSizePolicy(sizePolicy)
        self.horizontalSplitter.addWidget(self.rigDisplay)
        self.scrollAttributesEditor = QScrollArea(self.horizontalSplitter)
        self.scrollAttributesEditor.setObjectName(u"scrollAttributesEditor")
        sizePolicy.setHeightForWidth(self.scrollAttributesEditor.sizePolicy().hasHeightForWidth())
        self.scrollAttributesEditor.setSizePolicy(sizePolicy)
        self.scrollAttributesEditor.setFrameShape(QFrame.NoFrame)
        self.scrollAttributesEditor.setWidgetResizable(True)
        self.attributesEditorObject = QWidget()
        self.attributesEditorObject.setObjectName(u"attributesEditorObject")
        self.attributesEditorObject.setGeometry(QRect(0, 0, 86, 194))
        self.attributesEditorLayout = QVBoxLayout(self.attributesEditorObject)
        self.attributesEditorLayout.setObjectName(u"attributesEditorLayout")
        self.attributesEditorLayout.setContentsMargins(0, 0, 0, 0)
        self.attributesSpacer = QSpacerItem(20, 189, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.attributesEditorLayout.addItem(self.attributesSpacer)

        self.scrollAttributesEditor.setWidget(self.attributesEditorObject)
        self.horizontalSplitter.addWidget(self.scrollAttributesEditor)

        self.verticalLayout.addWidget(self.horizontalSplitter)

        self.selectionGroup = HorizontalButtonBarWidget(self.rig_display_page)
        self.selectionGroup.setObjectName(u"selectionGroup")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.selectionGroup.sizePolicy().hasHeightForWidth())
        self.selectionGroup.setSizePolicy(sizePolicy1)
        self.selectionGroup.setMinimumSize(QSize(50, 50))

        self.verticalLayout.addWidget(self.selectionGroup)

        self.stackedWidget.addWidget(self.rig_display_page)

        self.mainLayout.addWidget(self.stackedWidget)


        self.retranslateUi(RigDisplayWidget)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(RigDisplayWidget)
    # setupUi

    def retranslateUi(self, RigDisplayWidget):
        RigDisplayWidget.setWindowTitle(QCoreApplication.translate("RigDisplayWidget", u"Form", None))
        self.no_rig_label.setText(QCoreApplication.translate("RigDisplayWidget", u"No rig loaded in the scene.", None))
    # retranslateUi

