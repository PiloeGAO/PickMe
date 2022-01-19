# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'error_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ErrorDialog(object):
    def setupUi(self, ErrorDialog):
        if not ErrorDialog.objectName():
            ErrorDialog.setObjectName(u"ErrorDialog")
        ErrorDialog.resize(400, 321)
        self.main_layout = QVBoxLayout(ErrorDialog)
        self.main_layout.setObjectName(u"main_layout")
        self.title_layout = QHBoxLayout()
        self.title_layout.setObjectName(u"title_layout")
        self.title_layout_prev_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.title_layout.addItem(self.title_layout_prev_spacer)

        self.error_icon = QPushButton(ErrorDialog)
        self.error_icon.setObjectName(u"error_icon")
        self.error_icon.setIconSize(QSize(32, 32))
        self.error_icon.setAutoDefault(False)
        self.error_icon.setFlat(True)

        self.title_layout.addWidget(self.error_icon)

        self.title_label = QLabel(ErrorDialog)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setMargin(10)

        self.title_layout.addWidget(self.title_label)

        self.title_layout_next_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.title_layout.addItem(self.title_layout_next_spacer)


        self.main_layout.addLayout(self.title_layout)

        self.error_info_label = QLabel(ErrorDialog)
        self.error_info_label.setObjectName(u"error_info_label")

        self.main_layout.addWidget(self.error_info_label)

        self.traceback_details = QTextEdit(ErrorDialog)
        self.traceback_details.setObjectName(u"traceback_details")
        self.traceback_details.setReadOnly(True)

        self.main_layout.addWidget(self.traceback_details)

        self.log_layout = QHBoxLayout()
        self.log_layout.setObjectName(u"log_layout")
        self.log_text_label = QLabel(ErrorDialog)
        self.log_text_label.setObjectName(u"log_text_label")

        self.log_layout.addWidget(self.log_text_label)

        self.open_log_button = QPushButton(ErrorDialog)
        self.open_log_button.setObjectName(u"open_log_button")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_log_button.sizePolicy().hasHeightForWidth())
        self.open_log_button.setSizePolicy(sizePolicy)
        self.open_log_button.setFlat(False)

        self.log_layout.addWidget(self.open_log_button)


        self.main_layout.addLayout(self.log_layout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.main_layout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttons_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.buttons_spacer)

        self.report_button = QPushButton(ErrorDialog)
        self.report_button.setObjectName(u"report_button")

        self.horizontalLayout.addWidget(self.report_button)

        self.close_button = QPushButton(ErrorDialog)
        self.close_button.setObjectName(u"close_button")

        self.horizontalLayout.addWidget(self.close_button)


        self.main_layout.addLayout(self.horizontalLayout)


        self.retranslateUi(ErrorDialog)

        self.open_log_button.setDefault(False)
        self.report_button.setDefault(True)


        QMetaObject.connectSlotsByName(ErrorDialog)
    # setupUi

    def retranslateUi(self, ErrorDialog):
        ErrorDialog.setWindowTitle(QCoreApplication.translate("ErrorDialog", u"PickMe Error Reporter", None))
        self.error_icon.setText(QCoreApplication.translate("ErrorDialog", u"ICON", None))
        self.title_label.setText(QCoreApplication.translate("ErrorDialog", u"<h1>Oups: PickeMe crashed!</h1>", None))
        self.error_info_label.setText(QCoreApplication.translate("ErrorDialog", u"Error: message", None))
        self.log_text_label.setText(QCoreApplication.translate("ErrorDialog", u"<i>Please send your log with the report</i>", None))
        self.open_log_button.setText(QCoreApplication.translate("ErrorDialog", u"Open Log File", None))
        self.report_button.setText(QCoreApplication.translate("ErrorDialog", u"Send report", None))
        self.close_button.setText(QCoreApplication.translate("ErrorDialog", u"Quit PickeMe", None))
    # retranslateUi

