# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'integerEditor.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QRadioButton,
    QSizePolicy, QSpacerItem, QSpinBox, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(685, 645)
        font = QFont()
        font.setPointSize(11)
        Form.setFont(font)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lblMax = QLabel(Form)
        self.lblMax.setObjectName(u"lblMax")
        self.lblMax.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.lblMax, 2, 2, 1, 1)

        self.lblDefault = QLabel(Form)
        self.lblDefault.setObjectName(u"lblDefault")
        self.lblDefault.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.lblDefault, 2, 4, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.sbMax = QSpinBox(Form)
        self.sbMax.setObjectName(u"sbMax")

        self.gridLayout.addWidget(self.sbMax, 2, 3, 1, 1)

        self.lblObjectName = QLabel(Form)
        self.lblObjectName.setObjectName(u"lblObjectName")
        self.lblObjectName.setFont(font)

        self.gridLayout.addWidget(self.lblObjectName, 0, 0, 1, 1)

        self.lblMin = QLabel(Form)
        self.lblMin.setObjectName(u"lblMin")
        self.lblMin.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.lblMin, 2, 0, 1, 1)

        self.sbMin = QSpinBox(Form)
        self.sbMin.setObjectName(u"sbMin")

        self.gridLayout.addWidget(self.sbMin, 2, 1, 1, 1)

        self.sbDefault = QSpinBox(Form)
        self.sbDefault.setObjectName(u"sbDefault")

        self.gridLayout.addWidget(self.sbDefault, 2, 5, 1, 1)

        self.cbInNvm = QCheckBox(Form)
        self.cbInNvm.setObjectName(u"cbInNvm")

        self.gridLayout.addWidget(self.cbInNvm, 0, 5, 1, 1)

        self.gbSize = QGroupBox(Form)
        self.gbSize.setObjectName(u"gbSize")
        self.gbSize.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.horizontalLayout = QHBoxLayout(self.gbSize)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.rb1Byte = QRadioButton(self.gbSize)
        self.rb1Byte.setObjectName(u"rb1Byte")

        self.horizontalLayout.addWidget(self.rb1Byte)

        self.rb2Byte = QRadioButton(self.gbSize)
        self.rb2Byte.setObjectName(u"rb2Byte")

        self.horizontalLayout.addWidget(self.rb2Byte)

        self.rb4Byte = QRadioButton(self.gbSize)
        self.rb4Byte.setObjectName(u"rb4Byte")
        self.rb4Byte.setChecked(True)

        self.horizontalLayout.addWidget(self.rb4Byte)

        self.rb8Byte = QRadioButton(self.gbSize)
        self.rb8Byte.setObjectName(u"rb8Byte")

        self.horizontalLayout.addWidget(self.rb8Byte)


        self.gridLayout.addWidget(self.gbSize, 1, 0, 1, 6)

        self.leObjectName = QLineEdit(Form)
        self.leObjectName.setObjectName(u"leObjectName")
        self.leObjectName.setFont(font)

        self.gridLayout.addWidget(self.leObjectName, 0, 1, 1, 4)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lblMax.setText(QCoreApplication.translate("Form", u"Maximum:", None))
        self.lblDefault.setText(QCoreApplication.translate("Form", u"Default:", None))
        self.lblObjectName.setText(QCoreApplication.translate("Form", u"Object Name:", None))
        self.lblMin.setText(QCoreApplication.translate("Form", u"Minimum:", None))
        self.cbInNvm.setText(QCoreApplication.translate("Form", u"In NVM", None))
        self.gbSize.setTitle(QCoreApplication.translate("Form", u"Size", None))
        self.rb1Byte.setText(QCoreApplication.translate("Form", u"1 Byte", None))
        self.rb2Byte.setText(QCoreApplication.translate("Form", u"2 Bytes", None))
        self.rb4Byte.setText(QCoreApplication.translate("Form", u"4 Bytes", None))
        self.rb8Byte.setText(QCoreApplication.translate("Form", u"8 Bytes", None))
        self.leObjectName.setPlaceholderText(QCoreApplication.translate("Form", u"INTEGER_1", None))
    # retranslateUi

