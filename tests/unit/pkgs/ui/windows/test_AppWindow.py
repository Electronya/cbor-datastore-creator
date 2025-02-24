from unittest import TestCase
from unittest.mock import call, Mock, patch

from PySide6.QtWidgets import QMessageBox

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.windows import AppWindow                       # noqa: E402
from pkgs.ui.models import DatastoreNodeType                # noqa: E402


class TestAppWindow(TestCase):
    """
    AppWindow test cases.
    """
    def setUp(self) -> None:
        self._QMainWindow = 'pkgs.ui.windows.appWindow.qtw.QMainWindow.' \
            '__init__'
        self._QMsgBoxCls = 'pkgs.ui.windows.appWindow.qtw.QMessageBox'
        self._QDateCls = 'pkgs.ui.windows.appWindow.qtc.QDate'
        self._DatastoreNodeCls = 'pkgs.ui.windows.appWindow.DatastoreNode'
        self._DatastoreModelCls = 'pkgs.ui.windows.appWindow.DatastoreModel'
        self._DatastoreCls = 'pkgs.ui.windows.appWindow.Datastore'
        self._DatastoreDataCls = 'pkgs.ui.windows.appWindow.DatastoreData'
        self._loggingMod = 'pkgs.ui.windows.appWindow.logging'
        self._mockedLogger = Mock()
        with patch(self._loggingMod) as mockedLoggingMod, \
                patch(self._QMainWindow), patch.object(AppWindow, 'setupUi'), \
                patch.object(AppWindow, '_initUi'):
            mockedLoggingMod.getLogger.return_value = self._mockedLogger
            self._uut = AppWindow()
        self._setUpMockedWidgets()
        self._mockedLogger.reset_mock()

    def _setUpMockedWidgets(self):
        """
        Setup the mocked widgets.
        """
        self._uut.actionNew = Mock()
        self._uut.tvObjectList = Mock()

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the main window logger.
        """
        with patch(self._loggingMod) as mockedLoggingMod, \
                patch(self._QMainWindow), patch.object(AppWindow, 'setupUi'), \
                patch.object(AppWindow, '_initUi'):
            AppWindow()
            mockedLoggingMod.getLogger \
                .assert_called_once_with('app.windows.main')

    def test_constructorSetupUi(self) -> None:
        """
        The constructor must setup the UI.
        """
        with patch(self._QMainWindow), \
                patch(self._QMainWindow), \
                patch.object(AppWindow, 'setupUi') as mockedSetupUi, \
                patch.object(AppWindow, '_initUi'):
            testAppWindow = AppWindow()
            mockedSetupUi.assert_called_once_with(testAppWindow)

    def test_constructorInitUi(self) -> None:
        """
        The constructor must initialize the UI submodules.
        """
        with patch(self._QMainWindow), \
                patch(self._QMainWindow), patch.object(AppWindow, 'setupUi'), \
                patch.object(AppWindow, '_initUi') as mockedInitUi:
            AppWindow()
            mockedInitUi.assert_called_once()

    def test_initUiConnectEventsAndSlots(self) -> None:
        """
        The _initUi method must connect all the window events to there
        corresponding slots.
        """
        self._uut._initUi()
        self._uut.actionNew.triggered.connect \
            .assert_called_once_with(self._uut._createNewStore)

    def test_createNewStoreCreateNewStore(self) -> None:
        """
        The _createNewStore method must create a new empty datastore and create
        the tree view model based on it.
        """
        date = '2025-02-24'
        datastoreData = Mock()
        datastore = Mock()
        rootNode = Mock()
        datastoreNode = Mock()
        model = Mock()
        nodes = [rootNode, datastoreNode, None, None, None,
                 None, None, None, None, None, None]
        nodeNames = ['', None, 'Buttons', 'Button Arrays', 'Floats',
                     'Float Arrays', 'Multi-States', 'Signed Integers',
                     'Signed Integer Arrays', 'Unsigned Integers',
                     'Unsigned Integer Arrays']
        expectedCalls = []
        for idx, node in enumerate(nodes):
            if idx == 0:
                expectedCalls.append(call(DatastoreNodeType.OBJ_LIST,
                                          name=nodeNames[idx]))
            elif nodeNames[idx] is None:
                expectedCalls.append(call(DatastoreNodeType.STORE,
                                          data=datastore, parent=rootNode))
            else:
                expectedCalls.append(call(DatastoreNodeType.OBJ_LIST,
                                          name=nodeNames[idx],
                                          parent=datastoreNode))
        with patch(self._QDateCls) as mockedDate, \
                patch(self._DatastoreDataCls) as mockedDatastoreData, \
                patch(self._DatastoreCls) as mockedDatastore, \
                patch(self._DatastoreNodeCls) as mockedDatastoreNode, \
                patch(self._DatastoreModelCls) as mockedDatastoreModel:
            mockedDate.currentDate().toString.return_value = date
            mockedDatastoreData.return_value = datastoreData
            mockedDatastore.return_value = datastore
            mockedDatastoreNode.side_effect = nodes
            mockedDatastoreModel.return_value = model
            self._uut._createNewStore()
            self._mockedLogger.info \
                .assert_called_once_with('creating new datastore')
            mockedDate.currentDate() \
                .toString.assert_called_once_with('yyyy-mm-dd')
            mockedDatastoreData.assert_called_once_with('datastore', date)
            mockedDatastore.assert_called_once_with(datastoreData)
            mockedDatastoreNode.assert_has_calls(expectedCalls)
            mockedDatastoreModel.assert_called_once_with(rootNode)
            self._uut.tvObjectList.setModel.assert_called_once_with(model)
            self._uut.tvObjectList.expandAll.assert_called_once_with()

    def test_createErrorMsgBoxNewMsgBox(self) -> None:
        """
        The _createErrorMsgBox method must create the new message box.
        """
        mockedMsgBox = Mock()
        testLvl = QMessageBox.Warning
        testException = Exception('test error')
        with patch(self._QMsgBoxCls) as mockedMsgBoxCls:
            mockedMsgBoxCls.return_value = mockedMsgBox
            self._uut._createErrorMsgBox(testLvl, testException)
            mockedMsgBoxCls.assert_called_once_with(self._uut)
            mockedMsgBox.setWindowTitle.assert_called_once_with('Error!!')
            mockedMsgBox.setText.assert_called_once_with(str(testException))
            mockedMsgBox.setIcon.assert_called_once_with(testLvl)

    def test_createErrorMsgBoxCriticalQuit(self) -> None:
        """
        The _createErrorMsgBox method must connect the button clicked signal
        to the application quit slot when the level is critical.
        """
        mockedMsgBox = Mock()
        testException = Exception('test error')
        with patch(self._QMsgBoxCls) as mockedMsgBoxCls:
            mockedMsgBoxCls.return_value = mockedMsgBox
            testLvls = [mockedMsgBoxCls.Warning, mockedMsgBoxCls.Critical]
            for testLvl in testLvls:
                self._uut._createErrorMsgBox(testLvl, testException)
            mockedMsgBox.buttonClicked.connect.assert_called_once()

    def test_createErrorMsgBoxExec(self) -> None:
        """
        The _createErrorMsgBox method must execute the created message box.
        """
        mockedMsgBox = Mock()
        testLvl = QMessageBox.Warning
        testException = Exception('test error')
        with patch(self._QMsgBoxCls) as mockedMsgBoxCls:
            mockedMsgBoxCls.return_value = mockedMsgBox
            self._uut._createErrorMsgBox(testLvl, testException)
            mockedMsgBox.exec_.assert_called_once()
