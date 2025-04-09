# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'multiStateEditor.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTableView, QWidget)

class Ui_MultiStateEditor(object):
    def setupUi(self, MultiStateEditor):
        if not MultiStateEditor.objectName():
            MultiStateEditor.setObjectName(u"MultiStateEditor")
        MultiStateEditor.resize(400, 300)
        font = QFont()
        font.setPointSize(12)
        MultiStateEditor.setFont(font)
        self.gridLayout = QGridLayout(MultiStateEditor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tvStateList = QTableView(MultiStateEditor)
        self.tvStateList.setObjectName(u"tvStateList")

        self.gridLayout.addWidget(self.tvStateList, 2, 0, 1, 3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 1, 1, 1)

        self.pbAddState = QPushButton(MultiStateEditor)
        self.pbAddState.setObjectName(u"pbAddState")
        self.pbAddState.setEnabled(True)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.pbAddState.setIcon(icon)

        self.gridLayout.addWidget(self.pbAddState, 3, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 2, 1, 1)

        self.lblStateList = QLabel(MultiStateEditor)
        self.lblStateList.setObjectName(u"lblStateList")

        self.gridLayout.addWidget(self.lblStateList, 1, 0, 1, 2)

        self.pbDeleteState = QPushButton(MultiStateEditor)
        self.pbDeleteState.setObjectName(u"pbDeleteState")
        self.pbDeleteState.setEnabled(False)
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.pbDeleteState.setIcon(icon1)

        self.gridLayout.addWidget(self.pbDeleteState, 3, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 3, 2, 1, 1)

        self.cbDefaultState = QComboBox(MultiStateEditor)
        self.cbDefaultState.setObjectName(u"cbDefaultState")

        self.gridLayout.addWidget(self.cbDefaultState, 0, 2, 1, 1)

        self.lblDefaultState = QLabel(MultiStateEditor)
        self.lblDefaultState.setObjectName(u"lblDefaultState")

        self.gridLayout.addWidget(self.lblDefaultState, 0, 0, 1, 2)


        self.retranslateUi(MultiStateEditor)

        QMetaObject.connectSlotsByName(MultiStateEditor)
    # setupUi

    def retranslateUi(self, MultiStateEditor):
        MultiStateEditor.setWindowTitle(QCoreApplication.translate("MultiStateEditor", u"Form", None))
        self.pbAddState.setText("")
        self.lblStateList.setText(QCoreApplication.translate("MultiStateEditor", u"State List:", None))
        self.pbDeleteState.setText("")
        self.lblDefaultState.setText(QCoreApplication.translate("MultiStateEditor", u"Default State:", None))
    # retranslateUi

