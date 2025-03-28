# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'appWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHeaderView,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QToolBar,
    QTreeView, QWidget)
from ..assets import resources_rc

class Ui_appWindow(object):
    def setupUi(self, appWindow):
        if not appWindow.objectName():
            appWindow.setObjectName(u"appWindow")
        appWindow.resize(800, 600)
        icon = QIcon()
        icon.addFile(u":/Icons/icons/app-icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        appWindow.setWindowIcon(icon)
        self.actionOpen = QAction(appWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen))
        self.actionOpen.setIcon(icon1)
        font = QFont()
        font.setPointSize(12)
        self.actionOpen.setFont(font)
        self.actionSave = QAction(appWindow)
        self.actionSave.setObjectName(u"actionSave")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.actionSave.setIcon(icon2)
        self.actionSave.setFont(font)
        self.actionSave_as = QAction(appWindow)
        self.actionSave_as.setObjectName(u"actionSave_as")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSaveAs))
        self.actionSave_as.setIcon(icon3)
        self.actionSave_as.setFont(font)
        self.actionNew = QAction(appWindow)
        self.actionNew.setObjectName(u"actionNew")
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentNew))
        self.actionNew.setIcon(icon4)
        self.actionNew.setFont(font)
        self.actionGenerate_All = QAction(appWindow)
        self.actionGenerate_All.setObjectName(u"actionGenerate_All")
        self.actionGenerate_All.setFont(font)
        self.actionGenerate_CDDL = QAction(appWindow)
        self.actionGenerate_CDDL.setObjectName(u"actionGenerate_CDDL")
        self.actionGenerate_CDDL.setFont(font)
        self.actionGenerate_Header = QAction(appWindow)
        self.actionGenerate_Header.setObjectName(u"actionGenerate_Header")
        self.actionGenerate_Header.setFont(font)
        self.actionGenerate_Binary = QAction(appWindow)
        self.actionGenerate_Binary.setObjectName(u"actionGenerate_Binary")
        self.actionGenerate_Binary.setFont(font)
        self.centralwidget = QWidget(appWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.objectListGroupBox = QGroupBox(self.centralwidget)
        self.objectListGroupBox.setObjectName(u"objectListGroupBox")
        self.objectListGroupBox.setFont(font)
        self.objectListGroupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_2 = QGridLayout(self.objectListGroupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pbDeleteObject = QPushButton(self.objectListGroupBox)
        self.pbDeleteObject.setObjectName(u"pbDeleteObject")
        self.pbDeleteObject.setEnabled(False)
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.pbDeleteObject.setIcon(icon5)
        self.pbDeleteObject.setIconSize(QSize(24, 24))

        self.gridLayout_2.addWidget(self.pbDeleteObject, 1, 1, 1, 1)

        self.tvObjectList = QTreeView(self.objectListGroupBox)
        self.tvObjectList.setObjectName(u"tvObjectList")

        self.gridLayout_2.addWidget(self.tvObjectList, 0, 0, 1, 3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 2, 1, 1)

        self.pbAddObject = QPushButton(self.objectListGroupBox)
        self.pbAddObject.setObjectName(u"pbAddObject")
        self.pbAddObject.setEnabled(False)
        icon6 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ContactNew))
        self.pbAddObject.setIcon(icon6)
        self.pbAddObject.setIconSize(QSize(24, 24))

        self.gridLayout_2.addWidget(self.pbAddObject, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.objectListGroupBox, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        font1 = QFont()
        font1.setFamilies([u"Bitstream Charter"])
        font1.setPointSize(12)
        self.groupBox_2.setFont(font1)
        self.groupBox_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)

        self.gridLayout.setColumnStretch(0, 100)
        self.gridLayout.setColumnStretch(1, 100)
        appWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(appWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 27))
        self.menubar.setFont(font)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setFont(font)
        self.menuDatastore_Tool = QMenu(self.menubar)
        self.menuDatastore_Tool.setObjectName(u"menuDatastore_Tool")
        self.menuDatastore_Tool.setFont(font)
        appWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(appWindow)
        self.statusbar.setObjectName(u"statusbar")
        appWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(appWindow)
        self.toolBar.setObjectName(u"toolBar")
        appWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDatastore_Tool.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuDatastore_Tool.addAction(self.actionGenerate_All)
        self.menuDatastore_Tool.addAction(self.actionGenerate_CDDL)
        self.menuDatastore_Tool.addAction(self.actionGenerate_Header)
        self.menuDatastore_Tool.addAction(self.actionGenerate_Binary)
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)

        self.retranslateUi(appWindow)

        QMetaObject.connectSlotsByName(appWindow)
    # setupUi

    def retranslateUi(self, appWindow):
        appWindow.setWindowTitle(QCoreApplication.translate("appWindow", u"CBOR Datastore Creator", None))
        self.actionOpen.setText(QCoreApplication.translate("appWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("appWindow", u"Save", None))
        self.actionSave_as.setText(QCoreApplication.translate("appWindow", u"Save as", None))
        self.actionNew.setText(QCoreApplication.translate("appWindow", u"New", None))
        self.actionGenerate_All.setText(QCoreApplication.translate("appWindow", u"Generate All", None))
        self.actionGenerate_CDDL.setText(QCoreApplication.translate("appWindow", u"Generate CDDL", None))
        self.actionGenerate_Header.setText(QCoreApplication.translate("appWindow", u"Generate Header", None))
        self.actionGenerate_Binary.setText(QCoreApplication.translate("appWindow", u"Generate Binary", None))
        self.objectListGroupBox.setTitle(QCoreApplication.translate("appWindow", u"Datastore's Objects", None))
#if QT_CONFIG(tooltip)
        self.pbDeleteObject.setToolTip(QCoreApplication.translate("appWindow", u"Remove object", None))
#endif // QT_CONFIG(tooltip)
        self.pbDeleteObject.setText("")
#if QT_CONFIG(tooltip)
        self.pbAddObject.setToolTip(QCoreApplication.translate("appWindow", u"Add object", None))
#endif // QT_CONFIG(tooltip)
        self.pbAddObject.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("appWindow", u"Object Editor", None))
        self.menuFile.setTitle(QCoreApplication.translate("appWindow", u"File", None))
        self.menuDatastore_Tool.setTitle(QCoreApplication.translate("appWindow", u"Datastore Tool", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("appWindow", u"toolBar", None))
    # retranslateUi

