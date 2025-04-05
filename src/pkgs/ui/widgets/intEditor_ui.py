# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'intEditor.ui'
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

class Ui_IntEditor(object):
    def setupUi(self, IntEditor):
        if not IntEditor.objectName():
            IntEditor.setObjectName(u"IntEditor")
        IntEditor.resize(400, 300)
        font = QFont()
        font.setPointSize(12)
        IntEditor.setFont(font)
        self.gridLayout = QGridLayout(IntEditor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lblMinValue = QLabel(IntEditor)
        self.lblMinValue.setObjectName(u"lblMinValue")

        self.gridLayout.addWidget(self.lblMinValue, 1, 0, 1, 1)

        self.lblDefaultValue = QLabel(IntEditor)
        self.lblDefaultValue.setObjectName(u"lblDefaultValue")

        self.gridLayout.addWidget(self.lblDefaultValue, 0, 0, 1, 1)

        self.sbDefaultValue = QSpinBox(IntEditor)
        self.sbDefaultValue.setObjectName(u"sbDefaultValue")

        self.gridLayout.addWidget(self.sbDefaultValue, 0, 1, 1, 1)

        self.sbMinValue = QSpinBox(IntEditor)
        self.sbMinValue.setObjectName(u"sbMinValue")

        self.gridLayout.addWidget(self.sbMinValue, 1, 1, 1, 1)

        self.lblMaxValue = QLabel(IntEditor)
        self.lblMaxValue.setObjectName(u"lblMaxValue")

        self.gridLayout.addWidget(self.lblMaxValue, 2, 0, 1, 1)

        self.sbMaxValue = QSpinBox(IntEditor)
        self.sbMaxValue.setObjectName(u"sbMaxValue")

        self.gridLayout.addWidget(self.sbMaxValue, 2, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)


        self.retranslateUi(IntEditor)

        QMetaObject.connectSlotsByName(IntEditor)
    # setupUi

    def retranslateUi(self, IntEditor):
        IntEditor.setWindowTitle(QCoreApplication.translate("IntEditor", u"Form", None))
        self.lblMinValue.setText(QCoreApplication.translate("IntEditor", u"Minimum Value:", None))
        self.lblDefaultValue.setText(QCoreApplication.translate("IntEditor", u"Default Value:", None))
        self.lblMaxValue.setText(QCoreApplication.translate("IntEditor", u"Maximum Value:", None))
    # retranslateUi

