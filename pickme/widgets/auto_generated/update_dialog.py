# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'update_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_UpdateDialog(object):
    def setupUi(self, UpdateDialog):
        if not UpdateDialog.objectName():
            UpdateDialog.setObjectName(u"UpdateDialog")
        UpdateDialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(UpdateDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.title_layout_previous_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.title_layout_previous_spacer)

        self.update_icon = QPushButton(UpdateDialog)
        self.update_icon.setObjectName(u"update_icon")
        self.update_icon.setFlat(True)

        self.horizontalLayout.addWidget(self.update_icon)

        self.title_label = QLabel(UpdateDialog)
        self.title_label.setObjectName(u"title_label")

        self.horizontalLayout.addWidget(self.title_label)

        self.title_layout_next_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.title_layout_next_spacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.description_widget = QTextEdit(UpdateDialog)
        self.description_widget.setObjectName(u"description_widget")
        self.description_widget.setFrameShape(QFrame.NoFrame)
        self.description_widget.setLineWidth(0)
        self.description_widget.setReadOnly(True)

        self.verticalLayout.addWidget(self.description_widget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.download_layout_next_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.download_layout_next_spacer)

        self.download_button = QPushButton(UpdateDialog)
        self.download_button.setObjectName(u"download_button")

        self.horizontalLayout_2.addWidget(self.download_button)

        self.download_layout_previous_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.download_layout_previous_spacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(UpdateDialog)

        self.download_button.setDefault(True)


        QMetaObject.connectSlotsByName(UpdateDialog)
    # setupUi

    def retranslateUi(self, UpdateDialog):
        UpdateDialog.setWindowTitle(QCoreApplication.translate("UpdateDialog", u"Dialog", None))
        self.update_icon.setText(QCoreApplication.translate("UpdateDialog", u"ICON", None))
        self.title_label.setText(QCoreApplication.translate("UpdateDialog", u"<h1>New update available. </h1>", None))
        self.download_button.setText(QCoreApplication.translate("UpdateDialog", u"Download Now", None))
    # retranslateUi

