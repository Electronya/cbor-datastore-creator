# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'floatEditor.ui'
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QGridLayout, QLabel,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_FloatEditor(object):
    def setupUi(self, FloatEditor):
        if not FloatEditor.objectName():
            FloatEditor.setObjectName(u"FloatEditor")
        FloatEditor.resize(400, 300)
        font = QFont()
        font.setPointSize(12)
        FloatEditor.setFont(font)
        self.gridLayout = QGridLayout(FloatEditor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lblDefaultValue = QLabel(FloatEditor)
        self.lblDefaultValue.setObjectName(u"lblDefaultValue")

        self.gridLayout.addWidget(self.lblDefaultValue, 0, 0, 1, 1)

        self.dsbMaxValue = QDoubleSpinBox(FloatEditor)
        self.dsbMaxValue.setObjectName(u"dsbMaxValue")

        self.gridLayout.addWidget(self.dsbMaxValue, 2, 1, 1, 1)

        self.lblMaxValue = QLabel(FloatEditor)
        self.lblMaxValue.setObjectName(u"lblMaxValue")

        self.gridLayout.addWidget(self.lblMaxValue, 2, 0, 1, 1)

        self.dsbMinValue = QDoubleSpinBox(FloatEditor)
        self.dsbMinValue.setObjectName(u"dsbMinValue")

        self.gridLayout.addWidget(self.dsbMinValue, 1, 1, 1, 1)

        self.dsbDefaultValue = QDoubleSpinBox(FloatEditor)
        self.dsbDefaultValue.setObjectName(u"dsbDefaultValue")

        self.gridLayout.addWidget(self.dsbDefaultValue, 0, 1, 1, 1)

        self.lblMinValue = QLabel(FloatEditor)
        self.lblMinValue.setObjectName(u"lblMinValue")

        self.gridLayout.addWidget(self.lblMinValue, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)


        self.retranslateUi(FloatEditor)

        QMetaObject.connectSlotsByName(FloatEditor)
    # setupUi

    def retranslateUi(self, FloatEditor):
        FloatEditor.setWindowTitle(QCoreApplication.translate("FloatEditor", u"Form", None))
        self.lblDefaultValue.setText(QCoreApplication.translate("FloatEditor", u"Default Value:", None))
        self.lblMaxValue.setText(QCoreApplication.translate("FloatEditor", u"Maximum Value:", None))
        self.lblMinValue.setText(QCoreApplication.translate("FloatEditor", u"Minimum Value:", None))
    # retranslateUi

