# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'buttonEditor.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QSpacerItem, QSpinBox, QWidget)

class Ui_ButtonEditor(object):
    def setupUi(self, ButtonEditor):
        if not ButtonEditor.objectName():
            ButtonEditor.setObjectName(u"ButtonEditor")
        ButtonEditor.resize(400, 300)
        font = QFont()
        font.setPointSize(12)
        ButtonEditor.setFont(font)
        self.gridLayout = QGridLayout(ButtonEditor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lblInactiv = QLabel(ButtonEditor)
        self.lblInactiv.setObjectName(u"lblInactiv")

        self.gridLayout.addWidget(self.lblInactiv, 1, 0, 1, 1)

        self.spInactiveTime = QSpinBox(ButtonEditor)
        self.spInactiveTime.setObjectName(u"spInactiveTime")
        self.spInactiveTime.setMinimum(1000)
        self.spInactiveTime.setMaximum(600000)

        self.gridLayout.addWidget(self.spInactiveTime, 1, 1, 1, 1)

        self.lblLongPress = QLabel(ButtonEditor)
        self.lblLongPress.setObjectName(u"lblLongPress")
        self.lblLongPress.setFont(font)

        self.gridLayout.addWidget(self.lblLongPress, 0, 0, 1, 1)

        self.spLongPressTime = QSpinBox(ButtonEditor)
        self.spLongPressTime.setObjectName(u"spLongPressTime")
        self.spLongPressTime.setMinimum(1000)
        self.spLongPressTime.setMaximum(600000)

        self.gridLayout.addWidget(self.spLongPressTime, 0, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 0, 1, 1)


        self.retranslateUi(ButtonEditor)

        QMetaObject.connectSlotsByName(ButtonEditor)
    # setupUi

    def retranslateUi(self, ButtonEditor):
        ButtonEditor.setWindowTitle(QCoreApplication.translate("ButtonEditor", u"Form", None))
        self.lblInactiv.setText(QCoreApplication.translate("ButtonEditor", u"Inactive Time [ms]:", None))
        self.lblLongPress.setText(QCoreApplication.translate("ButtonEditor", u"Long Press Time [ms]:", None))
    # retranslateUi

