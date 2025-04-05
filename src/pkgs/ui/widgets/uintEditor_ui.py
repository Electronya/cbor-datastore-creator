# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'uintEditor.ui'
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

class Ui_UintEditor(object):
    def setupUi(self, UintEditor):
        if not UintEditor.objectName():
            UintEditor.setObjectName(u"UintEditor")
        UintEditor.resize(400, 300)
        font = QFont()
        font.setPointSize(12)
        UintEditor.setFont(font)
        self.gridLayout = QGridLayout(UintEditor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lblMinValue = QLabel(UintEditor)
        self.lblMinValue.setObjectName(u"lblMinValue")

        self.gridLayout.addWidget(self.lblMinValue, 1, 0, 1, 1)

        self.lblDefaultValue = QLabel(UintEditor)
        self.lblDefaultValue.setObjectName(u"lblDefaultValue")

        self.gridLayout.addWidget(self.lblDefaultValue, 0, 0, 1, 1)

        self.sbDefaultValue = QSpinBox(UintEditor)
        self.sbDefaultValue.setObjectName(u"sbDefaultValue")

        self.gridLayout.addWidget(self.sbDefaultValue, 0, 1, 1, 1)

        self.sbMinValue = QSpinBox(UintEditor)
        self.sbMinValue.setObjectName(u"sbMinValue")

        self.gridLayout.addWidget(self.sbMinValue, 1, 1, 1, 1)

        self.lblMaxValue = QLabel(UintEditor)
        self.lblMaxValue.setObjectName(u"lblMaxValue")

        self.gridLayout.addWidget(self.lblMaxValue, 2, 0, 1, 1)

        self.sbMaxValue = QSpinBox(UintEditor)
        self.sbMaxValue.setObjectName(u"sbMaxValue")

        self.gridLayout.addWidget(self.sbMaxValue, 2, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)


        self.retranslateUi(UintEditor)

        QMetaObject.connectSlotsByName(UintEditor)
    # setupUi

    def retranslateUi(self, UintEditor):
        UintEditor.setWindowTitle(QCoreApplication.translate("UintEditor", u"Form", None))
        self.lblMinValue.setText(QCoreApplication.translate("UintEditor", u"Minimum Value:", None))
        self.lblDefaultValue.setText(QCoreApplication.translate("UintEditor", u"Default Value:", None))
        self.lblMaxValue.setText(QCoreApplication.translate("UintEditor", u"Maximum Value:", None))
    # retranslateUi

